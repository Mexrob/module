# -*- coding: utf-8 -*-
{
    "name": "Website Custom",

    'summary': """
        Personalizacion Sitio web""",

    'description': """
        Agregamos medidas a los productos en el sitio web al momento de cotizar. 
    """,

    'author': "Diego",
    'website': "",
    'version': '0.1',

    'depends': ['website', 'website_sale'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_custom/static/src/css/*',
            'website_custom/static/src/js/product.js',
        ],
    },
}
