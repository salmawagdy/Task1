from django.urls import path
from .views import product_list, active_products, create_product

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/active/', active_products, name='active-products'),
    path('products/create/', create_product, name='create-product'),
]