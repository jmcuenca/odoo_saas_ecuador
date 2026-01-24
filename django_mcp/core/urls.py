from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(
    title="Odoo Vibe Middleware",
    description="Headless API Gateway for Odoo 18",
    version="1.0.0"
)

# Import Controllers
from api.generic import router as generic_router
from api.sri import router as sri_router
from api.products import router as products_router
from api.auth import router as auth_router
from api.cart import router as cart_router

api.add_router("/generic", generic_router)
api.add_router("/sri", sri_router)
api.add_router("/products", products_router)
api.add_router("/auth", auth_router)
api.add_router("/cart", cart_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
