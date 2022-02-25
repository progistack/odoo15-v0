# -*- coding: utf-8 -*-

{
    'name': "ecommerce SMS",
    'version': '15.0.1.0.0',
    'summary': """ sends text messages to customers after ordering on the e-commerce site""",
    'description': """sends text messages to customers after ordering on the e-commerce site""",
    'author': 'progistack',
    'company': 'progistack',
    'maintainer': 'emmanuel.kissi@progistack.com',
    'website': "https://www.progistack.com",
    'category': 'Tools',
    'depends': ['contacts', 'sms', 'sale'],
    'data': [
        #'views/sms_template.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}