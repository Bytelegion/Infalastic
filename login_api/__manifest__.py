# -*- coding: utf-8 -*-
{
    'name': "Login Api's",
    'summary': """Login Api's""",
    'description': """
        Login Api's
    """,
    'author': "Odoo",
    'license': 'LGPL-3',
    'website': "http://www.Odoo.com",
    'version': '15.0.21',
    'depends': ['base','mail','hr'],
    'data': [
        'views/views.xml',
        'views/employee.xml',
        'views/department.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False
}
