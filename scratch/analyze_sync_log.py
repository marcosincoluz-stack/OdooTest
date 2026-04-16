import os

def read_log():
    try:
        with open('odoo_debug.log', 'rb') as f:
            content = f.read().decode('utf-16')
        
        lines = content.split('\n')
        found = False
        for i, line in enumerate(lines):
            if 'Respuesta Supabase OK' in line:
                print("--- ENCONTRADO ÉXITO ---")
                # Mostrar 5 líneas antes y 20 después
                start = max(0, i - 5)
                end = min(len(lines), i + 20)
                for j in range(start, end):
                    prefix = ">>> " if j == i else "    "
                    print(f"{prefix}{lines[j]}")
                found = True
                # No hacemos break por si hay varios intentos
        
        if not found:
            print("No se encontró 'Respuesta Supabase OK' en el log.")
            print("Últimas 20 líneas del log:")
            for line in lines[-20:]:
                print(line)
                
    except Exception as e:
        print(f"Error leyendo log: {e}")

if __name__ == "__main__":
    read_log()
