# -*- coding: utf-8 -*-

{
    'name': 'pos session',
    'version': '15.0.1.0.0',
    'summary': 'montant total de chaque sessions',
    'description': """montant total de chaque session""",
    'author': 'progistack',
    'company': 'progistack',
    'maintainer': 'emmanuel.kissi@progistack.com',
    'depends': ['base', 'point_of_sale'],
    'website': 'https://www.progistack.com',
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_session_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
