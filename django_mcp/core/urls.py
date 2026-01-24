from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(
    title="Odoo Vibe Middleware",
    description="Headless API Gateway for Odoo 18 - ALL MODULES",
    version="2.0.0"
)

# Import Controllers
from api.generic import router as generic_router
from api.sri import router as sri_router
from api.products import router as products_router
from api.auth import router as auth_router
from api.cart import router as cart_router
from api.ecuador import router as ecuador_router
from api.odoo import router as odoo_router

api.add_router("/generic", generic_router, tags=["Generic CRUD"])
api.add_router("/sri", sri_router, tags=["SRI Ecuador"])
api.add_router("/products", products_router, tags=["Products"])
api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/cart", cart_router, tags=["Shopping Cart"])
api.add_router("/ecuador", ecuador_router, tags=["Ecuador Localization"])
api.add_router("/odoo", odoo_router, tags=["All Odoo Modules"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
