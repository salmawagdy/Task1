from django.db import models
from category.models import Category
from django_softdelete.models import SoftDeleteModel

class Product(SoftDeleteModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')


    def __str__(self):
        return self.name
