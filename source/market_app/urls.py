from django.urls import path
from market_app.views import products_view, product_view, product_add_view, category_add_view


urlpatterns = [
    path('', products_view, name='products'),
    path('products/', product_view, name='products'),
    path('products/<int:pk>/', product_view, name='product'),
    path('products/add/', product_add_view, name='product_add'),
    path('categories/add/', category_add_view, name='category_add'),
]