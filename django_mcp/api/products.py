from ninja import Router
from typing import List, Optional
from services.odoo_client import OdooClient
from pydantic import BaseModel

router = Router()

class ProductSchema(BaseModel):
    id: int
    name: str
    default_code: Optional[str] = None
    list_price: float
    description: Optional[str] = None
    image_url: Optional[str] = None

@router.get("/", response=List[ProductSchema])
def list_products(request):
    """
    Fetch visible products from Odoo.
    Logic: product.template where sale_ok=True and published.
    """
    client = OdooClient()

    # 1. Search
    domain = [('sale_ok', '=', True)]
    ids = client.execute_kw('product.template', 'search', [domain])

    if not ids:
        return []

    # 2. Read
    fields = ['id', 'name', 'default_code', 'list_price', 'description_sale']
    products_data = client.execute_kw('product.template', 'read', [ids], {'fields': fields})

    # 3. Transform
    results = []
    for p in products_data:
        results.append({
            'id': p['id'],
            'name': p['name'],
            'default_code': p.get('default_code') or '',
            'list_price': p['list_price'],
            'description': p.get('description_sale') or '',
            # Image URL logic would go here (e.g. /web/image/product.template/ID/image_128)
            'image_url': f"/web/image/product.template/{p['id']}/image_512"
        })

    return results

@router.get("/{product_id}", response=ProductSchema)
def get_product(request, product_id: int):
    client = OdooClient()
    data = client.execute_kw('product.template', 'read', [[product_id]], {
        'fields': ['id', 'name', 'default_code', 'list_price', 'description_sale']
    })

    if not data:
        from ninja.errors import HttpError
        raise HttpError(404, "Product not found")

    p = data[0]
    return {
        'id': p['id'],
        'name': p['name'],
        'default_code': p.get('default_code') or '',
        'list_price': p['list_price'],
        'description': p.get('description_sale') or '',
        'image_url': f"/web/image/product.template/{p['id']}/image_512"
    }
