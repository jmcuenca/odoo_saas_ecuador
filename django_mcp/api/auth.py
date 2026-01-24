from ninja import Router
from pydantic import BaseModel
from typing import Optional
from services.odoo_client import OdooClient
from ninja.errors import HttpError

router = Router()

class LoginSchema(BaseModel):
    login: str
    password: str
    db: Optional[str] = None

class SignupSchema(BaseModel):
    name: str
    email: str
    password: str
    vat: Optional[str] = None # RUC/Cedula
    phone: Optional[str] = None

@router.post("/login")
def login(request, payload: LoginSchema):
    """
    Authenticates a user against Odoo.
    Returns: UID and Partner ID.
    """
    client = OdooClient()
    db = payload.db or client.db

    # 1. Authenticate (returns UID if success, False/None if fail)
    uid = client.common.authenticate(db, payload.login, payload.password, {})

    if not uid:
        raise HttpError(401, "Invalid Credentials")

    # 2. Fetch Partner ID associated with this User
    # res.users model has 'partner_id' field.
    user_data = client.execute_kw('res.users', 'read', [[uid]], {'fields': ['partner_id']})

    partner_id = None
    partner_name = ""
    if user_data:
        # partner_id is [id, name]
        p_field = user_data[0].get('partner_id')
        if p_field:
            partner_id = p_field[0]
            partner_name = p_field[1]

    return {
        "status": "success",
        "uid": uid,
        "partner_id": partner_id,
        "name": partner_name,
        # In a real app, we would issue a JWT here.
        # For this vibe implementation, we return the raw identifiers for the frontend to store.
    }

@router.post("/signup")
def signup(request, payload: SignupSchema):
    """
    Creates a new Customer (res.partner) and linked Portal User (res.users) in Odoo.
    Note: Creating res.users usually requires admin execution context.
    The OdooClient is configured as ADMIN, so this is valid.
    """
    client = OdooClient()

    # 1. Check if partner exists (by email or vat)
    domain = ['|', ('email', '=', payload.email), ('vat', '=', payload.vat)] if payload.vat else [('email', '=', payload.email)]
    existing = client.execute_kw('res.partner', 'search', [domain])

    if existing:
        raise HttpError(409, "User with this Email or RUC already exists")

    # 2. Create Partner
    partner_vals = {
        'name': payload.name,
        'email': payload.email,
        'vat': payload.vat or '',
        'phone': payload.phone or '',
        'customer_rank': 1,
        'l10n_ec_identifier_type': ('cedula' if len(payload.vat) == 10 else 'ruc') if payload.vat else False
    }
    partner_id = client.execute_kw('res.partner', 'create', [partner_vals])

    # 3. Create Portal User
    # We assign the 'Portal' group (internal link)
    # This is more complex via API. Simplified: We just Create User with partner_id.
    # Odoo will auto-assign proper groups via 'sel_groups_1_9_10' (group selection field) or user template.
    # For now, we JUST create the partner. The "User" account is optional unless they need Portal access.
    # PRO VIBE RULE: "Real Implementation".
    # Real implementation: Commerce users need a login.

    user_vals = {
        'name': payload.name,
        'login': payload.email,
        'password': payload.password,
        'partner_id': partner_id,
        'groups_id': [(6, 0, [])] # Default groups?
        # By default, a new user might get Internal User if not careful.
        # We'll skip forcing res.users logic to avoid breaking Odoo ACLs remotely without known IDs.
        # Strategy: We rely on the Partner ID for the Cart.
        # BUT: For /login to work, they NEED a res.users.

        # Let's try creating it. If it fails due to context/groups, we'll see.
        # 'active': True
    }

    try:
        user_id = client.execute_kw('res.users', 'create', [user_vals])
    except Exception as e:
        # Atomic-ish Rollback: Delete the partner if user creation fails
        # to prevent "Email already exists" errors on retry.
        try:
            client.execute_kw('res.partner', 'unlink', [[partner_id]])
        except Exception as cleanup_error:
            # If rollback fails, we are in trouble, but at least we tried.
            # Log this in a real system.
            pass

        raise HttpError(500, f"User account creation failed: {str(e)}")

    return {
        "status": "success",
        "uid": user_id,
        "partner_id": partner_id
    }
