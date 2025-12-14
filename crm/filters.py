"""
Django-filter classes for CRM models.
"""
import django_filters
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """Filter class for Customer model."""
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    email_icontains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='exact')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Custom filter for phone pattern (starts with +1)
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at', 'phone']

    def filter_phone_pattern(self, queryset, name, value):
        """Filter customers by phone number pattern."""
        if value:
            return queryset.filter(phone__startswith=value)
        return queryset


class ProductFilter(django_filters.FilterSet):
    """Filter class for Product model."""
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='exact')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock = django_filters.NumberFilter(field_name='stock', lookup_expr='exact')
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    
    # Custom filter for low stock (stock < 10)
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

    def filter_low_stock(self, queryset, name, value):
        """Filter products with low stock (< 10)."""
        if value:
            return queryset.filter(stock__lt=10)
        return queryset


class OrderFilter(django_filters.FilterSet):
    """Filter class for Order model."""
    total_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='exact')
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='exact')
    order_date_gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')
    
    # Filter by customer name (related field lookup)
    customer_name = django_filters.CharFilter(
        field_name='customer__name',
        lookup_expr='icontains'
    )
    
    # Filter by product name (related field lookup)
    product_name = django_filters.CharFilter(
        field_name='products__name',
        lookup_expr='icontains'
    )
    
    # Filter orders that include a specific product ID
    product_id = django_filters.NumberFilter(field_name='products__id', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date', 'customer', 'products']

