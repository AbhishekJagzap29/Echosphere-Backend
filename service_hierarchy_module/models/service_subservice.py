from odoo import models, fields


class ServiceSubservice(models.Model):
    _name = 'service.subservice'
    _description = 'Sub Service'

    name = fields.Char(string='Subservice Name', required=True)

    service_id = fields.Many2one(
        'service.service',
        string='Parent Service',
        required=True,
        ondelete='cascade'
    )

    detail_ids = fields.One2many(
        'service.detail',
        'subservice_id',
        string='Details'
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

    active = fields.Boolean(
        default=True
    )