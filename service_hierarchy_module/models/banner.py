from odoo import models, fields


class ServiceBanner(models.Model):
    _name = 'service.banner'

    title = fields.Char()

    image = fields.Image(required=True)

    sequence = fields.Integer(default=10)

    active = fields.Boolean(default=True)