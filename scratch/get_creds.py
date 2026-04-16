from odoo import api, SUPERUSER_ID
import odoo
import json

def get_config():
    # Setup Odoo environment
    registry = odoo.registry('odoo14_test')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        ICP = env['ir.config_parameter'].sudo()
        url = ICP.get_param('incorutas.supabase_url')
        key = ICP.get_param('incorutas.supabase_service_role_key')
        return url, key

if __name__ == "__main__":
    try:
        url, key = get_config()
        print(json.dumps({"url": url, "key": key}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
