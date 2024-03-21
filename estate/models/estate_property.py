from odoo import _, models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

# Estate Property Model
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An Estate Property Model"
    _order = "id desc"
    
    name = fields.Char(
        required=True,
        string="Name"
    )
    description = fields.Text(
        string="Description"
    )
    postcode = fields.Char(
        string="Postal Code"
    )
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(),months=3),
        string="Availability Form"
    )
    expected_price = fields.Float(
        required=True,
        string="Expected Price"
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False,
        string="Selling Price"
    )
    bedrooms = fields.Integer(
        default=2,
        string="Bedrooms"
    )
    living_area = fields.Integer(
        string="Living Area"
    )
    facades = fields.Integer(
        string="Facades"
    )
    garage = fields.Boolean(
        string="Garage"
    )
    garden = fields.Boolean(
        string="Garden"
    )
    garden_area = fields.Integer(
        string="Garden Area"
    )
    garden_orientation = fields.Selection(
        selection= [
            ('north','North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Orientation"
    )
    state = fields.Selection(
        selection= [
            ('new','New'),
            ('offer_received','Offer Recieved'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Canceled')
        ],
        default='new',
        string="Status"
    )
    active = fields.Boolean(
        default=True,
        string="Active"
    )
    buyer_id = fields.Many2one(
        "res.partner",
        readonly=True,
        copy=False,
        string="Buyer"
    )
    seller_id = fields.Many2one(
        "res.users",
        string="Seller"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        required=True
    )
    total_area = fields.Integer(
        compute="_compute_total",
        string="Total Area"
    )
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Price"
    )
    @api.depends('living_area','garden_area')
    def _compute_total(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.offer_price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("offer_price"))
            else:
                rec.best_price = 0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price:
                minimun_value = rec.expected_price * 0.9
                if minimun_value > rec.selling_price:
                    raise ValidationError(_('The offer value must be greater than 90% of Expected Price!!'))

    _sql_constraints = {(
        'check_expected_price', 'CHECK(expected_price >= 0)',
        'The expected price cannot be less than 0!!'
        ), (
            'check_selling_price', 'CHECK(selling_price >= 0)',
            'The selling price cannot be less than 0!!'
        )
    }

    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10
                rec.garden_orientation = "north"
            else:
                rec.garden_area = 0
                rec.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_canceled(self):
        if any(rec.state != 'new' and rec.state !='cancel' for rec in self):
            raise UserError("You can only delete new or cancelled property!!")

    def action_sold_property(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(_("You cannot sell Cancelled Property"))
            else:
                rec.state = 'sold'
                return True

    def action_cancel_property(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("You cannot cancel Sold Property"))
            else:
                rec.state = 'cancel'
                return True


# Estate Property Tag Model
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(
        required=True
    )
    color = fields.Integer(
        "Color"
    )

    _sql_constraints = {(
        'property_tag_unique', 'unique(name)', 'The Proprty Tag must be different!!'
    )}

# Estate Property Offer Model
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Model"
    _order = "offer_price desc"

    offer_price = fields.Float(
        string="Offer Price"
    )
    status = fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ],
        string="Offer Status"
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Partner"
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
        string="Property"
    )
    validity = fields.Integer(
        default=7,
        string="Validity (in days)"
    )
    date_deadline = fields.Date(
        compute="_compute_validity_date",
        inverse="_inverse_validity_date"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )
    
    @api.depends("validity", "date_deadline")
    def _compute_validity_date(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = datetime.now().date() + timedelta(days=rec.validity)

    def _inverse_validity_date(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days
            else:
                rec.validity = (rec.date_deadline - datetime.now().date()).days

    _sql_constraints = {(
        'check_expected_offer_price', 'CHECK(offer_price >= 0)',
        'The offered price cannot be less than 0!!'
    )}

    @api.model_create_multi
    def create(self, vals):
        offer = self.env["estate.property.offer"].search([("property_id","=",vals[0]["property_id"])]).mapped("offer_price")
        if offer:
            max_offer = max(offer)
            if max_offer and vals[0]['offer_price'] < max_offer:
                raise exceptions.ValidationError(f"Cannot create offer with amount less than {int(max_offer)} :-(")
        res = super().create(vals)
        res.property_id.state = 'offer_received'
        return res

    def action_offer_accept(self):
            total_offers = self.property_id.offer_ids
            for rec in self:
                if any(offer.status == "accepted" for offer in total_offers):
                    raise UserError("Two offers cannot  be accepted at the same time!")
                rec.status = 'accepted'
                rec.property_id.buyer_id = rec.partner_id.id
                rec.property_id.selling_price = rec.offer_price
                rec.property_id.state = 'offer_accepted'

    def action_offer_refuse(self):
        for rec in self:
            rec.status = 'refused'