# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Point of Sale (Electronic Invoicing)',
    'version': '18.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'SRI Electronic Invoicing for POS',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'document_id': 'SRS-08',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'l10n_ec_edi',
    ],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'l10n_ec_pos/static/src/js/**/*',
            'l10n_ec_pos/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
