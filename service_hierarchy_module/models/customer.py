from odoo import models, fields


class ServiceCustomer(models.Model):
    _name = 'service.customer'

    name = fields.Char(required=True)

    photo = fields.Image()

    phone = fields.Char(required=True)

    card_number = fields.Char()

    dob = fields.Date()

    age = fields.Integer()

    address = fields.Text()

    taluka_id = fields.Many2one(
        'service.taluka',
        string='Taluka'
    )

    district = fields.Char()

    state = fields.Char()

    active = fields.Boolean(default=True)

    is_card_holder = fields.Boolean(
        string='Is Card Holder'
    )

class ServiceTaluka(models.Model):
    _name = 'service.taluka'
    _description = 'Taluka'

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)