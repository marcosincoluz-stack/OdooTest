{
    "name": "Incoluz Entregas y Montajes",
    "summary": "Gestión de zonas de entrega y montaje para Incoluz",
    "description": """
        Módulo base que replica la funcionalidad del ERP de producción.
        - Define el modelo de Zonas de montaje.
        - Añade campo zona_id a los albaranes (stock.picking).
        - Sirve como base para el módulo satélite de sincronización.
    """,
    "version": "14.0.1.0.1",
    "author": "Marcos - Incoluz",
    "category": "Inventory",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/zona_views.xml",
        "views/stock_picking_views.xml",
        "data/demo_data.xml",
    ],
    "installable": True,
    "application": False,
}
