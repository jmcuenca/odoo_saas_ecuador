# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.l10n_ec_edi.models.access_key import AccessKey

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_ec_sri_access_key = fields.Char(string="SRI Access Key", copy=False, help="49-digit Clave de Acceso")
    l10n_ec_sri_status = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('sent', 'Sent'),
        ('authorized', 'Authorized'),
        ('rejected', 'Rejected'),
    ], string="SRI Status", default='draft', copy=False, index=True)
    l10n_ec_xml_data = fields.Binary("Signed XML", attachment=True, copy=False)
    l10n_ec_sri_response = fields.Text("SRI Response", copy=False)

    # 2026 Mandate: No cancellation of Consumidor Final
    def button_cancel_sri(self):
        for move in self:
            if move.l10n_ec_sri_status == 'authorized':
                # Check for Consumidor Final Rule
                if move.partner_id.vat == '9999999999999':
                     raise UserError(_("SRI 2026 Rule: Cannot cancel Authorized invoices for Consumidor Final."))
        return super(AccountMove, self).button_cancel() # Standard cancel logic needs review

    def _generate_access_key(self):
        for move in self:
            # Only for Ecuador
            if move.company_id.country_id.code != 'EC':
                continue

            # Use AccessKey helper
            company = move.company_id
             # Environment: 1=Test, 2=Prod
            env = '2' if company.l10n_ec_sri_environment == 'production' else '1'
             # TODO: Get establishment/emission point from Journal
            estab = '001'
            pto = '001'
            seq = move.name.split('/')[-1] if '/' in move.name else move.name[-9:] # Simple logic, needs refinement

            key = AccessKey.generate(
                invoice_date=move.invoice_date,
                doc_type=move.l10n_latam_document_type_id.code,
                ruc=company.vat,
                environment=env,
                establishment=estab,
                emission_point=pto,
                sequential=seq
            )
            move.l10n_ec_sri_access_key = key

