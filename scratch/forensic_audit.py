import os, sys
sys.path.append('c:\\Users\\marcos\\Desktop\\Odoo\\odoo_14.0')
import odoo
import json

def audit_record():
    odoo.tools.config.parse(['-c', 'c:\\Users\\marcos\\Desktop\\Odoo\\odoo_14.0\\odoo.conf'])
    registry = odoo.registry('odoo14_test')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, 1, {})
        # Buscar el 00001
        pick = env['stock.picking'].search([('name', 'ilike', '00001')], limit=1)
        if not pick:
            return {"error": "Albarán 00001 no encontrado"}
        
        return {
            "name": pick.name,
            "id": pick.id,
            "zona_name": pick.zona_id.name if pick.zona_id else "SIN ZONA",
            "zona_supabase_id": pick.zona_id.supabase_id if pick.zona_id else "N/A",
            "sync_status": pick.supabase_sync_status,
            "vals": {
                "titulo": pick.x_titulo_montaje,
                "responsable": pick.x_responsable,
                "referencia": pick.x_referencia
            }
        }

if __name__ == "__main__":
    try:
        res = audit_record()
        print(json.dumps(res, indent=4))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
