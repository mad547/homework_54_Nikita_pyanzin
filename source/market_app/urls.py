from django.urls import path
from market_app.views import (
    products_view, product_view, product_add_view,
    product_edit_view, product_delete_view,
    category_add_view, category_products_view
)


urlpatterns = [
    path('', products_view, name='products'),
    path('products/add/', product_add_view, name='product_add'),
    path('products/<int:pk>/', product_view, name='product'),
    path('products/<int:pk>/edit/', product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', product_delete_view, name='product_delete'),
    path('categories/add/', category_add_view, name='category_add'),
    path('categories/<str:category_title>/', category_products_view, name='category_products'),
]