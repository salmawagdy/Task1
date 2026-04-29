from django.urls import path
from .views import product_list, active_products, create_product, product_detail

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/active/', active_products, name='active-products'),
    path('products/create/', create_product, name='create-product'),
    path('products/detail/<int:pk>/', product_detail, name='product-detail'),
]