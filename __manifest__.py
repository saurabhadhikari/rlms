# -*- coding: utf-8 -*-
{
    'name': "stream",

    'summary': """
        Recommends url of the related subjects materials, an easy tool for learning further.""",

    'description': """
        The module extends subject management of openeducat and shows web links as recommendation.
    """,

    'author': "Saurabh Adhikari",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','openeducat_core'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/stream_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'views/stream_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}