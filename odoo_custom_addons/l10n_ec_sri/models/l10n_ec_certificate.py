# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64

class L10nEcCertificate(models.Model):
    _name = 'l10n_ec.certificate'
    _description = 'Ecuadorian Digital Signature (SRI)'
    _check_company_auto = True

    name = fields.Char(string='Name', required=True, help='Friendly name, e.g. "Firma 2026"')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    # Store P12 content
    content = fields.Binary(string='Certificate File (.p12)', required=True, attachment=True)
    password = fields.Char(string='Password', required=True, help='Password for the .p12 file')

    expiration_date = fields.Date(string='Expiration Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], default='draft', string='Status')

    def action_validate(self):
        """
        Validate the certificate using cryptography library.
        Checking password and expiration.
        """
        for record in self:
            # TODO: Implement cryptography validation logic here
            # For now, we simulate validation
            if not record.content:
                raise ValidationError(_("Please upload a .p12 file"))

            # Simulated check
            record.state = 'active'

    _sql_constraints = [
        ('uniq_name_company', 'unique(name, company_id)', 'Certificate name must be unique per company'),
    ]
