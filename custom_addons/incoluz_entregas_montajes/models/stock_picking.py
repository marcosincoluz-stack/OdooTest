from odoo import fields, models


class StockPicking(models.Model):
    """Extensión de stock.picking para añadir zona de montaje.
    
    Añade el campo zona_id a los albaranes, tal como existe
    en el ERP de producción. El módulo satélite (mrp_montador)
    se apoyará en este campo para sincronizar con Supabase.
    """
    _inherit = 'stock.picking'

    zona_id = fields.Many2one(
        'incoluz_entregas_montajes.zona',
        string="Zona de Montaje",
        help="Instalador o zona asignada a este albarán"
    )
    x_titulo_montaje = fields.Char(string='Título del Montaje')
    x_responsable = fields.Char(string='Responsable')
    x_referencia = fields.Char(string='Referencia Montaje')
    x_notas_programacion = fields.Text(string='Notas Programación')
