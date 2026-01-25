# -*- coding: utf-8 -*-
"""
Ecuador Complete MCP API
========================

ALL Ecuador ERP operations accessible via MCP.
Django Ninja router for Odoo Ecuador localization.
"""
from ninja import Router
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from services.odoo_client import OdooClient

router = Router()
odoo = OdooClient()


# =============================================================================
# SCHEMAS
# =============================================================================

class RucSchema(BaseModel):
    ruc: str


class PartnerSchema(BaseModel):
    ruc: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_company: bool = True


class InvoiceSchema(BaseModel):
    partner_id: int
    lines: List[Dict[str, Any]]


class InvoiceIdSchema(BaseModel):
    invoice_id: int


class WithholdingSchema(BaseModel):
    invoice_id: int
    ir_tax_id: Optional[int] = None
    iva_tax_id: Optional[int] = None


class PayslipSchema(BaseModel):
    employee_id: int
    date_start: str
    date_end: str


class DauSchema(BaseModel):
    name: str
    fob_value: float
    freight: float
    insurance: float


# =============================================================================
# COMPANY ONBOARDING
# =============================================================================

@router.post("/onboarding/ruc")
def onboard_by_ruc(request, payload: RucSchema):
    """
    Super simple onboarding: Enter RUC, auto-load ALL data from SRI.
    """
    sri_data = odoo.execute_kw(
        'l10n_ec.sri.ruc.service',
        'consult_ruc',
        [payload.ruc]
    )

    if not sri_data or sri_data.get('error'):
        return {"error": "RUC no encontrado en SRI", "ruc": payload.ruc}

    company_id = odoo.execute_kw('res.company', 'search', [[]], {'limit': 1})[0]

    odoo.execute_kw('res.company', 'write', [[company_id], {
        'name': sri_data.get('razonSocial', ''),
        'vat': payload.ruc,
        'street': sri_data.get('direccionMatriz', ''),
        'l10n_ec_special_contributor': sri_data.get('contribuyenteEspecial') == 'SI',
        'l10n_ec_retention_agent': sri_data.get('agenteRetencion') == 'SI',
        'l10n_ec_obligated_accounting': sri_data.get('obligadoContabilidad') == 'SI',
    }])

    return {"status": "success", "company_id": company_id, "sri_data": sri_data}


# =============================================================================
# PARTNERS
# =============================================================================

@router.post("/partner/create")
def create_partner(request, payload: PartnerSchema):
    """Create partner with SRI auto-load if RUC provided."""
    vals = {'is_company': payload.is_company}

    if payload.ruc and len(payload.ruc) == 13:
        sri_data = odoo.execute_kw('l10n_ec.sri.ruc.service', 'consult_ruc', [payload.ruc])
        if sri_data and not sri_data.get('error'):
            vals.update({
                'name': sri_data.get('razonSocial', payload.name or ''),
                'vat': payload.ruc,
                'street': sri_data.get('direccionMatriz', ''),
                'l10n_ec_identifier_type': 'ruc',
            })
    else:
        vals['name'] = payload.name or 'Cliente'
        if payload.ruc:
            vals['vat'] = payload.ruc

    if payload.email:
        vals['email'] = payload.email
    if payload.phone:
        vals['phone'] = payload.phone

    partner_id = odoo.execute_kw('res.partner', 'create', [vals])
    return {"partner_id": partner_id}


@router.get("/partner/search/{query}")
def search_partner(request, query: str):
    """Search partner by RUC, cedula, or name."""
    domain = ['|', '|', ('vat', 'ilike', query), ('name', 'ilike', query), ('ref', 'ilike', query)]
    return odoo.execute_kw('res.partner', 'search_read', [domain],
                          {'fields': ['id', 'name', 'vat', 'email', 'phone'], 'limit': 10})


# =============================================================================
# INVOICES
# =============================================================================

