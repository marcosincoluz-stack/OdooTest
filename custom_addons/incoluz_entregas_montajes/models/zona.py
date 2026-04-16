from odoo import fields, models


class IncoluzZona(models.Model):
    """Modelo de Zona de Montaje/Entrega.
    
    Replica el modelo que existe en el ERP de producción.
    Cada zona representa un instalador o equipo de montaje
    al que se le asignan albaranes de entrega.
    """
    _name = 'incoluz_entregas_montajes.zona'
    _description = 'Zona de Montaje/Entrega'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Nombre del instalador o zona de montaje"
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
    )
    notes = fields.Text(
        string="Notas",
        help="Notas internas sobre esta zona"
    )
