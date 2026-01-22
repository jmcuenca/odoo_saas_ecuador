# -*- coding: utf-8 -*-
# Part of Universal Odoo MCP System. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ecuador SRI Electronic Invoicing (U-OMS)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/SRI',
    'summary': 'Full SRI Electronic Invoicing Compliance (2025-2026)',
    'author': 'Universal Odoo MCP System',
    'website': 'https://github.com/universal-odoo-mcp',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_ec',  # Base EC Chart of Accounts
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/account.tax.group.csv',
        'data/account.account.template.csv',
        'data/account.tax.template.csv',
        'data/l10n_ec_chart_data.xml',
        'data/sri_error_codes.xml',
        'data/cron_jobs.xml',
        'data/ir_sequence_data.xml',
        'views/menus.xml',
        'views/res_company_views.xml',
        'views/certificate_views.xml',
        'views/account_move_views.xml',
        'views/account_move_purchase_views.xml',
        'views/l10n_ec_retention_views.xml',
        'views/l10n_ec_retention_xml_template.xml',
        'report/report_ride.xml',
    ],
    'assets': {
        'web.assets_backend': [
             # Future: Add status badges styling if needed
        ],
    },
    'external_dependencies': {
        'python': ['zeep', 'cryptography', 'lxml'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
