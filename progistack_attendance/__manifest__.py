# -*- coding: utf-8 -*-

{
    'name': 'Biometric Integration',
    'version': '1.0',
    'summary': """Integrating Biometric Device  With HR Attendance (Face + Thumb)""",
    'description': """This module integrates Odoo with the biometric device,odoo15,odoo,hr,attendance""",
    'category': 'Generic Modules/Human Resources',
    'author': 'progistack, emmanuelprogistack',
    'company': 'progistack',
    'website': "https://www.progistack.com",
    'depends': ['base_setup', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/date_modification_wizard.xml',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        'views/parametrage_view.xml',
        'data/download_data.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
