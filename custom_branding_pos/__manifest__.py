{
    'name': 'Custom Branding',
    'version': '17.0.1.0.0',
    'author': 'Dreamwarez',
    'website': 'https://dreamwarez.com',
    'license': 'LGPL-3',
    'depends': ['web'],
    'data': ['static/src/xml/custom_template.xml',
             'views/custom_favicon.xml',
             'views/login_title.xml',
             ],
    
    'assets': {
        'web.assets_backend': [
            "custom_branding_pos/static/src/js/early_title_fix.js",
            'custom_branding_pos/static/src/js/custom_title.js',
            'custom_branding_pos/static/src/js/hide_mail_odoo_title.js',
            # 'custom_branding_pos/static/src/js/custom_content.js',
        ],
        'point_of_sale._assets_pos': [
            'custom_branding_pos/static/src/css/pos_logo_fix.css',
            'custom_branding_pos/static/src/js/pos_brand_force.js',
            'custom_branding_pos/static/src/js/pos_custom_logo.js',
        ],
        'web.assets_qweb': [
            'custom_branding_pos/static/src/xml/pos_brand_force.xml',
            'custom_branding_pos/static/src/xml/pos_direct_brand.xml',
            'custom_branding_pos/static/src/xml/pos_custom_logo.xml',
        ],
    },      
    'installable': True,
    'auto_install': False,
}