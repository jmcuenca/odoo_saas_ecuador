# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Reports (ATS)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/Reporting',
    'summary': 'ATS (Anexo Transaccional Simplificado) XML Generation',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'document_id': 'DM-007',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'l10n_ec_base',
        'l10n_ec_edi',
        'l10n_ec_withholding',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ats_template.xml',
        'wizard/l10n_ec_ats_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
