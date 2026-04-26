from pyclbr import Class

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')


    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


    def __str__(self):
        return self.name
