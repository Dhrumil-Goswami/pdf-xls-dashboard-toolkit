# -*- coding: utf-8 -*-q
{
    'name': "Account Move Report",
    'summary': " Account Move Report",
    'description': "Account Move Report",
    'author': "Logicloop",
    'website': "",
    'category': 'Account',
    'version': '14.0.1.0.0',
    'depends': ['website', 'account',
                'purchase',
                'web',
                'portal',
                'sale_management'
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data_url.xml',
        'report/pfs.xml',
        'report/template_pfs.xml',
        'report/purchase_order_report_inherit.xml',
        'wizard/wizard_account_move_report.xml',
        'views/assets.xml',
        'views/booking_form.xml',
        'views/sale_order_view.xml',
    ],
    'application': True,
}
