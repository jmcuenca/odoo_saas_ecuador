from ninja import Router
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..services.odoo_client import OdooClient

router = Router()
odoo = OdooClient()

class SearchReadSchema(BaseModel):
    model: str
    domain: List[Any] = []
    fields: Optional[List[str]] = None
    limit: int = 10
    offset: int = 0
    order: Optional[str] = None

class CreateSchema(BaseModel):
    model: str
    values: Dict[str, Any]

class WriteSchema(BaseModel):
    model: str
    ids: List[int]
    values: Dict[str, Any]

class UnlinkSchema(BaseModel):
    model: str
    ids: List[int]

class ExecuteSchema(BaseModel):
    model: str
    method: str
    ids: List[int]
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}

class IntrospectionSchema(BaseModel):
    model: str

@router.post("/odoo/search_read")
def search_read(request, payload: SearchReadSchema):
    """
    Universal Read: Fetch records from any Odoo model.
    """
    return odoo.execute_kw(
        payload.model,
        'search_read',
        [payload.domain],
        {
            'fields': payload.fields,
            'limit': payload.limit,
            'offset': payload.offset,
            'order': payload.order
        }
    )

@router.post("/odoo/create")
def create_record(request, payload: CreateSchema):
    """
    Universal Create: Create a record in any Odoo model.
    """
    return odoo.execute_kw(
        payload.model,
        'create',
        [payload.values]
    )

@router.post("/odoo/write")
def write_record(request, payload: WriteSchema):
    """
    Universal Update: Update records in any Odoo model.
    """
    return odoo.execute_kw(
        payload.model,
        'write',
        [payload.ids, payload.values]
    )

@router.post("/odoo/unlink")
def unlink_record(request, payload: UnlinkSchema):
    """
    Universal Delete: Delete records in any Odoo model.
    """
    return odoo.execute_kw(
        payload.model,
        'unlink',
        [payload.ids]
    )

@router.post("/odoo/execute")
def execute_method(request, payload: ExecuteSchema):
    """
    Universal Execute: Call any method (like button clicks) on any Odoo model.
    """
    # The 'ids' are typically the first argument for model methods
    args = [payload.ids] + payload.args
    return odoo.execute_kw(
        payload.model,
        payload.method,
        args,
        payload.kwargs
    )

@router.post("/odoo/inspect_model")
def inspect_model(request, payload: IntrospectionSchema):
    """
    Introspection: Get fields, types, and help text for a model.
    """
    return odoo.execute_kw(
        payload.model,
        'fields_get',
        [],
        {'attributes': ['string', 'help', 'type', 'selection', 'required', 'readonly']}
    )
