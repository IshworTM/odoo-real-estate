from odoo import models, fields, api

class EstatePropertyInheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property', 
        'seller_id',
        domain="[('state','=','new'), ('state','=','offer_received')]"
    )
