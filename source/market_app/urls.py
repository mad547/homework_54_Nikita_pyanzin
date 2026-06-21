from django.urls import path
from market_app.views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    CategoryCreateView, CategoryProductsView,
    CartAddView, CartView, CartRemoveView, OrderCreateView,
)


urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/cart/add/', CartAddView.as_view(), name='cart_add'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<str:category_title>/', CategoryProductsView.as_view(), name='category_products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/remove/', CartRemoveView.as_view(), name='cart_remove'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
]