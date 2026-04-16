import psycopg2
import json

def audit():
    try:
        # Usamos los credenciales estándar de tu Odoo
        conn = psycopg2.connect("dbname='odoo14_test' user='odoo' password='odoo' host='localhost'")
        cur = conn.cursor()
        
        # 1. Buscar el albarán 00001 y su zona vinculada
        cur.execute("""
            SELECT 
                sp.id, 
                sp.name, 
                sp.zona_id, 
                z.name, 
                z.supabase_id 
            FROM stock_picking sp 
            LEFT JOIN incoluz_entregas_montajes_zona z ON sp.zona_id = z.id 
            WHERE sp.name ILIKE '%00001%'
        """)
        row = cur.fetchone()
        
        if not row:
            return {"error": "No se encontró el albarán con nombre parecido a 00001"}
            
        return {
            "success": True,
            "picking_id": row[0],
            "picking_name": row[1],
            "zona_id": row[2],
            "zona_name": row[3] if row[3] else "SIN NOMBRE",
            "zona_supabase_id": row[4] if row[4] else "FALTA ID SUPABASE"
        }
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print(json.dumps(audit(), indent=4))
