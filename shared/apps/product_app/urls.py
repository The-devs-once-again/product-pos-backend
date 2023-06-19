from django.urls import path, include
from shared.apps.product_app.views import ProductViewSet

from shared.utils.custom_routers import CRUDRouter


product_router = CRUDRouter()
product_router.register('product', ProductViewSet, 'product')

urlpatterns = [
    path('', include(product_router.urls)),
]