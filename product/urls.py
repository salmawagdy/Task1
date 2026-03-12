from django.urls import path
from .views import product_list, product_by_id, active_products, create_product

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_by_id, name='product-by-id'),
    path('products/active/', active_products, name='active-products'),
    path('products/create/', create_product, name='create-product'),
]