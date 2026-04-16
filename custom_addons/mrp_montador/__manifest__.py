{
    "name": "Satélite IncoRutas (Sync Externa)",
    "summary": "Sincroniza Albaranes (stock.picking) con Supabase Sign Installer",
    "description": """
        Módulo satélite para integrar el ERP externo con Supabase.
        - Sincroniza zonas a montadores.
        - Envía albaranes y sus PDFs al asignar zona_id.
    """,
    "version": "14.0.1.0.0",
    "author": "Marcos - Incoluz",
    "category": "Inventory",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "incoluz_entregas_montajes",
        "base",
        "mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/mrp_montador_cron.xml",
        "views/mrp_montador_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
}
