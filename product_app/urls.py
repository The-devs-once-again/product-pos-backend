from django.contrib import admin
from django.urls import path
from .views import ProductListView, ProductDetailView, CreatProductView, UpdateProductView

urlpatterns = [
    path('create_product/', CreatProductView.as_view()),
    path('upate_product/', UpdateProductView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<str:product_name>', ProductDetailView.as_view())
]
