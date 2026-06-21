from django.contrib import admin
from market_app.models import Category, Product, CartItem,Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'created_at']
    list_filter = ['category']
    search_fields = ['title']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'created_at']
    list_display_links = ['id','name']
    ordering = ['-created_at']
    inlines = [OrderItemInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)