# -*- coding: utf-8 -*-
from odoo import models, fields

class L10nEcDriver(models.Model):
    _name = 'l10n_ec.driver'
    _description = 'Transport Driver (Ecuador)'

    name = fields.Char(string='Driver Name', required=True)
    identifier_type = fields.Selection([
        ('cedula', 'Cédula'),
        ('ruc', 'RUC'),
        ('pasaporte', 'Pasaporte')
    ], string='Identifier Type', default='cedula', required=True)

    license_number = fields.Char(string='License Number', required=True, help="Driver's License ID")
    active = fields.Boolean(default=True)
