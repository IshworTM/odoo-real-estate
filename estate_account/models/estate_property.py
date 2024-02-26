from odoo import models

# Estate Property Model
class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold_property(self):
        for property_record in self:
            selling_price = property_record.selling_price
            administrative_fee = 100.00
            invoice = self.env['account.move'].create(
                {
                'partner_id': property_record.buyer_id.id, 
                'move_type': 'out_invoice',
                'invoice_line_ids':[
                    (0, 0, {
                    'name': 'Property Sale (6% of selling price)',
                    'quantity': 1,
                    'price_unit': selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': administrative_fee,
                })
                ]
            })
        return super(EstateProperty, self).action_sold_property()
    