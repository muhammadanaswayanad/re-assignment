{
    'name': 'CRM Lead Reassignment',
    'version': '1.0',
    'summary': 'Allows salespeople to reassign leads',
    'description': """
        This module allows users in the "Sales / Own Documents Only" group
        to reassign a lead to another salesperson even if they don't have
        direct access to that lead.
    """,
    'category': 'Sales/CRM',
    'author': 'Odoo Developer',
    'website': '',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/lead_reassignment_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