@router.post("/invoice/create")
def create_invoice(request, payload: InvoiceSchema):
    """Create sales invoice."""
    lines = [(0, 0, {
        'product_id': l.get('product_id'),
        'quantity': l.get('quantity', 1),
        'price_unit': l.get('price_unit', 0),
    }) for l in payload.lines]

    invoice_id = odoo.execute_kw('account.move', 'create', [{
        'move_type': 'out_invoice',
        'partner_id': payload.partner_id,
        'invoice_line_ids': lines,
    }])
    return {"invoice_id": invoice_id}


@router.post("/invoice/post")
def post_invoice(request, payload: InvoiceIdSchema):
    """Confirm invoice and auto-send to SRI if configured."""
    odoo.execute_kw('account.move', 'action_post', [[payload.invoice_id]])
    return odoo.execute_kw('account.move', 'search_read',
                          [[['id', '=', payload.invoice_id]]],
                          {'fields': ['name', 'state', 'l10n_ec_sri_status', 'l10n_ec_sri_access_key']})[0]


@router.post("/invoice/send_sri")
def send_to_sri(request, payload: InvoiceIdSchema):
    """Send invoice to SRI."""
    odoo.execute_kw('account.move', 'action_send_sri', [[payload.invoice_id]])
    return odoo.execute_kw('account.move', 'search_read',
                          [[['id', '=', payload.invoice_id]]],
                          {'fields': ['l10n_ec_sri_status', 'l10n_ec_sri_response', 'l10n_ec_sri_access_key']})[0]


@router.post("/invoice/check_sri")
def check_sri_status(request, payload: InvoiceIdSchema):
    """Check SRI authorization status."""
    odoo.execute_kw('account.move', 'action_check_sri', [[payload.invoice_id]])
    return odoo.execute_kw('account.move', 'search_read',
                          [[['id', '=', payload.invoice_id]]],
                          {'fields': ['l10n_ec_sri_status', 'l10n_ec_authorization_date']})[0]


# =============================================================================
# WITHHOLDING (RETENCIONES)
# =============================================================================

@router.post("/withholding/create")
def create_withholding(request, payload: WithholdingSchema):
    """Create withholding for vendor bill."""
    invoice = odoo.execute_kw('account.move', 'search_read',
                             [[['id', '=', payload.invoice_id]]],
                             {'fields': ['partner_id', 'amount_untaxed', 'amount_tax']})[0]

    lines = []
    if payload.ir_tax_id:
        lines.append((0, 0, {'tax_id': payload.ir_tax_id, 'base': invoice['amount_untaxed']}))
    if payload.iva_tax_id:
        lines.append((0, 0, {'tax_id': payload.iva_tax_id, 'base': invoice['amount_tax']}))

    ret_id = odoo.execute_kw('l10n_ec.withholding', 'create', [{
        'partner_id': invoice['partner_id'][0],
        'invoice_id': payload.invoice_id,
        'line_ids': lines,
    }])
    return {"withholding_id": ret_id}


@router.get("/withholding/taxes")
def get_withholding_taxes(request):
    """Get available withholding taxes (IR and IVA)."""
    taxes = odoo.execute_kw('account.tax', 'search_read',
                           [[['name', 'ilike', 'Retención']]],
                           {'fields': ['id', 'name', 'amount', 'type_tax_use']})
    return {"taxes": taxes}


# =============================================================================
# PAYROLL (NÓMINA)
# =============================================================================

@router.post("/payroll/create")
def create_payslip(request, payload: PayslipSchema):
    """Create Ecuador payslip with IESS calculations."""
    payslip_id = odoo.execute_kw('l10n_ec.payslip', 'create', [{
        'employee_id': payload.employee_id,
        'date_start': payload.date_start,
        'date_end': payload.date_end,
    }])
    return {"payslip_id": payslip_id}


