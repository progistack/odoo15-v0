# -*- coding: utf-8 -*-
{
    'name': "action automatisé",

    'summary': """
    action automatisé
        """,

    'description': """
       automatisé les actions dans odoo
    """,

    'author': "emmanuel.kissi@progistack.com",
    'website': "http://www.progistack.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/negative_quantity.xml',
        'views/negative_quantity_view.xml'

    ],
    'assets': {

        'web.assets_backend': [

        ],
        'web.assets_qweb': [

        ]
    },
    'demo': [

    ],
}
