"""
Script to seed the database with sample CRM data.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer, Product, Order
from django.utils import timezone
from decimal import Decimal


def seed_database():
    """Seed the database with sample data."""
    print("Seeding database...")

    # Clear existing data (optional - comment out if you want to keep existing data)
    # Order.objects.all().delete()
    # Product.objects.all().delete()
    # Customer.objects.all().delete()

    # Create customers
    customers_data = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'phone': '+1234567890'},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'phone': '123-456-7890'},
        {'name': 'Carol White', 'email': 'carol@example.com', 'phone': '+1987654321'},
        {'name': 'David Brown', 'email': 'david@example.com', 'phone': '555-123-4567'},
    ]

    customers = []
    for data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=data['email'],
            defaults={
                'name': data['name'],
                'phone': data['phone']
            }
        )
        customers.append(customer)
        if created:
            print(f"Created customer: {customer.name}")

    # Create products
    products_data = [
        {'name': 'Laptop', 'price': Decimal('999.99'), 'stock': 10},
        {'name': 'Mouse', 'price': Decimal('29.99'), 'stock': 50},
        {'name': 'Keyboard', 'price': Decimal('79.99'), 'stock': 30},
        {'name': 'Monitor', 'price': Decimal('299.99'), 'stock': 15},
        {'name': 'Webcam', 'price': Decimal('49.99'), 'stock': 25},
    ]

    products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data['name'],
            defaults={
                'price': data['price'],
                'stock': data['stock']
            }
        )
        products.append(product)
        if created:
            print(f"Created product: {product.name} - ${product.price}")

    # Create orders
    orders_data = [
        {
            'customer': customers[0],
            'products': [products[0], products[1], products[2]],
            'order_date': timezone.now()
        },
        {
            'customer': customers[1],
            'products': [products[0], products[3]],
            'order_date': timezone.now()
        },
        {
            'customer': customers[2],
            'products': [products[1], products[2], products[4]],
            'order_date': timezone.now()
        },
    ]

    for data in orders_data:
        order = Order.objects.create(
            customer=data['customer'],
            total_amount=sum(p.price for p in data['products']),
            order_date=data['order_date']
        )
        order.products.set(data['products'])
        print(f"Created order: Order #{order.id} - {order.customer.name} - ${order.total_amount}")

    print("\nDatabase seeding completed!")
    print(f"Created {len(customers)} customers, {len(products)} products, and {len(orders_data)} orders.")


if __name__ == '__main__':
    seed_database()


