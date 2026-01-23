# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Withholding Management (Retenciones)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Vendor Bill Withholding, SRI Authorization, 5-Day Rule',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'l10n_ec_base',
        'l10n_ec_edi',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_ec_withholding.xml',
        'data/retention_template.xml',
        'views/account_retention_views.xml',
        'wizard/retention_wizard_views.xml',
        'views/account_move_views_fixed.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
