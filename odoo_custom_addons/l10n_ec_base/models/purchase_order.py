# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Copyright 2026 Somatech.dev
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
#
# DE 045-2025: Penalty Calculation for Late Deliveries
# =====================================================
# ALL regulatory values are configurable via ir.config_parameter
# NO HARDCODED DEFAULTS - System must be properly configured.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class PurchaseOrder(models.Model):
    """
    Extends purchase.order with Ecuador penalty calculation per DE 045-2025.

    Regulatory Reference:
    - Decreto Ejecutivo 045-2025: Penalidad diaria por retrasos
    - Applies to government contracts

    Configuration Parameters (ir.config_parameter):
    - l10n_ec.penalty_rate_daily: Daily penalty rate (e.g., 2.0 for 2%)
    - l10n_ec.penalty_cap_percent: Maximum penalty cap (e.g., 10.0 for 10%)
    """
    _inherit = 'purchase.order'

    # =========================================================================
    # DE 045-2025: Daily Penalty Fields
    # =========================================================================
    l10n_ec_expected_delivery_date = fields.Date(
        string="Fecha Entrega Prevista",
        help="Fecha contractual de entrega (DE 045-2025)"
    )
    l10n_ec_actual_delivery_date = fields.Date(
        string="Fecha Entrega Real",
        help="Fecha real de entrega del pedido"
    )
    l10n_ec_delay_days = fields.Integer(
        string="Días de Retraso",
        compute="_compute_penalty",
        store=True,
        help="Días de retraso en la entrega"
    )
    l10n_ec_penalty_amount = fields.Monetary(
        string="Monto Penalidad",
        compute="_compute_penalty",
        store=True,
        currency_field='currency_id',
        help="Penalidad calculada por retraso"
    )
    l10n_ec_penalty_capped = fields.Boolean(
        string="Penalidad Limitada",
        compute="_compute_penalty",
        store=True,
        help="Indica si la penalidad alcanzó el límite máximo"
    )
    l10n_ec_is_government_contract = fields.Boolean(
        string="Contrato Gubernamental",
        related='partner_id.l10n_ec_government_contractor',
        store=True,
        help="Se aplica régimen de penalidades DE 045-2025"
    )

    # =========================================================================
    # CONFIGURATION HELPERS - No hardcoded values
    # =========================================================================

    def _get_penalty_rate(self):
        """Get daily penalty rate from configuration."""
        param = self.env['ir.config_parameter'].sudo().get_param(
            'l10n_ec.penalty_rate_daily'
        )
        if not param:
            raise ValidationError(_(
                "Missing configuration: l10n_ec.penalty_rate_daily\n"
                "DE 045-2025 requires penalty rate configuration.\n"
                "Please configure System Parameters."
            ))
        return float(param)

    def _get_penalty_cap(self):
        """Get penalty cap percentage from configuration."""
        param = self.env['ir.config_parameter'].sudo().get_param(
            'l10n_ec.penalty_cap_percent'
        )
        if not param:
            raise ValidationError(_(
                "Missing configuration: l10n_ec.penalty_cap_percent\n"
                "DE 045-2025 requires penalty cap configuration.\n"
                "Please configure System Parameters."
            ))
        return float(param)

    @api.depends(
        'l10n_ec_expected_delivery_date',
        'l10n_ec_actual_delivery_date',
        'amount_total',
    )
    def _compute_penalty(self):
        """
        Computes delay days and penalty amount per DE 045-2025.

        Formula: penalty = amount_total * (penalty_rate/100) * delay_days
        Cap: Configurable maximum percentage of total

        All values from ir.config_parameter - NO HARDCODED DEFAULTS
        """
        for order in self:
            order.l10n_ec_delay_days = 0
            order.l10n_ec_penalty_amount = 0.0
            order.l10n_ec_penalty_capped = False

            if not order.l10n_ec_expected_delivery_date:
                continue

            # Determine delivery date (actual or today)
            delivery = order.l10n_ec_actual_delivery_date or date.today()
            expected = order.l10n_ec_expected_delivery_date

            if delivery > expected:
                delay = (delivery - expected).days
                order.l10n_ec_delay_days = delay

                try:
                    rate = order._get_penalty_rate()
                    cap_percent = order._get_penalty_cap()
                except ValidationError:
                    # Config not set - skip penalty calculation
                    continue

                # Calculate penalty
                penalty = order.amount_total * (rate / 100) * delay

                # Apply cap
                max_penalty = order.amount_total * (cap_percent / 100)
                if penalty > max_penalty:
                    order.l10n_ec_penalty_amount = max_penalty
                    order.l10n_ec_penalty_capped = True
                else:
                    order.l10n_ec_penalty_amount = penalty

    def action_compute_penalty(self):
        """Manual action to recalculate penalty."""
        self._compute_penalty()

        rate = self._get_penalty_rate()
        cap = self._get_penalty_cap()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Penalidad Calculada (DE 045-2025)'),
                'message': _(
                    'Días de retraso: %s\n'
                    'Tasa diaria: %.2f%%\n'
                    'Límite máximo: %.2f%%\n'
                    'Monto penalidad: $%.2f'
                ) % (self.l10n_ec_delay_days, rate, cap, self.l10n_ec_penalty_amount),
                'type': 'info',
                'sticky': False,
            }
        }

    @api.constrains('partner_id')
    def _check_uaf_for_government_contract(self):
        """
        DE 045-2025: Block contract confirmation if partner is government
        contractor without valid UAF certificate.
        """
        for order in self:
            partner = order.partner_id
            if partner.l10n_ec_government_contractor and not partner.l10n_ec_uaf_valid:
                raise ValidationError(_(
                    "DE 045-2025: No se puede confirmar este pedido.\n\n"
                    "El proveedor '%s' es contratista del Estado pero no tiene "
                    "un Certificado UAF válido.\n\n"
                    "Por favor, solicite al proveedor que cargue su certificado "
                    "UAF antes de continuar."
                ) % partner.name)
