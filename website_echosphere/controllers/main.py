from odoo import http
from odoo.http import request


class EchosphereWebsite(http.Controller):

    @http.route('/', auth='public', website=True)
    def homepage(self, **kwargs):

        services = request.env['service.service'].sudo().search([
            ('active', '=', True)
        ], order='sequence asc')

        popular_services = request.env['service.service'].sudo().search([
            ('is_popular', '=', True),
            ('active', '=', True)
        ])

        featured_providers = request.env['service.detail'].sudo().search([
            ('is_featured', '=', True),
            ('active', '=', True)
        ], limit=8)

        banners = request.env['service.banner'].sudo().search([
            ('active', '=', True)
        ], order='sequence asc')

        news = request.env['service.news'].sudo().search([
            ('active', '=', True)
        ], limit=5)

        website_content = request.env['website.content'].sudo().search([
            ('active', '=', True)
        ], limit=1)

        return request.render(
            'website_echosphere.homepage_template',
            {
                'services': services,
                'popular_services': popular_services,
                'featured_providers': featured_providers,
                'banners': banners,
                'news': news,
                'website_content': website_content,
            }
        )