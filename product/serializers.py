from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')  # show category name instead of ID

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'is_active', 'category']