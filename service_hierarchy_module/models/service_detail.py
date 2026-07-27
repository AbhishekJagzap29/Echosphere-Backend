from odoo import models, fields


class ServiceDetail(models.Model):
    _name = 'service.detail'
    _description = 'Service Detail'
    _order = 'sequence asc, id desc'
    
    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    # discount = fields.Float(string='Discount (%)')
    discount_ids = fields.One2many(
        'provider.discount',
        'service_detail_id',
        string='Discounts'
    )
    image = fields.Image(
        string='Image',
        max_width=1920,
        max_height=1920
    )
    owner_id = fields.Char(string='Owner')
    facility_ids = fields.One2many(
        'provider.facility',
        'service_detail_id',
        string='Facilities'
    )
    subservice_id = fields.Many2one(
        'service.subservice',
        string='Subservice',
        required=True,
        ondelete='cascade'
    )

    whatsapp = fields.Char(
        string='WhatsApp'
    )

    email = fields.Char(
        string='Email'
    )

    website = fields.Char(
        string='Website'
    )

    rating = fields.Float(
        string='Rating'
    )

    review_count = fields.Integer(
        string='Review Count'
    )

    latitude = fields.Float(
        string='Latitude'
    )

    longitude = fields.Float(
        string='Longitude'
    )

    open_24_hours = fields.Boolean(
        string='24 Hours Open'
    )

    is_featured = fields.Boolean(
        string='Featured'
    )

    is_verified = fields.Boolean(
        string='Verified'
    )

    sequence = fields.Integer(
        default=10
    )

    active = fields.Boolean(
        default=True
    )

    taluka_id = fields.Many2one(
        'service.taluka',
        string='Taluka'
    )

    district = fields.Char(
        string='District'
    )

    state = fields.Char(
        string='State'
    )

    pincode = fields.Char(
        string='Pincode'
    )

    gallery_ids = fields.One2many(
        'provider.gallery',
        'service_detail_id',
        string='Gallery'
    )
    youtube_link = fields.Char(
        string='YouTube Link'
    )

    facebook_link = fields.Char(
        string='Facebook Link'
    )

    instagram_link = fields.Char(
        string='Instagram Link'
    )

class ProviderFacility(models.Model):
    _name = 'provider.facility'
    _description = 'Provider Facility'

    service_detail_id = fields.Many2one(
        'service.detail',
        ondelete='cascade'
    )

    service_request_id = fields.Many2one(
        'service.request',
        ondelete='cascade'
    )

    name = fields.Char(
        required=True
    )

class ProviderDiscount(models.Model):
    _name = 'provider.discount'
    _description = 'Provider Discount'

    name = fields.Char(
        required=True
    )

    service_detail_id = fields.Many2one(
        'service.detail',
        ondelete='cascade'
    )

    service_request_id = fields.Many2one(
        'service.request',
        ondelete='cascade'
    )
    