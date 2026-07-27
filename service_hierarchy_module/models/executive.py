from odoo import models, fields


class Executive(models.Model):
    _name = 'service.executive'

    name = fields.Char()

    image = fields.Image()

    phone = fields.Char()

    designation = fields.Char()

    active = fields.Boolean(default=True)