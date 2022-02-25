# See LICENSE file for full copyright and licensing details.

{
    "name": "payment Signature",
    "version": "15.0.1.0.0",
    "author": "progistack",
    "maintainer": "emmanuel.kissi@gmail.com",
    "complexity": "easy",
    "depends": ["web", "om_account_accountant", 'hr_expense'],
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
     Ce module fournit la fonctionnalité pour stocker la signature numérique.
    """,
    "summary": """
        L'écran tactile permet à l'utilisateur d'ajouter une signature avec des appareils tactiles.
         La signature numérique peut être très utile pour les documents.
    """,
    "data": [
        "views/accounting_signature_view.xml"],
    "website": "http://www.progistack.com",
    "installable": True,
    "auto_install": False,
    'assets': {
        'web.assets_qweb':[
            'signature_electronic/static/src/xml/digital_sign.xml'],
        'web.assets_backend': [
            'signature_electronic/static/src/js/digital_sign.js'],
    }
}
