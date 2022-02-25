# -*- coding: utf-8 -*-

{
    'name': 'automatise received email',
    'version': '15.0.1.0.0',
    'summary': 'automation of email reception in odoo',
    'description': """automation of email reception in odoo""",
    'author': 'progistack',
    'company': 'progistack',
    'maintainer': 'emmanuel.kissi@progistack.com',
    'depends': ['base', 'fetchmail'],
    'website': 'https://www.progistack.com',
    'data': [
        #'security/ir.model.access.csv',
        'data/email.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
