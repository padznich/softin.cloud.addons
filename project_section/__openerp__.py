# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################
{
    'name': 'Project Sections',
    'version': '1.0.0',
    'category': 'Projects & Services',
    'sequence': 15,
    'summary': '',
    'description': """
Project Sections
==================
Add project sections
    """,
    'author':  'ShEV',
    'website': 'www',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'project',
        'decimal_precision',
    ],
    'data': [
        'project_view.xml',
        'project_data.xml',
#        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}