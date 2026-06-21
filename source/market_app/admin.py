from django.contrib import admin
from market_app.models import Category, Product, CartItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'created_at']
    list_filter = ['category']
    search_fields = ['title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)