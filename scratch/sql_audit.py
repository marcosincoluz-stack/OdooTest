import psycopg2
import json

def audit():
    try:
        conn = psycopg2.connect('dbname=odoo14_test user=odoo password=odoo host=localhost')
        cur = conn.cursor()
        
        # 1. Auditar Albarán 00001
        query = """
        SELECT 
            sp.id, 
            sp.name, 
            sp.zona_id, 
            sp.supabase_sync_status, 
            z.name as zona_name, 
            z.supabase_id as zona_supabase_id
        FROM stock_picking sp 
        LEFT JOIN mrp_montador_zona z ON sp.zona_id = z.id 
        WHERE sp.name ILIKE '%00001%' 
        LIMIT 1
        """
        cur.execute(query)
        res = cur.fetchone()
        
        if not res:
            return {"error": "Albarán no encontrado en la DB"}
            
        return {
            "id": res[0],
            "name": res[1],
            "zona_id": res[2],
            "status": res[3],
            "zona_name": res[4],
            "zona_supabase_id": res[5]
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print(json.dumps(audit(), indent=4))
