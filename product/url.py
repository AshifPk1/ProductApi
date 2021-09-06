from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/product_category', views.ProductCategoryCreateView.as_view(), name="Product-category-creation"),
    path('api/v1/product_category/<int:category_id>', views.VewProductCategory.as_view(),
         name="Vew-Product-category"),
    path('api/v1/product', views.ProductCreateView.as_view(), name="Product-creation"),
    path('api/v1/product/<int:product_id>', views.VewProduct.as_view(),
         name="Vew-Product")
]
