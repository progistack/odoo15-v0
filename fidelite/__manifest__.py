# -*- coding: utf-8 -*-
{
    'name': "programme_fidelite",

    'summary': """
    fidelite programme
        """,

    'description': """
        programme de fidelité
    """,

    'author': "emmanuel.kissi@progistack.com",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/programme_fidelite_view.xml',
        #'views/pos_template.xml',
        'views/loyalty_field.xml'

    ],
    'assets': {

        'web.assets_backend': [
            'fidelite/static/src/js/reward_button.js',
            'fidelite/static/src/js/loyalty_field.js',
            'fidelite/static/src/js/save_user_info.js',
            'fidelite/static/src/js/models.js',
            'fidelite/static/src/js/loyalty_operation.js',
            'fidelite/static/src/js/select_customer.js',
            'fidelite/static/src/js/ticket_screen_point.js',
            'fidelite/static/src/js/quotation_order.js',
            'fidelite/static/src/js/quatation_order_select.js',
        ],
        'web.assets_qweb': [
            'fidelite/static/src/xml/reward_button.xml',
            'fidelite/static/src/xml/loyalty_field1.xml',
            'fidelite/static/src/xml/show_loyalty_popup.xml',
            'fidelite/static/src/xml/loyalty_receipt.xml',
            'fidelite/static/src/xml/select_customer.xml',
            'fidelite/static/src/xml/override_back_btn.xml',
            'fidelite/static/src/xml/payment_screen.xml',

        ]
    },
    'demo': [

    ],
}
