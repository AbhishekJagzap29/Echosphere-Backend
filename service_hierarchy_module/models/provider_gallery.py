from odoo import models, fields


class ProviderGallery(models.Model):
    _name = 'provider.gallery'
    _description = 'Provider Gallery'

    service_detail_id = fields.Many2one(
        'service.detail',
        ondelete='cascade'
    )
    service_request_id = fields.Many2one(
        'service.request',
        ondelete='cascade'
    )

    image = fields.Image(
        required=True
    )