import json
import logging
import urllib.request
import urllib.error

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class IncoluzZona(models.Model):
    _inherit = 'incoluz_entregas_montajes.zona'

    supabase_id = fields.Char(string="ID Supabase", help="ID del montador en Supabase")

    _sql_constraints = [
        ('supabase_id_unique', 'UNIQUE(supabase_id)', 'El ID de Supabase debe ser único por montador.'),
    ]

