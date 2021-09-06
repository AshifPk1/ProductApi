from .serializer import *
import ast
import datetime
import json
import random
import secrets
import string
from .pagination import *
from rest_framework.response import Response
import pytz
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Avg, F, Max, Min, Sum
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .serializer import *


# Create your views here.

class VewProductCategory(APIView):
    def get(self, request, category_id):
        if not ProductCategory.objects.filter(id=category_id).exists():
            return Response({"status": "error", "data": "invalid Category id"})
        else:
            instance = ProductCategory.objects.get(id=category_id)
            instance_serializer = ProductCategorySerialize(instance)
            context = {"status": "success", "data": instance_serializer.data}
            return Response(context)

    def patch(self, request, category_id):
        if not ProductCategory.objects.filter(id=category_id).exists():
            return Response({"status": "error", "data": "invalid Category id"})
        else:
            instance = ProductCategory.objects.get(id=category_id)
            data = request.data
            instance.name = data.get("name", instance.name)
            instance.save()
            response = ProductCategory.objects.get(id=category_id)
            response_serializer = ProductCategorySerialize(response)
            return Response({"status": "success", "data": response_serializer.data})

    def delete(self, request, category_id):
        if not ProductCategory.objects.filter(id=category_id).exists():
            return Response({"status": "error", "data": "invalid Category id"})
        data = ProductCategory.objects.get(id=category_id)
        data.delete()
        return Response({"status": "sucess", "data": "deleted successfully"})


class ProductCategoryCreateView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = ProductCategorySerialize

    def get(self, request):
        instance = ProductCategory.objects.all()
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data)

    def post(self, request):

        name = request.data.get("name")

        product_category_create = ProductCategory.objects.create(name=name)

        return Response({"status": "success", "data": "Product Category Successfully Created"})


class ProductCreateView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = ProductSerialize

    def get(self, request):
        instance = Product.objects.all()
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data)

    def post(self, request):

        product_name = request.data.get("product_name")
        product_category_id = request.data.get("product_category_id")
        product_price = request.data.get("product_price")
        product_imageurl = request.FILES.get('product_imageurl')
        product_category = None

        if product_category_id:
            if not ProductCategory.objects.filter(id=product_category_id).exists():
                return Response({"status": "error", "data": "invalid Category id"})

            product_category = ProductCategory.objects.get(id=product_category_id)
        else:
            return Response({"status": "error", "data": "Please Add Category id"})

        product__create = Product.objects.create(product_name=product_name, product_category=product_category,
                                                 product_price=product_price, product_imageurl=product_imageurl)

        return Response({"status": "success", "data": "Product Successfully Created"})


class VewProduct(APIView):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return Response({"status": "error", "data": "invalid Product id"})
        else:
            instance = Product.objects.get(id=product_id)
            instance_serializer = ProductSerialize(instance)
            context = {"status": "success", "data": instance_serializer.data}
            return Response(context)

    def patch(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return Response({"status": "error", "data": "invalid Product id"})
        else:
            instance = Product.objects.get(id=product_id)
            data = request.data
            files = request.FILES
            instance.product_name = data.get("product_name", instance.product_name)
            instance.product_price = data.get("product_price", instance.product_price)
            instance.product_imageurl = files.get("product_imageurl", instance.product_imageurl)
            product_category_id = data.get("product_category_id")
            if product_category_id:
                if not ProductCategory.objects.filter(id=product_category_id).exists():
                    return Response({"status": "error", "data": "invalid Category id"})

                product_category = ProductCategory.objects.get(id=product_category_id)
                instance.product_category = product_category
            instance.save()
            response = Product.objects.get(id=product_id)
            response_serializer = ProductSerialize(response)
            return Response({"status": "success", "data": response_serializer.data})

    def delete(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return Response({"status": "error", "data": "invalid Product id"})
        data = Product.objects.get(id=product_id)
        data.delete()
        return Response({"status": "sucess", "data": "deleted successfully"})
