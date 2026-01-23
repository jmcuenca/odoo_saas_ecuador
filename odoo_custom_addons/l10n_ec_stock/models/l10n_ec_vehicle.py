# -*- coding: utf-8 -*-
from odoo import models, fields

class L10nEcVehicle(models.Model):
    _name = 'l10n_ec.vehicle'
    _description = 'Transport Vehicle (Ecuador)'

    name = fields.Char(string='Vehicle Name', required=True, help="e.g., Truck 01")
    license_plate = fields.Char(string='License Plate', required=True, help="e.g., ABC-1234")
    model = fields.Char(string='Model')
    brand = fields.Char(string='Brand')
    active = fields.Boolean(default=True)
