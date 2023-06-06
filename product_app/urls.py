from django.contrib import admin
from django.urls import path
from .views import ProductListView, ProductDetailView, CreatProductView, UpdateProductView

urlpatterns = [
    path('create_product/', CreatProductView.as_view()),
    path('update_product/<int:pk>', UpdateProductView.as_view()),
    path('product_list/', ProductListView.as_view()),
    path('get_product/<str:product_name>', ProductDetailView.as_view())
]
