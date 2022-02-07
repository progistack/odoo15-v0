# -*- coding: utf-8 -*-

{
    'name': 'agentis module',
    'version': '15.0.1.0.0',
    'summary': 'automation of email reception in odoo',
    'description': """automation of email reception in odoo""",
    'author': 'progistack',
    'company': 'progistack',
    'maintainer': 'emmanuel.kissi@progistack.com',
    'depends': ['base', 'fetchmail', 'hr_expense'],
    'website': 'https://www.progistack.com',
    'data': [
        'security/ir.model.access.csv',
        'views/mouvement_caise.xml',
        'views/agentis_pga.xml',
        'views/sequence_numero_facture_dga.xml',
        'views/agentis_office_manager.xml',
        'views/agentis_chantier.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
