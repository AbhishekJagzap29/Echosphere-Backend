from odoo import models, fields


class WebsiteContent(models.Model):
    _name = 'website.content'
    _description = 'Website Content'

    name = fields.Char(required=True)

    mission = fields.Html()

    vision = fields.Html()

    about_company = fields.Html()

    iso_content = fields.Html()

    what_we_do = fields.Html()

    what_we_think = fields.Html()

    careers = fields.Html()

    contact_us = fields.Html()

    future_plans = fields.Html()

    founder_name = fields.Char()

    founder_image = fields.Image()

    ceo_message = fields.Html()

    company_logo = fields.Image()

    hero_banner = fields.Image()

    active = fields.Boolean(default=True)