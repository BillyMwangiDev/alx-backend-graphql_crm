"""
Django admin configuration for CRM models.
"""
from django.contrib import admin
from .models import Customer, Product, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    list_display = ['id', 'name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    list_display = ['id', 'name', 'price', 'stock', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer', 'total_amount', 'order_date']
    search_fields = ['customer__name', 'customer__email']
    list_filter = ['order_date', 'total_amount']
    filter_horizontal = ['products']


