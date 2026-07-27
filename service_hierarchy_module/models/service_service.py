from odoo import models, fields


class ServiceService(models.Model):
    _name = 'service.service'
    _description = 'Main Service'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text(string='Description')
    subservice_ids = fields.One2many(
        'service.subservice',
        'service_id',
        string='Subservices'
    )
    is_popular = fields.Boolean(
        string='Popular Service'
    )

    icon = fields.Image(
        string='Icon'
    )

    banner = fields.Image(
        string='Banner'
    )

    sequence = fields.Integer(
        default=10
    )

    is_featured = fields.Boolean(
        string='Featured'
    )

    active = fields.Boolean(
        default=True
    )
