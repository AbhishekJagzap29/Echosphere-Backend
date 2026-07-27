{
    'name': 'Echosphere Website',
    'version': '17.0.1.0.0',
    'depends': [
        'website',
        'service_hierarchy_module'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/menus.xml',
        # 'views/website_pages.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_echosphere/static/src/css/style.css',
            'website_echosphere/static/src/js/website.js',
        ],
    },
    'installable': True,
    'application': True,
}