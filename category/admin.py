from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'image']
    search_fields = ['name']