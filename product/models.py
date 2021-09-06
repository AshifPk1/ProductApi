from django.db import models


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


class Product(models.Model):
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_price = models.CharField(max_length=100, blank=True, null=True)
    product_imageurl = models.ImageField(null=True, blank=True)
