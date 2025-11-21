# -*- coding: utf-8 -*-

{
    'name': "SD Clinic",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://giladoo.com/sd_clinic",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sd_projects' ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/prescriptions_views.xml',
        'views/inventory_views.xml',
        'views/patients_views.xml',
        'data/ir_sequence.xml',
        'data/medicine_types_data.xml',
        'data/therapy_types_data.xml',

        ],
    'assets': {
        'web._assets_common_scripts': [
        ],
        'web._assets_common_styles': [
        ],
        'web.assets_qweb': [

        ],
        'web.assets_backend': [

        ],
        'web.assets_frontend': [

        ],
        'web.report_assets_pdf': [

        ],
        },
    'images': [
        'static/src/img/user_avatar_100.png',
    ],
    'license': 'LGPL-3',
}




