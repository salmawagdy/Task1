from django.urls import path
from .views import product_list, product_by_id

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_by_id, name='product-by-id'),
]