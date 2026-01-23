# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Base Localization (NEC 2026)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Chart of Accounts, Tax Templates, and Identity Validation (SRI 2026)',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_latam_invoice_document',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_latam.document.type.csv',
        'data/account.tax.group.csv',
        'data/account.account.template.csv',
        'data/account.tax.template.csv',
        'data/l10n_ec_chart_data.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
