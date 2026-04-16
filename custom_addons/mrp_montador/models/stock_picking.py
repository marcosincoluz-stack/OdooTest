import json
import logging
import urllib.request
import urllib.error
import base64

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    supabase_sync_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('synced', 'Sincronizado'),
        ('error', 'Error'),
    ], string="Estado Sincronización App", default='pending', copy=False)

    @api.model
    def cron_sync_pending_jobs(self):
        """Robot de fondo que procesa la cola de sincronización."""
        # Buscamos registros pendientes (limitamos a 50 para no saturar en una sola pasada)
        pending_picks = self.search([
            ('supabase_sync_status', '=', 'pending'),
            ('zona_id', '!=', False)
        ], limit=50)

        if not pending_picks:
            return True

        _logger.info("Cron: Procesando %d albaranes pendientes para Supabase...", len(pending_picks))
        for pick in pending_picks:
            try:
                # Llamamos a la sincronización (que ya tiene sus propios try/except)
                pick.action_sync_to_supabase()
                # Pequeña pausa para no ametrallar la red si hay muchos
                self.env.cr.commit() 
            except Exception as e:
                _logger.error("Error en Cron procesando %s: %s", pick.name, str(e))
        return True

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.zona_id and record.supabase_sync_status == 'pending':
                # Solo nos aseguramos de que esté en pending (el Cron hará el resto)
                pass
        return records

    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        # Si tiene zona, nos aseguramos de que vuelva a estado 'pendiente' para que el Cron lo procese
        if any(f in vals for f in ['x_titulo_montaje', 'x_responsable', 'x_referencia', 'x_notas_programacion', 'zona_id', 'state']):
            for record in self:
                if record.zona_id and record.supabase_sync_status != 'pending':
                    self.env.cr.execute("UPDATE stock_picking SET supabase_sync_status = 'pending' WHERE id = %s", (record.id,))
                    # No hacemos commit aquí, dejamos que el write de Odoo cierre su transacción
        return res

    def action_sync_to_supabase(self):
        """Sincronización automática de Albarán y PDFs al asignar Zona."""
        self.ensure_one()
        
        if not self.zona_id:
            return

        if not hasattr(self.zona_id, 'supabase_id') or not self.zona_id.supabase_id:
            return

        ICP = self.env['ir.config_parameter'].sudo()
        url = ICP.get_param('incorutas.supabase_url')
        key = ICP.get_param('incorutas.supabase_service_role_key')

        if not url or not key:
            return

        # 1. Obtener PDFs adjuntos
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'stock.picking'),
            ('res_id', '=', self.id),
            ('mimetype', '=', 'application/pdf')
        ], order='create_date asc')

        pdf_urls = [None, None]
        
        for i, att in enumerate(attachments[:2]):
            storage_path = f"mounting-orders/{self.id}_{i}_{att.name}"
            storage_url = f"{url.rstrip('/')}/storage/v1/object/{storage_path}"
            
            headers = {
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/pdf"
            }
            try:
                pdf_content = base64.b64decode(att.datas)
                req = urllib.request.Request(storage_url, data=pdf_content, headers=headers, method='POST')
                urllib.request.urlopen(req, timeout=15)
                
                public_url = f"{url.rstrip('/')}/storage/v1/object/public/{storage_path}"
                pdf_urls[i] = public_url
            except Exception as e:
                _logger.warning("Error subiendo PDF %s: %s", att.name, e)

        # 2. Payload para 'jobs' (Usamos None para campos vacíos para evitar errores de tipo en DB)
        payload = {
            "title": self.x_titulo_montaje or self.name,
            "client_name": self.partner_id.name or "Sin Cliente",
            "address": self.partner_id.contact_address or "Sin Dirección",
            "description": self.x_notas_programacion or None,
            "mounting_order": self.x_referencia or None,
            "responsable": self.x_responsable or None,
            "assigned_to": self.zona_id.supabase_id,
            "mounting_order_url": pdf_urls[0],
            "plans_url": pdf_urls[1],
            "status": "pending",
            "odoo_task_id": self.id,
            "external_sync_status": "synced"
        }

        try:
            # Usamos on_conflict para que sea un UPSERT (actualizar si ya existe)
            full_url = f"{url.rstrip('/')}/rest/v1/jobs?on_conflict=odoo_task_id"
            headers = {
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            data_json = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(full_url, data=data_json, headers=headers, method='POST')
            
            # Realizamos la petición con timeout estricto para evitar bloqueos del worker
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    status_code = response.getcode()
                
                # ACTUALIZACIÓN DE ESTADO
                self.env.cr.execute("UPDATE stock_picking SET supabase_sync_status = 'synced' WHERE id = %s", (self.id,))
                self.env.cr.commit()
            except Exception as net_error:
                # Si falla la red, registramos pero no rompemos el proceso
                _logger.error("Error de red sincronizando %s: %s", self.name, str(net_error))
                self.env.cr.execute("UPDATE stock_picking SET supabase_sync_status = 'error' WHERE id = %s", (self.id,))
                self.env.cr.commit()

        except urllib.error.HTTPError as e:
            # En caso de error HTTP, informamos al log sin volcar el contenido de la petición (por seguridad)
            _logger.error("Fallo respuesta API Supabase para %s: Código %s", self.name, e.code)
            self.env.cr.execute("UPDATE stock_picking SET supabase_sync_status = 'error' WHERE id = %s", (self.id,))
            self.env.cr.commit()

        except Exception as e:
            # Error genérico capturado silenciosamente para no asustar al usuario final
            _logger.error("Fallo inesperado sincronizador %s: %s", self.name, str(e))
            self.env.cr.execute("UPDATE stock_picking SET supabase_sync_status = 'error' WHERE id = %s", (self.id,))
            self.env.cr.commit()


