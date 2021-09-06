from rest_framework import serializers
from .models import *


class ProductCategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerialize(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
