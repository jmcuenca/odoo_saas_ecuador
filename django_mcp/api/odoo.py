# -*- coding: utf-8 -*-
"""
Complete Odoo MCP API
======================

ALL Odoo ERP operations accessible via MCP.
Covers: Accounting, Sales, Purchase, Inventory, HR, CRM, POS, etc.
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

class IdSchema(BaseModel):
    id: int

class IdsSchema(BaseModel):
    ids: List[int]

class SearchSchema(BaseModel):
    domain: List[Any] = []
    fields: Optional[List[str]] = None
    limit: int = 80
    offset: int = 0
    order: Optional[str] = None

class CreateSchema(BaseModel):
    values: Dict[str, Any]

class WriteSchema(BaseModel):
    ids: List[int]
    values: Dict[str, Any]

class SaleOrderLineSchema(BaseModel):
    product_id: int
    quantity: float
    price_unit: Optional[float] = None

class SaleOrderSchema(BaseModel):
    partner_id: int
    lines: List[SaleOrderLineSchema]

class PurchaseOrderSchema(BaseModel):
    partner_id: int
    lines: List[Dict[str, Any]]

class StockMoveSchema(BaseModel):
    product_id: int
    quantity: float
    location_id: int
    location_dest_id: int

class PaymentSchema(BaseModel):
    partner_id: int
    amount: float
    journal_id: int
    payment_type: str = 'inbound'


# =============================================================================
# ACCOUNTING
# =============================================================================

@router.get("/accounting/journals")
def get_journals(request):
    """Get all journals."""
    return odoo.execute_kw('account.journal', 'search_read', [[]],
                          {'fields': ['id', 'name', 'type', 'code']})


@router.get("/accounting/accounts")
def get_accounts(request, account_type: Optional[str] = None):
    """Get chart of accounts."""
    domain = [('account_type', '=', account_type)] if account_type else []
    return odoo.execute_kw('account.account', 'search_read', [domain],
                          {'fields': ['id', 'code', 'name', 'account_type'], 'limit': 200})


@router.post("/accounting/invoices")
def search_invoices(request, payload: SearchSchema):
    """Search invoices."""
    return odoo.execute_kw('account.move', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'amount_total', 'state', 'move_type'],
                           'limit': payload.limit, 'offset': payload.offset, 'order': payload.order})


@router.post("/accounting/invoice/create")
def create_invoice(request, payload: CreateSchema):
    """Create invoice."""
    return {"id": odoo.execute_kw('account.move', 'create', [payload.values])}


@router.post("/accounting/invoice/post")
def post_invoice(request, payload: IdSchema):
    """Post/confirm invoice."""
    odoo.execute_kw('account.move', 'action_post', [[payload.id]])
    return {"status": "posted", "id": payload.id}


@router.post("/accounting/payment/create")
def create_payment(request, payload: PaymentSchema):
    """Create payment."""
    payment_id = odoo.execute_kw('account.payment', 'create', [{
        'partner_id': payload.partner_id,
        'amount': payload.amount,
        'journal_id': payload.journal_id,
        'payment_type': payload.payment_type,
    }])
    return {"payment_id": payment_id}


@router.post("/accounting/payment/post")
def post_payment(request, payload: IdSchema):
    """Post payment."""
    odoo.execute_kw('account.payment', 'action_post', [[payload.id]])
    return {"status": "posted", "id": payload.id}


@router.get("/accounting/taxes")
def get_taxes(request):
    """Get all taxes."""
    return odoo.execute_kw('account.tax', 'search_read', [[]],
                          {'fields': ['id', 'name', 'amount', 'type_tax_use', 'amount_type']})


# =============================================================================
# SALES
# =============================================================================

@router.post("/sales/orders")
def search_sales_orders(request, payload: SearchSchema):
    """Search sales orders."""
    return odoo.execute_kw('sale.order', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'amount_total', 'state'],
                           'limit': payload.limit, 'offset': payload.offset})


@router.post("/sales/order/create")
def create_sale_order(request, payload: SaleOrderSchema):
    """Create sales order."""
    lines = [(0, 0, {
        'product_id': l.product_id,
        'product_uom_qty': l.quantity,
        'price_unit': l.price_unit,
    }) for l in payload.lines]

    order_id = odoo.execute_kw('sale.order', 'create', [{
        'partner_id': payload.partner_id,
        'order_line': lines,
    }])
    return {"order_id": order_id}


@router.post("/sales/order/confirm")
def confirm_sale_order(request, payload: IdSchema):
    """Confirm sales order."""
    odoo.execute_kw('sale.order', 'action_confirm', [[payload.id]])
    return {"status": "confirmed", "id": payload.id}


@router.post("/sales/order/cancel")
def cancel_sale_order(request, payload: IdSchema):
    """Cancel sales order."""
    odoo.execute_kw('sale.order', 'action_cancel', [[payload.id]])
    return {"status": "cancelled", "id": payload.id}


@router.get("/sales/order/{order_id}")
def get_sale_order(request, order_id: int):
    """Get sales order details."""
    return odoo.execute_kw('sale.order', 'search_read', [[['id', '=', order_id]]],
                          {'fields': ['id', 'name', 'partner_id', 'order_line', 'amount_total', 'state']})[0]


# =============================================================================
# PURCHASE
# =============================================================================

@router.post("/purchase/orders")
def search_purchase_orders(request, payload: SearchSchema):
    """Search purchase orders."""
    return odoo.execute_kw('purchase.order', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'amount_total', 'state'],
                           'limit': payload.limit, 'offset': payload.offset})


@router.post("/purchase/order/create")
def create_purchase_order(request, payload: PurchaseOrderSchema):
    """Create purchase order."""
    lines = [(0, 0, l) for l in payload.lines]
    order_id = odoo.execute_kw('purchase.order', 'create', [{
        'partner_id': payload.partner_id,
        'order_line': lines,
    }])
    return {"order_id": order_id}


@router.post("/purchase/order/confirm")
def confirm_purchase_order(request, payload: IdSchema):
    """Confirm purchase order."""
    odoo.execute_kw('purchase.order', 'button_confirm', [[payload.id]])
    return {"status": "confirmed", "id": payload.id}


# =============================================================================
# INVENTORY / STOCK
# =============================================================================

@router.get("/stock/locations")
def get_stock_locations(request):
    """Get stock locations."""
    return odoo.execute_kw('stock.location', 'search_read', [[['usage', 'in', ['internal', 'transit']]]],
                          {'fields': ['id', 'name', 'complete_name', 'usage']})


@router.get("/stock/warehouses")
def get_warehouses(request):
    """Get warehouses."""
    return odoo.execute_kw('stock.warehouse', 'search_read', [[]],
                          {'fields': ['id', 'name', 'code', 'lot_stock_id']})


@router.post("/stock/quants")
def search_stock_quants(request, payload: SearchSchema):
    """Search stock quants (inventory levels)."""
    return odoo.execute_kw('stock.quant', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'product_id', 'location_id', 'quantity', 'available_quantity'],
                           'limit': payload.limit})


@router.get("/stock/product/{product_id}")
def get_product_stock(request, product_id: int):
    """Get product stock levels."""
    return odoo.execute_kw('stock.quant', 'search_read', [[['product_id', '=', product_id]]],
                          {'fields': ['location_id', 'quantity', 'available_quantity']})


@router.post("/stock/pickings")
def search_pickings(request, payload: SearchSchema):
    """Search stock pickings (transfers)."""
    return odoo.execute_kw('stock.picking', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'state', 'picking_type_id', 'scheduled_date'],
                           'limit': payload.limit})


@router.post("/stock/picking/validate")
def validate_picking(request, payload: IdSchema):
    """Validate stock picking."""
    odoo.execute_kw('stock.picking', 'button_validate', [[payload.id]])
    return {"status": "validated", "id": payload.id}


@router.post("/stock/move/create")
def create_stock_move(request, payload: StockMoveSchema):
    """Create stock move."""
    move_id = odoo.execute_kw('stock.move', 'create', [{
        'product_id': payload.product_id,
        'product_uom_qty': payload.quantity,
        'location_id': payload.location_id,
        'location_dest_id': payload.location_dest_id,
        'name': 'MCP Stock Move',
    }])
    return {"move_id": move_id}


# =============================================================================
# PRODUCTS
# =============================================================================

@router.post("/products/search")
def search_products(request, payload: SearchSchema):
    """Search products."""
    return odoo.execute_kw('product.product', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'default_code', 'list_price', 'qty_available', 'type'],
                           'limit': payload.limit, 'offset': payload.offset})


@router.post("/products/create")
def create_product(request, payload: CreateSchema):
    """Create product."""
    return {"id": odoo.execute_kw('product.product', 'create', [payload.values])}


@router.get("/products/{product_id}")
def get_product(request, product_id: int):
    """Get product details."""
    return odoo.execute_kw('product.product', 'search_read', [[['id', '=', product_id]]])[0]


@router.get("/products/categories")
def get_product_categories(request):
    """Get product categories."""
    return odoo.execute_kw('product.category', 'search_read', [[]],
                          {'fields': ['id', 'name', 'parent_id', 'complete_name']})


# =============================================================================
# PARTNERS / CONTACTS
# =============================================================================

@router.post("/partners/search")
def search_partners(request, payload: SearchSchema):
    """Search partners."""
    return odoo.execute_kw('res.partner', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'email', 'phone', 'vat', 'is_company', 'customer_rank', 'supplier_rank'],
                           'limit': payload.limit, 'offset': payload.offset})


@router.post("/partners/create")
def create_partner(request, payload: CreateSchema):
    """Create partner."""
    return {"id": odoo.execute_kw('res.partner', 'create', [payload.values])}


@router.post("/partners/write")
def update_partner(request, payload: WriteSchema):
    """Update partner."""
    odoo.execute_kw('res.partner', 'write', [payload.ids, payload.values])
    return {"status": "updated", "ids": payload.ids}


@router.get("/partners/{partner_id}")
def get_partner(request, partner_id: int):
    """Get partner details."""
    return odoo.execute_kw('res.partner', 'search_read', [[['id', '=', partner_id]]])[0]


# =============================================================================
# HR / EMPLOYEES
# =============================================================================

@router.get("/hr/employees")
def get_employees(request):
    """Get employees."""
    return odoo.execute_kw('hr.employee', 'search_read', [[]],
                          {'fields': ['id', 'name', 'job_title', 'department_id', 'work_email', 'mobile_phone'], 'limit': 100})


@router.post("/hr/employees/create")
def create_employee(request, payload: CreateSchema):
    """Create employee."""
    return {"id": odoo.execute_kw('hr.employee', 'create', [payload.values])}


@router.get("/hr/departments")
def get_departments(request):
    """Get departments."""
    return odoo.execute_kw('hr.department', 'search_read', [[]],
                          {'fields': ['id', 'name', 'parent_id', 'manager_id']})


@router.get("/hr/contracts")
def get_contracts(request, employee_id: Optional[int] = None):
    """Get HR contracts."""
    domain = [('employee_id', '=', employee_id)] if employee_id else []
    return odoo.execute_kw('hr.contract', 'search_read', [domain],
                          {'fields': ['id', 'name', 'employee_id', 'wage', 'state', 'date_start', 'date_end']})


@router.get("/hr/attendance")
def get_attendance(request, employee_id: Optional[int] = None, limit: int = 50):
    """Get attendance records."""
    domain = [('employee_id', '=', employee_id)] if employee_id else []
    return odoo.execute_kw('hr.attendance', 'search_read', [domain],
                          {'fields': ['id', 'employee_id', 'check_in', 'check_out', 'worked_hours'],
                           'limit': limit, 'order': 'check_in desc'})


# =============================================================================
# CRM
# =============================================================================

@router.post("/crm/leads")
def search_leads(request, payload: SearchSchema):
    """Search CRM leads/opportunities."""
    return odoo.execute_kw('crm.lead', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'email_from', 'phone', 'stage_id', 'expected_revenue', 'type'],
                           'limit': payload.limit, 'offset': payload.offset})


@router.post("/crm/lead/create")
def create_lead(request, payload: CreateSchema):
    """Create CRM lead."""
    return {"id": odoo.execute_kw('crm.lead', 'create', [payload.values])}


@router.post("/crm/lead/convert")
def convert_lead_to_opportunity(request, payload: IdSchema):
    """Convert lead to opportunity."""
    odoo.execute_kw('crm.lead', 'convert_opportunity', [[payload.id], payload.id])
    return {"status": "converted", "id": payload.id}


@router.get("/crm/stages")
def get_crm_stages(request):
    """Get CRM stages."""
    return odoo.execute_kw('crm.stage', 'search_read', [[]],
                          {'fields': ['id', 'name', 'sequence', 'is_won']})


# =============================================================================
# POS
# =============================================================================

@router.get("/pos/configs")
def get_pos_configs(request):
    """Get POS configurations."""
    return odoo.execute_kw('pos.config', 'search_read', [[]],
                          {'fields': ['id', 'name', 'picking_type_id', 'pricelist_id']})


@router.post("/pos/sessions")
def search_pos_sessions(request, payload: SearchSchema):
    """Search POS sessions."""
    return odoo.execute_kw('pos.session', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'config_id', 'state', 'start_at', 'stop_at'],
                           'limit': payload.limit})


@router.post("/pos/orders")
def search_pos_orders(request, payload: SearchSchema):
    """Search POS orders."""
    return odoo.execute_kw('pos.order', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'amount_total', 'state', 'date_order'],
                           'limit': payload.limit})


# =============================================================================
# COMPANY & USERS
# =============================================================================

@router.get("/company/current")
def get_current_company(request):
    """Get current company."""
    companies = odoo.execute_kw('res.company', 'search_read', [[]],
                               {'fields': ['id', 'name', 'vat', 'email', 'phone', 'street', 'city', 'country_id'], 'limit': 1})
    return companies[0] if companies else None


@router.get("/company/all")
def get_all_companies(request):
    """Get all companies."""
    return odoo.execute_kw('res.company', 'search_read', [[]],
                          {'fields': ['id', 'name', 'vat', 'email', 'country_id']})


@router.get("/users")
def get_users(request):
    """Get users."""
    return odoo.execute_kw('res.users', 'search_read', [[]],
                          {'fields': ['id', 'name', 'login', 'email', 'partner_id', 'company_id'], 'limit': 100})


# =============================================================================
# REPORTS / ANALYTICS
# =============================================================================

@router.get("/reports/sales/summary")
def get_sales_summary(request, date_from: Optional[str] = None, date_to: Optional[str] = None):
    """Get sales summary."""
    domain = [('state', 'in', ['sale', 'done'])]
    if date_from:
        domain.append(('date_order', '>=', date_from))
    if date_to:
        domain.append(('date_order', '<=', date_to))

    orders = odoo.execute_kw('sale.order', 'search_read', [domain],
                            {'fields': ['amount_total']})
    total = sum(o['amount_total'] for o in orders)
    return {"total_sales": total, "order_count": len(orders)}


@router.get("/reports/inventory/valuation")
def get_inventory_valuation(request):
    """Get inventory valuation summary."""
    quants = odoo.execute_kw('stock.quant', 'search_read', [[['location_id.usage', '=', 'internal']]],
                            {'fields': ['product_id', 'quantity', 'value']})
    total_value = sum(q.get('value', 0) for q in quants)
    return {"total_value": total_value, "quant_count": len(quants)}


# =============================================================================
# PROJECT
# =============================================================================

@router.post("/project/projects")
def search_projects(request, payload: SearchSchema):
    """Search projects."""
    return odoo.execute_kw('project.project', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'user_id', 'date_start', 'date'],
                           'limit': payload.limit})


@router.post("/project/create")
def create_project(request, payload: CreateSchema):
    """Create project."""
    return {"id": odoo.execute_kw('project.project', 'create', [payload.values])}


@router.post("/project/tasks")
def search_tasks(request, payload: SearchSchema):
    """Search project tasks."""
    return odoo.execute_kw('project.task', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'project_id', 'user_ids', 'stage_id', 'date_deadline', 'kanban_state'],
                           'limit': payload.limit})


@router.post("/project/task/create")
def create_task(request, payload: CreateSchema):
    """Create project task."""
    return {"id": odoo.execute_kw('project.task', 'create', [payload.values])}


@router.get("/project/stages")
def get_project_stages(request):
    """Get project stages."""
    return odoo.execute_kw('project.task.type', 'search_read', [[]],
                          {'fields': ['id', 'name', 'sequence', 'fold']})


# =============================================================================
# HELPDESK
# =============================================================================

@router.post("/helpdesk/tickets")
def search_tickets(request, payload: SearchSchema):
    """Search helpdesk tickets."""
    return odoo.execute_kw('helpdesk.ticket', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'team_id', 'stage_id', 'priority', 'user_id'],
                           'limit': payload.limit})


@router.post("/helpdesk/ticket/create")
def create_ticket(request, payload: CreateSchema):
    """Create helpdesk ticket."""
    return {"id": odoo.execute_kw('helpdesk.ticket', 'create', [payload.values])}


@router.get("/helpdesk/teams")
def get_helpdesk_teams(request):
    """Get helpdesk teams."""
    return odoo.execute_kw('helpdesk.team', 'search_read', [[]],
                          {'fields': ['id', 'name', 'use_sla', 'member_ids']})


# =============================================================================
# WEBSITE / ECOMMERCE
# =============================================================================

@router.get("/website/pages")
def get_website_pages(request):
    """Get website pages."""
    return odoo.execute_kw('website.page', 'search_read', [[]],
                          {'fields': ['id', 'name', 'url', 'is_published', 'website_id'], 'limit': 100})


@router.get("/website/menus")
def get_website_menus(request):
    """Get website menus."""
    return odoo.execute_kw('website.menu', 'search_read', [[]],
                          {'fields': ['id', 'name', 'url', 'parent_id', 'sequence']})


@router.post("/ecommerce/orders")
def search_ecommerce_orders(request, payload: SearchSchema):
    """Search eCommerce orders (sale.order with website origin)."""
    domain = payload.domain + [('website_id', '!=', False)]
    return odoo.execute_kw('sale.order', 'search_read', [domain],
                          {'fields': payload.fields or ['id', 'name', 'partner_id', 'amount_total', 'state', 'website_id'],
                           'limit': payload.limit})


@router.get("/ecommerce/products")
def get_ecommerce_products(request, limit: int = 50):
    """Get products published on website."""
    return odoo.execute_kw('product.template', 'search_read', [[['is_published', '=', True]]],
                          {'fields': ['id', 'name', 'list_price', 'website_url', 'image_1920'], 'limit': limit})


# =============================================================================
# MANUFACTURING (MRP)
# =============================================================================

@router.post("/mrp/orders")
def search_manufacturing_orders(request, payload: SearchSchema):
    """Search manufacturing orders."""
    return odoo.execute_kw('mrp.production', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'product_id', 'product_qty', 'state', 'date_start', 'date_finished'],
                           'limit': payload.limit})


@router.post("/mrp/order/create")
def create_manufacturing_order(request, payload: CreateSchema):
    """Create manufacturing order."""
    return {"id": odoo.execute_kw('mrp.production', 'create', [payload.values])}


@router.post("/mrp/order/confirm")
def confirm_manufacturing_order(request, payload: IdSchema):
    """Confirm manufacturing order."""
    odoo.execute_kw('mrp.production', 'action_confirm', [[payload.id]])
    return {"status": "confirmed", "id": payload.id}


@router.get("/mrp/bom")
def get_bom_list(request, product_id: Optional[int] = None):
    """Get Bill of Materials."""
    domain = [('product_tmpl_id', '=', product_id)] if product_id else []
    return odoo.execute_kw('mrp.bom', 'search_read', [domain],
                          {'fields': ['id', 'product_tmpl_id', 'product_qty', 'code', 'type']})


@router.get("/mrp/workcenters")
def get_workcenters(request):
    """Get work centers."""
    return odoo.execute_kw('mrp.workcenter', 'search_read', [[]],
                          {'fields': ['id', 'name', 'code', 'resource_calendar_id', 'time_efficiency']})


# =============================================================================
# FLEET
# =============================================================================

@router.get("/fleet/vehicles")
def get_vehicles(request):
    """Get fleet vehicles."""
    return odoo.execute_kw('fleet.vehicle', 'search_read', [[]],
                          {'fields': ['id', 'name', 'license_plate', 'model_id', 'driver_id', 'state_id', 'odometer']})


@router.post("/fleet/vehicle/create")
def create_vehicle(request, payload: CreateSchema):
    """Create fleet vehicle."""
    return {"id": odoo.execute_kw('fleet.vehicle', 'create', [payload.values])}


@router.post("/fleet/odometer")
def log_odometer(request, vehicle_id: int, value: float):
    """Log odometer reading."""
    return {"id": odoo.execute_kw('fleet.vehicle.odometer', 'create', [{
        'vehicle_id': vehicle_id,
        'value': value,
    }])}


@router.get("/fleet/models")
def get_vehicle_models(request):
    """Get vehicle models."""
    return odoo.execute_kw('fleet.vehicle.model', 'search_read', [[]],
                          {'fields': ['id', 'name', 'brand_id', 'vehicle_type']})


# =============================================================================
# EVENTS
# =============================================================================

@router.post("/events/search")
def search_events(request, payload: SearchSchema):
    """Search events."""
    return odoo.execute_kw('event.event', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'date_begin', 'date_end', 'seats_available', 'state'],
                           'limit': payload.limit})


@router.post("/events/create")
def create_event(request, payload: CreateSchema):
    """Create event."""
    return {"id": odoo.execute_kw('event.event', 'create', [payload.values])}


@router.post("/events/registrations")
def search_event_registrations(request, payload: SearchSchema):
    """Search event registrations."""
    return odoo.execute_kw('event.registration', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'event_id', 'partner_id', 'name', 'email', 'state'],
                           'limit': payload.limit})


# =============================================================================
# CALENDAR / MEETINGS
# =============================================================================

@router.post("/calendar/events")
def search_calendar_events(request, payload: SearchSchema):
    """Search calendar events."""
    return odoo.execute_kw('calendar.event', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'start', 'stop', 'user_id', 'partner_ids', 'location'],
                           'limit': payload.limit})


@router.post("/calendar/event/create")
def create_calendar_event(request, payload: CreateSchema):
    """Create calendar event."""
    return {"id": odoo.execute_kw('calendar.event', 'create', [payload.values])}


# =============================================================================
# MAIL / MESSAGES
# =============================================================================

@router.post("/mail/messages")
def search_messages(request, payload: SearchSchema):
    """Search mail messages."""
    return odoo.execute_kw('mail.message', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'subject', 'body', 'author_id', 'date', 'model', 'res_id'],
                           'limit': payload.limit})


@router.post("/mail/send")
def send_message(request, model: str, res_id: int, body: str, subject: Optional[str] = None):
    """Post message on record."""
    return odoo.execute_kw(model, 'message_post', [[res_id]], {
        'body': body,
        'subject': subject,
        'message_type': 'comment',
    })


# =============================================================================
# DOCUMENTS / ATTACHMENTS
# =============================================================================

@router.post("/attachments/search")
def search_attachments(request, payload: SearchSchema):
    """Search attachments."""
    return odoo.execute_kw('ir.attachment', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'res_model', 'res_id', 'mimetype', 'file_size'],
                           'limit': payload.limit})


@router.post("/attachments/create")
def create_attachment(request, name: str, datas: str, res_model: str, res_id: int):
    """Create attachment (datas must be base64 encoded)."""
    return {"id": odoo.execute_kw('ir.attachment', 'create', [{
        'name': name,
        'datas': datas,
        'res_model': res_model,
        'res_id': res_id,
    }])}


# =============================================================================
# SURVEYS
# =============================================================================

@router.get("/surveys")
def get_surveys(request):
    """Get surveys."""
    return odoo.execute_kw('survey.survey', 'search_read', [[]],
                          {'fields': ['id', 'title', 'state', 'questions_layout', 'scoring_type']})


@router.post("/surveys/answers")
def search_survey_answers(request, payload: SearchSchema):
    """Search survey user inputs."""
    return odoo.execute_kw('survey.user_input', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'survey_id', 'partner_id', 'state', 'scoring_total'],
                           'limit': payload.limit})


# =============================================================================
# LUNCH
# =============================================================================

@router.get("/lunch/products")
def get_lunch_products(request):
    """Get lunch products."""
    return odoo.execute_kw('lunch.product', 'search_read', [[]],
                          {'fields': ['id', 'name', 'price', 'supplier_id', 'category_id']})


@router.post("/lunch/order")
def create_lunch_order(request, product_id: int):
    """Create lunch order."""
    return {"id": odoo.execute_kw('lunch.order', 'create', [{
        'product_id': product_id,
    }])}


# =============================================================================
# EXPENSES
# =============================================================================

@router.post("/expenses/search")
def search_expenses(request, payload: SearchSchema):
    """Search expenses."""
    return odoo.execute_kw('hr.expense', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'name', 'employee_id', 'total_amount', 'state', 'date'],
                           'limit': payload.limit})


@router.post("/expenses/create")
def create_expense(request, payload: CreateSchema):
    """Create expense."""
    return {"id": odoo.execute_kw('hr.expense', 'create', [payload.values])}


# =============================================================================
# TIMESHEETS
# =============================================================================

@router.post("/timesheets/search")
def search_timesheets(request, payload: SearchSchema):
    """Search timesheets."""
    return odoo.execute_kw('account.analytic.line', 'search_read',
                          [payload.domain + [('project_id', '!=', False)]],
                          {'fields': payload.fields or ['id', 'name', 'project_id', 'task_id', 'employee_id', 'unit_amount', 'date'],
                           'limit': payload.limit})


@router.post("/timesheets/log")
def log_timesheet(request, project_id: int, task_id: int, hours: float, description: str):
    """Log timesheet entry."""
    return {"id": odoo.execute_kw('account.analytic.line', 'create', [{
        'project_id': project_id,
        'task_id': task_id,
        'unit_amount': hours,
        'name': description,
    }])}


# =============================================================================
# LEAVE / TIME OFF
# =============================================================================

@router.post("/leave/requests")
def search_leave_requests(request, payload: SearchSchema):
    """Search leave requests."""
    return odoo.execute_kw('hr.leave', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'employee_id', 'holiday_status_id', 'date_from', 'date_to', 'state'],
                           'limit': payload.limit})


@router.post("/leave/request")
def create_leave_request(request, payload: CreateSchema):
    """Create leave request."""
    return {"id": odoo.execute_kw('hr.leave', 'create', [payload.values])}


@router.get("/leave/types")
def get_leave_types(request):
    """Get leave types."""
    return odoo.execute_kw('hr.leave.type', 'search_read', [[]],
                          {'fields': ['id', 'name', 'requires_allocation', 'request_unit']})


# =============================================================================
# RECRUITMENT
# =============================================================================

@router.post("/recruitment/applicants")
def search_applicants(request, payload: SearchSchema):
    """Search job applicants."""
    return odoo.execute_kw('hr.applicant', 'search_read', [payload.domain],
                          {'fields': payload.fields or ['id', 'partner_name', 'job_id', 'stage_id', 'email_from', 'phone'],
                           'limit': payload.limit})


@router.post("/recruitment/applicant/create")
def create_applicant(request, payload: CreateSchema):
    """Create job applicant."""
    return {"id": odoo.execute_kw('hr.applicant', 'create', [payload.values])}


@router.get("/recruitment/jobs")
def get_jobs(request):
    """Get job positions."""
    return odoo.execute_kw('hr.job', 'search_read', [[]],
                          {'fields': ['id', 'name', 'department_id', 'no_of_recruitment', 'state']})

