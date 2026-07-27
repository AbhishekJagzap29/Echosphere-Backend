from odoo import models, fields


class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'

    service_id = fields.Many2one(
        'service.service'
    )
    executive_id = fields.Many2one(
        'res.users',
        string='Executive',
        default=lambda self: self.env.user
    )
    new_service = fields.Char()

    subservice_id = fields.Many2one(
        'service.subservice'
    )

    new_subservice = fields.Char()

    name = fields.Char(required=True)

    address = fields.Text()

    taluka_id = fields.Many2one(
        'service.taluka',
        string='Taluka'
    )

    phone = fields.Char()
    owner_id = fields.Char(
        string='Owner'
    )
    facility_ids = fields.One2many(
        'provider.facility',
        'service_request_id',
        string='Facilities'
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
    # discount = fields.Float()
    discount_ids = fields.One2many(
        'provider.discount',
        'service_request_id',
        string='Discounts'
    )

    gallery_ids = fields.One2many(
        'provider.gallery',
        'service_request_id',
        string='Gallery'
    )

    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')

    approved_by = fields.Many2one(
        'res.users'
    )

    def action_approve(self):

        for rec in self:

            service = rec.service_id

            if not service and rec.new_service:

                service = self.env[
                    'service.service'
                ].create({
                    'name': rec.new_service
                })

            subservice = rec.subservice_id
            gallery_list = []

            for gallery in rec.gallery_ids:

                gallery_list.append((0, 0, {
                    'image': gallery.image
                }))

            facility_data = []

            for facility in rec.facility_ids:

                facility_data.append((0, 0, {
                    'name': facility.name
                }))
            if not subservice and rec.new_subservice:

                subservice = self.env[
                    'service.subservice'
                ].create({
                    'name': rec.new_subservice,
                    'service_id': service.id
                })

            discount_data = []

            for discount in rec.discount_ids:

                discount_data.append((0, 0, {
                    'name': discount.name
                }))

            self.env[
                'service.detail'
            ].create({

                'name': rec.name,
                'address': rec.address,
                'taluka_id': rec.taluka_id.id if rec.taluka_id else False,
                'phone': rec.phone,
                # 'discount': rec.discount,
                'discount_ids': discount_data,
                'owner_id': rec.owner_id,
                'youtube_link': rec.youtube_link,
                'facebook_link': rec.facebook_link,
                'instagram_link': rec.instagram_link,
                'subservice_id': subservice.id,
                'gallery_ids': gallery_list,
                'facility_ids': facility_data

            })

            rec.write({
                'state': 'approved',
                'approved_by': self.env.user.id
            })

    def action_reject(self):

        self.write({
            'state': 'rejected'
        })