from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'category']
    search_fields = ['name', 'price', 'is_active', 'category'] 
    list_filter = ['price', 'is_active', 'category']
