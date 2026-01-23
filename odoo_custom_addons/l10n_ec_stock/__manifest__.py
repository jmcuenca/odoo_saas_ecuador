# -*- coding: utf-8 -*-
{
    'name': 'Ecuador - Stock & Logistics (Guía de Remisión)',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Localizations',
    'summary': 'Guía de Remisión, Transportistas, Motivos de Traslado',
    'author': 'SomaTech Ecuador (Expert Crew)',
    'document_id': 'DM-004',
    'website': 'https://somatech.ec',
    'license': 'LGPL-3',
    'depends': [
        'l10n_ec_base',
        'l10n_ec_edi',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/l10n_ec_transport_views.xml',
        'data/l10n_ec_stock_data.xml',
        'data/guia_template.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
