#!/bin/bash
# Script to clean inactive customers with no orders since a year ago

python manage.py shell << EOF
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from crm.models import Customer, Order

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders at all
customers_no_orders = Customer.objects.filter(orders__isnull=True)

# Find customers whose most recent order is older than one year
# Get the latest order date for each customer
latest_orders = Order.objects.values('customer').annotate(
    latest_order_date=Max('order_date')
).filter(latest_order_date__lt=one_year_ago)

customer_ids_old_orders = [item['customer'] for item in latest_orders]
customers_old_orders = Customer.objects.filter(id__in=customer_ids_old_orders)

# Combine both querysets
customers_to_delete = (customers_no_orders | customers_old_orders).distinct()

# Get count before deletion
count = customers_to_delete.count()

# Delete customers
customers_to_delete.delete()

# Log result
with open('/tmp/customer_cleanup_log.txt', 'a') as f:
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"{timestamp} - Deleted {count} inactive customers\n")

print(f"Deleted {count} inactive customers")
EOF
