# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_ec_sri_status = fields.Selection([
        ('draft', 'Draft (Not Sent)'),
        ('sent', 'Sent to SRI'),
        ('authorized', 'Authorized'),
        ('rejected', 'Rejected'),
    ], string='SRI Status', default='draft', copy=False, index=True)

    l10n_ec_sri_access_key = fields.Char(string='Clave de Acceso', copy=False, size=49)
    l10n_ec_authorization_date = fields.Datetime(string='Authorization Date', copy=False)
    l10n_ec_xml_content = fields.Binary(string='Signed XML', copy=False, attachment=True)
    l10n_ec_sri_error = fields.Text(string='SRI Error Message', copy=False)

    def action_send_sri(self):
        """
        Orchestrator: Key Gen -> XML Gen -> Sign -> Send
        """
        for move in self:
            if move.l10n_ec_sri_status in ['authorized', 'sent']:
                continue

            # 1. Generate Access Key
            if not move.l10n_ec_sri_access_key:
                move.l10n_ec_sri_access_key = self.env['l10n_ec.sri.xml'].generate_access_key(move)

            # 2. Render XML (Placeholder for QWeb call)
            # xml_bytes = self.env['l10n_ec.sri.xml'].render_xml(move)

            # 3. Sign XML
            # signed_xml = self._sign_xml(xml_bytes)

            # 4. Send (Stub for SOAP Service)
            # response = self.env['l10n_ec.sri.service'].send_document(signed_xml)

            # Simulated Success for Scaffold
            move.l10n_ec_sri_status = 'sent'
            move.l10n_ec_authorization_date = datetime.now()

            # Note: In real impl, we handle faults here.

    def action_check_sri(self):
        """
        Ping Check Status service
        """
        for move in self:
            if not move.l10n_ec_sri_access_key:
                raise UserError(_("No Access Key generated yet."))

            # Simulated Check
            move.l10n_ec_sri_status = 'authorized'

    def _sign_xml(self, xml_content):
        """
        Internal helper to call the signer lib.
        """
        self.ensure_one()
        certificate = self.company_id.l10n_ec_certificate_id
        if not certificate:
            raise UserError(_("No active Electronic Signature found for this company."))

        # REAL IMPLEMENTATION
        # Pass the raw XML and the encrypted P12 data to the signer service
        return self.env['l10n_ec.sri.signer'].sign_xml(
            xml_content,
            certificate.content, # Binary field
            certificate.password # Decrypt if needed, here passed as stored
        )
