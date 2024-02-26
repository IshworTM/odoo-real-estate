from odoo import models, fields, api
from collections import Counter

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence"

    name = fields.Char(
        required=True,
        string="Name"
    )
    sequence = fields.Integer(
        'Sequence',
    )
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        required=True,
        string="Property IDs"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        inverse_name="property_type_id",
        string="Offer ID"
    )
    offer_count = fields.Integer(
        compute="_compute_count_property",
        string="Offer Count"
    )

    @api.depends('offer_ids')
    def _compute_count_property(self):
        for rec in self:
            rec.offer_count = Counter(rec.offer_ids)

    _sql_constraints = {(
        'property_type_unique',
        'unique(name)',
        'The Proprty Type must be different!!'
    )}

    def action_stat_button(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:

            res = self.env['ir.actions.act_window']._for_xml_id(xml_id)
            res.update(
                context=dict(
                    self.env.context,
                    default_property_type_id=self.id,
                    group_by=False
                ),
                domain=[('property_type_id', '=', self.id)]
            )
            return res
        return False
    