@router.get("/payroll/rates")
def get_payroll_rates(request):
    """Get current IESS and SBU rates from config - NO HARDCODED FALLBACKS."""
    def get_required(key):
        value = odoo.execute_kw('ir.config_parameter', 'get_param', [key])
        if not value:
            raise ValueError(f"Missing required config: {key}. Install l10n_ec modules properly.")
        return value

    return {
        "sbu": float(get_required('l10n_ec.sbu')),
        "iess_personal": float(get_required('l10n_ec.iess_aporte_personal')),
        "iess_employer": float(get_required('l10n_ec.iess_aporte_patronal')),
    }


@router.get("/payroll/employees")
def get_employees(request):
    """Get list of employees."""
    return odoo.execute_kw('hr.employee', 'search_read', [[]],
                          {'fields': ['id', 'name', 'job_title', 'department_id'], 'limit': 50})


# =============================================================================
# TAX CALENDAR (CALENDARIO TRIBUTARIO)
# =============================================================================

@router.get("/calendar/deadlines")
def get_deadlines(request, days_ahead: int = 30):
    """Get upcoming tax deadlines based on company's 9th RUC digit."""
    return odoo.execute_kw('l10n_ec.tax.calendar', 'get_upcoming_deadlines', [days_ahead])


@router.get("/calendar/company")
def get_company_calendar_info(request):
    """Get company deadline info including 9th RUC digit."""
    return odoo.execute_kw('l10n_ec.tax.calendar', 'get_company_deadline_info', [])


# =============================================================================
# CUSTOMS (ADUANAS)
# =============================================================================

@router.post("/customs/dau/create")
def create_dau(request, payload: DauSchema):
    """Create DAU (Declaración Aduanera Única)."""
    dau_id = odoo.execute_kw('l10n_ec.import.dau', 'create', [{
        'name': payload.name,
        'fob_value': payload.fob_value,
        'freight': payload.freight,
        'insurance': payload.insurance,
    }])
    return {"dau_id": dau_id}


@router.get("/customs/rates")
def get_customs_rates(request):
    """Get FODINFA and customs IVA rates - NO HARDCODED FALLBACKS."""
    def get_required(key):
        value = odoo.execute_kw('ir.config_parameter', 'get_param', [key])
        if not value:
            raise ValueError(f"Missing required config: {key}. Install l10n_ec modules properly.")
        return value

    return {
        "fodinfa": float(get_required('l10n_ec.fodinfa')),
        "customs_iva": float(get_required('l10n_ec.customs_iva')),
    }


@router.get("/customs/tariffs")
def get_tariffs(request, query: str = ""):
    """Search tariff headings."""
    domain = [('name', 'ilike', query)] if query else []
    return odoo.execute_kw('l10n_ec.tariff.heading', 'search_read', [domain],
                          {'fields': ['id', 'code', 'name', 'ad_valorem'], 'limit': 20})


# =============================================================================
# REPORTS (ATS, RDEP)
# =============================================================================

@router.get("/reports/ats/generate")
def generate_ats(request, year: int, month: int):
    """Generate ATS XML for given period."""
    return odoo.execute_kw('l10n_ec.ats.wizard', 'generate', [{
        'year': year, 'month': month
    }])


@router.get("/reports/form104")
def get_form104_data(request, year: int, month: int):
    """Get Form 104 (IVA) data for period."""
    return odoo.execute_kw('l10n_ec.report.form104', 'get_data', [{
        'year': year, 'month': month
    }])


# =============================================================================
# CONFIG
# =============================================================================

@router.get("/config/all")
def get_all_config(request):
    """Get all Ecuador configuration parameters."""
    params = odoo.execute_kw('ir.config_parameter', 'search_read',
                            [[['key', 'like', 'l10n_ec.%']]],
                            {'fields': ['key', 'value']})
    return {p['key']: p['value'] for p in params}


@router.post("/config/set")
def set_config(request, key: str, value: str):
    """Set configuration parameter."""
    odoo.execute_kw('ir.config_parameter', 'set_param', [key, value])
    return {"status": "success", "key": key, "value": value}
