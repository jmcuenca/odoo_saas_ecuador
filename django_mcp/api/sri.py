from ninja import Router
from pydantic import BaseModel
from typing import List, Optional
from services.odoo_client import OdooClient

router = Router()
odoo = OdooClient()

class SignSendSchema(BaseModel):
    invoice_id: int

class CheckStatusSchema(BaseModel):
    invoice_id: int

class ConfigureCompanySchema(BaseModel):
    company_name: str
    ruc: str
    p12_content_b64: str
    p12_password: str
    environment: str = '1' # 1=Test

@router.post("/sri/sign_and_send_invoice")
def sign_and_send_invoice(request, payload: SignSendSchema):
    """
    Macro Tool: Triggers the Odoo 'action_send_sri' method for a specific invoice.
    """
    # 1. Trigger the logic inside Odoo (which handles KeyGen, Signing, Sending)
    result = odoo.execute_kw(
        'account.move',
        'action_send_sri',
        [[payload.invoice_id]]
    )

    # 2. Read back the status to tell the Agent
    invoice = odoo.execute_kw(
        'account.move',
        'search_read',
        [[['id', '=', payload.invoice_id]]],
        {'fields': ['l10n_ec_sri_status', 'l10n_ec_sri_error', 'l10n_ec_sri_access_key']}
    )

    return {
        "action": "triggered",
        "current_state": invoice[0] if invoice else None
    }

@router.post("/sri/check_authorization")
def check_authorization(request, payload: CheckStatusSchema):
    """
    Macro Tool: Force check status with SRI.
    """
    odoo.execute_kw(
        'account.move',
        'action_check_sri',
        [[payload.invoice_id]]
    )

    invoice = odoo.execute_kw(
        'account.move',
        'search_read',
        [[['id', '=', payload.invoice_id]]],
        {'fields': ['l10n_ec_sri_status', 'l10n_ec_authorization_date']}
    )

    return invoice[0] if invoice else None

@router.post("/sri/configure_company_ec")
def configure_company_ec(request, payload: ConfigureCompanySchema):
    """
    Macro Tool: Onboards a new company for Ecuador SRI.
    1. Creates Company
    2. Sets RUC
    3. Uploads Certificate
    4. Sets Environment
    """
    # 1. Create Company
    company_id = odoo.execute_kw('res.company', 'create', [{
        'name': payload.company_name,
        'vat': payload.ruc,
        'l10n_ec_sri_environment': payload.environment
    }])

    # 2. Create Certificate
    cert_id = odoo.execute_kw('l10n_ec.certificate', 'create', [{
        'name': f"Firma {payload.company_name}",
        'company_id': company_id,
        'content': payload.p12_content_b64,
        'password': payload.p12_password,
        'state': 'active' # Assume validated for macro speed
    }])

    # 3. Link Certificate
    odoo.execute_kw('res.company', 'write', [[company_id], {
        'l10n_ec_certificate_id': cert_id
    }])

    return {"status": "success", "company_id": company_id, "sri_ready": True}
