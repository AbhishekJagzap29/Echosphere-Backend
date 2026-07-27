from odoo import http
from odoo.http import request, Response
import json
import logging
import base64
import random

_logger = logging.getLogger(__name__)

class ServiceAPI(http.Controller):

    # =====================================================
    # LOGIN API
    # =====================================================
    @http.route(
        '/api/login',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False,
        cors='*'
    )
    def login(self):

        try:
            data = json.loads(request.httprequest.data)

            login = data.get("login")
            password = data.get("password")

            # =========================
            # VALIDATION
            # =========================
            if not login or not password:

                missing = []

                if not login:
                    missing.append("login")

                if not password:
                    missing.append("password")

                return Response(
                    json.dumps({
                        'status': 'FAILED',
                        'message': f"Missing fields: {', '.join(missing)}"
                    }),
                    content_type='application/json',
                    status=400
                )

            # =========================
            # AUTHENTICATION
            # =========================
            uid = request.session.authenticate(
                request.env.cr.dbname,
                login,
                password
            )

            if not uid:

                return Response(
                    json.dumps({
                        'status': 'FAILED',
                        'message': 'Invalid login or password'
                    }),
                    content_type='application/json',
                    status=401
                )

            user = request.env['res.users'].sudo().browse(uid)

            # =========================
            # SUCCESS RESPONSE
            # =========================
            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Login successful',
                    'user_id': user.id,
                    'name': user.name,
                    'login': user.login,
                    'session_id': request.session.sid
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            _logger.error(str(e))

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )
        
    # =====================================================
    # GET ALL SERVICES
    # =====================================================
    @http.route('/api/services', type='http', auth='public', methods=['GET'], csrf=False)
    def get_services(self, **kwargs):

        services = request.env['service.service'].sudo().search([])

        data = []

        for service in services:
            data.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
            })

        return request.make_response(
            json.dumps({
                'status': 'success',
                'data': data
            }),
            headers=[('Content-Type', 'application/json')]
        )
    
    # =====================================================
    # CREATE SERVICE
    # =====================================================
    @http.route('/api/create_service', type='json', auth='public', methods=['POST'], csrf=False)
    def create_service(self, **kwargs):

        name = kwargs.get('name')
        description = kwargs.get('description')

        if not name:
            return {
                'status': 'FAILED',
                'message': 'Name is required'
            }

        service = request.env['service.service'].sudo().create({
            'name': name,
            'description': description,
        })

        return {
            'status': 'SUCCESS',
            'message': 'Service Created Successfully',
            'service_id': service.id
        }
    
    # =====================================================
    # GET SUBSERVICES
    # =====================================================
    @http.route('/api/services', type='http', auth='public',
                methods=['GET'], csrf=False, cors='*')
    def get_services(self):

        try:

            services = request.env['service.service'].sudo().search([])

            data = []

            for service in services:
                data.append({
                    'id': service.id,
                    'name': service.name,
                    'description': service.description,
                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    # =====================================================
    # CREATE SUBSERVICE
    # =====================================================
    @http.route('/api/create_subservice', type='http',
                auth='public', methods=['POST'],
                csrf=False, cors='*')
    def create_subservice(self):

        try:
            data = json.loads(request.httprequest.data)

            name = data.get('name')
            service_id = data.get('service_id')

            if not name or not service_id:
                return Response(
                    json.dumps({
                        'status': 'FAILED',
                        'message': 'Name and service_id required'
                    }),
                    content_type='application/json',
                    status=400
                )

            subservice = request.env['service.subservice'].sudo().create({
                'name': name,
                'service_id': service_id
            })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Subservice created successfully',
                    'subservice_id': subservice.id
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    # =====================================================
    # GET SUBSERVICES
    # =====================================================
    @http.route('/api/subservices', type='http',
                auth='public', methods=['GET'],
                csrf=False, cors='*')
    def get_subservices(self, **kwargs):

        try:

            service_id = kwargs.get('service_id')

            domain = []

            if service_id:
                domain.append(('service_id', '=', int(service_id)))

            subservices = request.env['service.subservice'].sudo().search(domain)

            data = []

            for subservice in subservices:
                data.append({
                    'id': subservice.id,
                    'name': subservice.name,
                    'service_id': subservice.service_id.id,
                    'service_name': subservice.service_id.name,
                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    # =====================================================
    # CREATE SERVICE DETAIL
    # =====================================================
    @http.route('/api/create_service_detail', type='http',
                auth='public', methods=['POST'],
                csrf=False, cors='*')
    def create_service_detail(self):

        try:
            data = json.loads(request.httprequest.data)

            name = data.get('name')
            address = data.get('address')
            phone = data.get('phone')
            discount = data.get('discount')
            subservice_id = data.get('subservice_id')
            image = data.get('image')

            if not name or not subservice_id:
                return Response(
                    json.dumps({
                        'status': 'FAILED',
                        'message': 'Name and subservice_id required'
                    }),
                    content_type='application/json',
                    status=400
                )

            detail = request.env['service.detail'].sudo().create({
                'name': name,
                'address': address,
                'phone': phone,
                'discount': discount,
                'subservice_id': subservice_id,
                'image': image
            })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Service detail created successfully',
                    'detail_id': detail.id
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    # =====================================================
    # GET SERVICE DETAILS
    # =====================================================
    # @http.route('/api/service_details', type='http',
    #             auth='public', methods=['GET'],
    #             csrf=False, cors='*')
    # def get_service_details(self, **kwargs):

    #     try:

    #         subservice_id = kwargs.get('subservice_id')

    #         domain = []

    #         if subservice_id:
    #             domain.append(('subservice_id', '=', int(subservice_id)))

    #         details = request.env['service.detail'].sudo().search(domain)

    #         data = []

    #         for detail in details:
    #             data.append({
    #                 'id': detail.id,
    #                 'name': detail.name,
    #                 'address': detail.address,
    #                 'phone': detail.phone,
    #                 'discount': detail.discount,
    #                 'subservice_id': detail.subservice_id.id,
    #                 'subservice_name': detail.subservice_id.name,
    #                 'image': detail.image.decode() if detail.image else False,
    #                 'youtube_link': detail.youtube_link,
    #                 'facebook_link': detail.facebook_link,
    #                 'instagram_link': detail.instagram_link,
    #             })

    #         return Response(
    #             json.dumps({
    #                 'status': 'SUCCESS',
    #                 'data': data
    #             }),
    #             content_type='application/json',
    #             status=200
    #         )

    #     except Exception as e:

    #         return Response(
    #             json.dumps({
    #                 'status': 'ERROR',
    #                 'message': str(e)
    #             }),
    #             content_type='application/json',
    #             status=500
    #         )

    @http.route('/api/service_details',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def get_service_details(self, **kwargs):

        try:

            subservice_id = kwargs.get('subservice_id')
            taluka_id = kwargs.get('taluka_id')
            detail_id = kwargs.get('detail_id')

            domain = [('active', '=', True)]

            if detail_id:

                domain.append((
                    'id',
                    '=',
                    int(detail_id)
                ))

            # -------------------------
            # SUBSERVICE FILTER
            # -------------------------
            if subservice_id:

                domain.append((
                    'subservice_id',
                    '=',
                    int(subservice_id)
                ))

            # -------------------------
            # TALUKA FILTER
            # -------------------------
            if taluka_id:

                domain.append((
                    'taluka_id',
                    '=',
                    int(taluka_id)
                ))

            details = request.env[
                'service.detail'
            ].sudo().search(domain)

            data = []

            for detail in details:

                data.append({
                    'id': detail.id,
                    'name': detail.name,
                    'address': detail.address,
                    'phone': detail.phone,
                    # 'discount': detail.discount,
                    'discounts': [
                        discount.name
                        for discount in detail.discount_ids
                    ],
                    'subservice_id':
                        detail.subservice_id.id,
                    'subservice_name':
                        detail.subservice_id.name,
                    'taluka_id':
                        detail.taluka_id.id
                        if detail.taluka_id else False,
                    'taluka_name':
                        detail.taluka_id.name
                        if detail.taluka_id else False,
                    'owner_id':
                        detail.owner_id,
                    'whatsapp':
                        detail.whatsapp,
                    'email':
                        detail.email,
                    'website':
                        detail.website,
                    'rating':
                        detail.rating,
                    'review_count':
                        detail.review_count,
                    'district':
                        detail.district,
                    'state':
                        detail.state,
                    'pincode':
                        detail.pincode,
                    'is_featured':
                        detail.is_featured,
                    'is_verified':
                        detail.is_verified,
                    'open_24_hours':
                        detail.open_24_hours,
                    'youtube_link':
                        detail.youtube_link,
                    'facebook_link':
                        detail.facebook_link,
                    'instagram_link':
                        detail.instagram_link,
                    'gallery_images': [
                        gallery.image.decode()
                        if gallery.image else False
                        for gallery in detail.gallery_ids
                    ],
                    'facilities': [
                        facility.name
                        for facility in detail.facility_ids
                    ],

                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )
        
    @http.route('/api/popular_services',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def popular_services(self):

        try:

            services = request.env[
                'service.service'
            ].sudo().search([

                ('is_popular', '=', True),
                ('active', '=', True)

            ], order='sequence asc')

            data = []

            for service in services:

                # --------------------------------
                # FIND SUBSERVICES
                # --------------------------------
                subservices = request.env[
                    'service.subservice'
                ].sudo().search([

                    ('service_id', '=', service.id)

                ])

                # --------------------------------
                # FIND DETAIL WITH GALLERY
                # --------------------------------
                detail = request.env[
                    'service.detail'
                ].sudo().search([

                    ('subservice_id', 'in', subservices.ids),
                    ('gallery_ids', '!=', False)

                ], limit=1, order='id desc')

                image = False

                # --------------------------------
                # GET FIRST GALLERY IMAGE
                # --------------------------------
                if detail and detail.gallery_ids:

                    first_image = detail.gallery_ids[0]

                    if first_image.image:

                        image = first_image.image.decode()

                data.append({

                    'id':
                        service.id,

                    'name':
                        service.name,

                    'description':
                        service.description,

                    'image':
                        image,

                })

            return Response(
                json.dumps({

                    'status': 'SUCCESS',

                    'data':
                        data

                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({

                    'status': 'ERROR',

                    'message':
                        str(e)

                }),
                content_type='application/json',
                status=500
            )
        
    @http.route('/api/other_services',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def other_services(self):

        try:

            services = request.env[
                'service.service'
            ].sudo().search([

                ('is_popular', '=', False),
                ('active', '=', True)

            ], order='sequence asc')

            data = []

            for service in services:

                # --------------------------------
                # FIND SUBSERVICES
                # --------------------------------
                subservices = request.env[
                    'service.subservice'
                ].sudo().search([

                    ('service_id', '=', service.id)

                ])

                # --------------------------------
                # FIND DETAILS WITH GALLERY
                # --------------------------------
                details = request.env[
                    'service.detail'
                ].sudo().search([

                    ('subservice_id', 'in', subservices.ids),
                    ('gallery_ids', '!=', False)

                ])

                detail = details and random.choice(details) or False

                image = False

                # --------------------------------
                # RANDOM GALLERY IMAGE
                # --------------------------------
                if detail and detail.gallery_ids:

                    random_gallery = random.choice(
                        detail.gallery_ids
                    )

                    if random_gallery.image:

                        image = random_gallery.image.decode()

                data.append({

                    'id':
                        service.id,

                    'name':
                        service.name,

                    'description':
                        service.description,

                    'image':
                        image,

                })

            return Response(
                json.dumps({

                    'status': 'SUCCESS',

                    'data':
                        data

                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({

                    'status': 'ERROR',

                    'message':
                        str(e)

                }),
                content_type='application/json',
                status=500
            )

    @http.route('/api/banners',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def get_banners(self):

        try:

            banners = request.env['service.banner'].sudo().search([
                ('active', '=', True)
            ], order='sequence asc, id desc')

            data = []

            for banner in banners:

                data.append({
                    'id': banner.id,
                    'title': banner.title,
                    'image': banner.image.decode() if banner.image else False,
                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    @http.route('/api/news',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def get_news(self):

        try:

            news_items = request.env['service.news'].sudo().search([
                ('active', '=', True)
            ], order='date desc, id desc')

            data = []

            for news in news_items:

                data.append({
                    'id': news.id,
                    'title': news.title,
                    'description': news.description,
                    'date': news.date.isoformat() if news.date else False,
                    'image': news.image.decode() if news.image else False,
                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )
        
    @http.route('/api/talukas',
                type='http',
                auth='public',
                methods=['GET'],
                csrf=False,
                cors='*')
    def get_talukas(self):

        try:

            talukas = request.env[
                'service.taluka'
            ].sudo().search([
                ('active', '=', True)
            ])

            data = []

            for taluka in talukas:

                data.append({
                    'id': taluka.id,
                    'name': taluka.name
                })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'data': data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )
        
    @http.route('/api/register_customer',
                type='json',
                auth='public',
                methods=['POST'],
                csrf=False,
                cors='*')
    def register_customer(self, **kwargs):

        try:

            data = json.loads(request.httprequest.data)

            name = data.get('name')
            phone = data.get('phone')
            taluka_id = data.get('taluka_id')
            is_card_holder = data.get('is_card_holder')

            # Validation
            if not name:
                return {
                    'status': 'ERROR',
                    'message': 'Name is required'
                }

            if not phone:
                return {
                    'status': 'ERROR',
                    'message': 'Phone number is required'
                }

            customer = request.env[
                'service.customer'
            ].sudo().create({

                'name': name,
                'phone': phone,
                'taluka_id': taluka_id,
                'is_card_holder': is_card_holder,

            })

            return {
                'status': 'SUCCESS',
                'message': 'Customer Registered Successfully',
                'customer_id': customer.id
            }

        except Exception as e:

            return {
                'status': 'ERROR',
                'message': str(e)
            }
        
    # @http.route('/api/create_service_request',
    #             type='http',
    #             auth='public',
    #             methods=['POST'],
    #             csrf=False,
    #             cors='*')
    # def create_service_request(self):

    #     try:

    #         data = json.loads(request.httprequest.data)

    #         request_rec = request.env[
    #             'service.request'
    #         ].sudo().create({

    #             'service_id': data.get('service_id'),
    #             'new_service': data.get('new_service'),

    #             'subservice_id': data.get('subservice_id'),
    #             'new_subservice': data.get('new_subservice'),

    #             'name': data.get('name'),
    #             'address': data.get('address'),
    #             'phone': data.get('phone'),
    #             'discount': data.get('discount'),
    #             'image': data.get('image'),

    #         })

    #         return Response(
    #             json.dumps({
    #                 'status': 'SUCCESS',
    #                 'message': 'Request Submitted Successfully',
    #                 'request_id': request_rec.id
    #             }),
    #             content_type='application/json',
    #             status=200
    #         )

    #     except Exception as e:

    #         return Response(
    #             json.dumps({
    #                 'status': 'ERROR',
    #                 'message': str(e)
    #             }),
    #             content_type='application/json',
    #             status=500
    #         )

    @http.route('/api/create_service_request',
                type='http',
                auth='user',
                methods=['POST'],
                csrf=False,
                cors='*')
    def create_service_request(self):

        try:

            raw_data = request.httprequest.data
            data = json.loads(raw_data.decode('utf-8')) if raw_data else {}

            service_name = data.get('service')
            subservice_name = data.get('subservice')

            # -----------------------------
            # TALUKA ID (SAFE CONVERSION)
            # -----------------------------
            taluka_id = False
            raw_taluka = data.get('taluka_id')
            if raw_taluka not in (None, False, '', 'null'):
                try:
                    taluka_id = int(raw_taluka)
                except (ValueError, TypeError):
                    taluka_id = False

            # -----------------------------
            # SERVICE
            # -----------------------------
            service = False
            if service_name and isinstance(service_name, str):
                service = request.env[
                    'service.service'
                ].sudo().search([
                    ('name', '=ilike', service_name.strip())
                ], limit=1)

            # -----------------------------
            # SUBSERVICE
            # -----------------------------
            subservice = False

            if service and subservice_name and isinstance(subservice_name, str):

                subservice = request.env[
                    'service.subservice'
                ].sudo().search([
                    ('name', '=ilike', subservice_name.strip()),
                    ('service_id', '=', service.id)
                ], limit=1)

            # -----------------------------
            # GALLERY IMAGES
            # -----------------------------
            gallery_list = []
            for img in data.get('gallery_images', []):
                if img:
                    gallery_list.append((0, 0, {
                        'image': img
                    }))

            facility_list = []
            for facility in data.get('facilities', []):
                if facility:
                    facility_list.append((0, 0, {
                        'name': facility
                    }))

            discount_list = []
            for discount in data.get('discounts', []):
                if discount:
                    discount_list.append((0, 0, {
                        'name': discount
                    }))

            # -----------------------------
            # CREATE REQUEST
            # -----------------------------
            request_rec = request.env[
                'service.request'
            ].sudo().create({
                'executive_id': request.env.user.id,
                'service_id':
                    service.id if service else False,
                'new_service':
                    False if service else service_name,
                'subservice_id':
                    subservice.id if subservice else False,
                'new_subservice':
                    False if subservice else subservice_name,
                'name': data.get('name'),
                'address': data.get('address'),
                'taluka_id': taluka_id,
                'phone': data.get('phone'),
                'owner_id': data.get('owner_id'),
                'discount_ids': discount_list,
                'youtube_link': data.get('youtube_link'),
                'facebook_link': data.get('facebook_link'),
                'instagram_link': data.get('instagram_link'),
                'gallery_ids': gallery_list,
                'facility_ids': facility_list,
            })

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Request Submitted Successfully',
                    'request_id': request_rec.id
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    @http.route('/api/approve_request',
                type='http',
                auth='user',
                methods=['POST'],
                csrf=False,
                cors='*')
    def approve_request(self):

        try:

            data = json.loads(request.httprequest.data)

            request_id = data.get('request_id')

            if not request_id:

                return Response(
                    json.dumps({
                        'status': 'ERROR',
                        'message': 'request_id is required'
                    }),
                    content_type='application/json',
                    status=400
                )

            service_request = request.env[
                'service.request'
            ].sudo().browse(int(request_id))

            if not service_request.exists():

                return Response(
                    json.dumps({
                        'status': 'ERROR',
                        'message': 'Request not found'
                    }),
                    content_type='application/json',
                    status=404
                )

            service_request.action_approve()

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Request Approved Successfully'
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    @http.route('/api/reject_request',
                type='http',
                auth='user',
                methods=['POST'],
                csrf=False,
                cors='*')
    def reject_request(self):

        try:

            data = json.loads(request.httprequest.data)

            request_id = data.get('request_id')

            if not request_id:

                return Response(
                    json.dumps({
                        'status': 'ERROR',
                        'message': 'request_id is required'
                    }),
                    content_type='application/json',
                    status=400
                )

            service_request = request.env[
                'service.request'
            ].sudo().browse(int(request_id))

            if not service_request.exists():

                return Response(
                    json.dumps({
                        'status': 'ERROR',
                        'message': 'Request not found'
                    }),
                    content_type='application/json',
                    status=404
                )

            service_request.action_reject()

            return Response(
                json.dumps({
                    'status': 'SUCCESS',
                    'message': 'Request Rejected Successfully'
                }),
                content_type='application/json',
                status=200
            )

        except Exception as e:

            return Response(
                json.dumps({
                    'status': 'ERROR',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )
