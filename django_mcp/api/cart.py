from ninja import Router
from typing import List, Optional
from pydantic import BaseModel
from services.odoo_client import OdooClient
from ninja.errors import HttpError
from datetime import datetime

router = Router()

class CartItemSchema(BaseModel):
    product_id: int
    quantity: float

class CartResponseSchema(BaseModel):
    order_id: int
    name: str # Order Reference (SO/xxx)
    amount_total: float
    lines: List[dict] # Simplified for now

class CheckoutSchema(BaseModel):
    partner_id: int # The customer checkout out
    # address_id, etc. for future

@router.post("/add")
def add_to_cart(request, payload: CartItemSchema, partner_id: int):
    """
    Adds an item to the user's active Draft Order (Quotation).
    If no draft order exists, creates one.
    """
    client = OdooClient()

    # 1. Find Open Draft Order for Partner
    domain = [
        ('partner_id', '=', partner_id),
        ('state', '=', 'draft'),
        # Optional: Check website_id if multi-website
    ]
    # Search for latest draft
    order_ids = client.execute_kw('sale.order', 'search', [domain], {'limit': 1, 'order': 'id desc'})

    order_id = None
    if order_ids:
        order_id = order_ids[0]
    else:
        # Create new Draft Order
        order_vals = {
            'partner_id': partner_id,
            'state': 'draft',
            'date_order': str(datetime.now())
        }
        order_id = client.execute_kw('sale.order', 'create', [order_vals])

    # 2. Add Line
    # Check if product already exists in line to increment?
    # Odoo 'sale.order.line' usually handles this if we use specific methods, but via API we might duplicate lines unless we check.
    # Simple Logic: Check if line with product_id exists.

    line_domain = [('order_id', '=', order_id), ('product_id', '=', payload.product_id)]
    line_ids = client.execute_kw('sale.order.line', 'search', [line_domain])

    if line_ids:
        # Update existing line
        line_id = line_ids[0]
        # Read current qty
        line_data = client.execute_kw('sale.order.line', 'read', [[line_id]], {'fields': ['product_uom_qty']})
        if line_data:
            new_qty = line_data[0]['product_uom_qty'] + payload.quantity
            client.execute_kw('sale.order.line', 'write', [[line_id], {'product_uom_qty': new_qty}])
    else:
        # Create new line
        line_vals = {
            'order_id': order_id,
            'product_id': payload.product_id,
            'product_uom_qty': payload.quantity,
        }
        client.execute_kw('sale.order.line', 'create', [line_vals])

    # Return updated Cart
    return get_cart_logic(client, order_id)

@router.get("/")
def get_cart(request, partner_id: int):
    """
    Get active cart for partner.
    """
    client = OdooClient()
    domain = [
        ('partner_id', '=', partner_id),
        ('state', '=', 'draft'),
    ]
    order_ids = client.execute_kw('sale.order', 'search', [domain], {'limit': 1, 'order': 'id desc'})

    if not order_ids:
        return {"message": "Empty Cart", "amount_total": 0.0, "lines": []}

    return get_cart_logic(client, order_ids[0])

def get_cart_logic(client, order_id):
    # Read Order Headers
    order_data = client.execute_kw('sale.order', 'read', [[order_id]], {
        'fields': ['id', 'name', 'amount_total', 'order_line']
    })

    if not order_data:
         raise HttpError(404, "Order not found")

    order = order_data[0]

    # Read Lines
    lines = []
    if order['order_line']:
        line_fields = ['id', 'product_id', 'product_uom_qty', 'price_unit', 'price_subtotal', 'name']
        line_data = client.execute_kw('sale.order.line', 'read', [order['order_line']], {'fields': line_fields})
        for l in line_data:
            # product_id is [id, name]
            p_name = l['product_id'][1] if l['product_id'] else "Unknown"
            p_id = l['product_id'][0] if l['product_id'] else 0

            lines.append({
                'id': l['id'],
                'product_id': p_id,
                'product_name': p_name,
                'qty': l['product_uom_qty'],
                'price': l['price_unit'],
                'total': l['price_subtotal']
            })

    return {
        "order_id": order['id'],
        "name": order['name'],
        "amount_total": order['amount_total'],
        "lines": lines
    }

@router.post("/checkout")
def checkout(request, payload: CheckoutSchema):
    """
    Confirms the Draft Order to 'sale' state.
    """
    # 1. Find Cart
    client = OdooClient()
    domain = [
        ('partner_id', '=', payload.partner_id),
        ('state', '=', 'draft'),
    ]
    order_ids = client.execute_kw('sale.order', 'search', [domain], {'limit': 1, 'order': 'id desc'})

    if not order_ids:
        raise HttpError(404, "No active cart to checkout")

    order_id = order_ids[0]

    # 2. Confirm (Action Confirm)
    # Allows Odoo to trigger delivery orders, etc.
    try:
        client.execute_kw('sale.order', 'action_confirm', [[order_id]])
    except Exception as e:
        raise HttpError(400, f"Checkout Failed: {str(e)}")

    return {"status": "success", "order_id": order_id, "message": "Order Confirmed"}
