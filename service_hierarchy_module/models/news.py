from odoo import models, fields


class ServiceNews(models.Model):
    _name = 'service.news'

    title = fields.Char(required=True)

    description = fields.Text()

    image = fields.Image()

    date = fields.Date()

    active = fields.Boolean(default=True)