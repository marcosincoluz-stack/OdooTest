import os, sys
sys.path.append('c:\\Users\\marcos\\Desktop\\Odoo\\odoo_14.0')
import odoo
import json

def audit():
    odoo.tools.config.parse(['-c', 'c:\\Users\\marcos\\Desktop\\Odoo\\odoo_14.0\\odoo.conf'])
    registry = odoo.registry('odoo14_test')
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, 1, {})
        ICP = env['ir.config_parameter'].sudo()
        url = ICP.get_param('incorutas.supabase_url') or ""
        key = ICP.get_param('incorutas.supabase_service_role_key') or ""
        return url, key

if __name__ == "__main__":
    try:
        url, key = audit()
        print(f"URL: {url}")
        print(f"KEY_START: {key[:10]}")
        print(f"KEY_END: {key[-10:]}")
        print(f"KEY_LENGTH: {len(key)}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
