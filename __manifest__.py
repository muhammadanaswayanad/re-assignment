{
    'name': 'Lead Re-assignment',
    'version': '1.0',
    'summary': 'Allow users to reassign leads to another salesperson',
    'description': 'Allow users in the "Sales / Own Documents Only" group to reassign leads to another salesperson using a wizard',
    'category': 'Sales/CRM',
    'author': 'Odoo Developer',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_lead_reassign_views.xml',  # Put wizard views BEFORE crm_lead_views.xml
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
