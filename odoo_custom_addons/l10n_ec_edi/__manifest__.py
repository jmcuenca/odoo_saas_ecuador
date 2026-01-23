# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Electronic Invoicing (SRI 2026)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Electronic Invoicing, XAdES-BES Signing, and SRI Transmission (Ficha 2.32)',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'l10n_ec_base',
        'account_edi',
    ],
    'data': [
        'security/ir.model.access.csv',


        'views/l10n_ec_certificate_views.xml',
    ],
    'external_dependencies': {
        'python': ['zeep', 'cryptography', 'lxml', 'requests'],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
