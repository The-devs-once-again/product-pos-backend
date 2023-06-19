from django.urls import path, include

from shared.utils.custom_routers import CRUDRouter
from .views import BillingViewSet, OrderViewSet

store_router = CRUDRouter()
store_router.register('order', OrderViewSet, basename='order')
store_router.register('billing', BillingViewSet, basename='billing')

urlpatterns = [
    path('', include(store_router.urls)),
]
