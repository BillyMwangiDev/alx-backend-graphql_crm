"""
Tests for CRM app.
"""
import pytest
from django.test import TestCase
from decimal import Decimal
from .models import Customer, Product, Order


class CustomerModelTest(TestCase):
    """Test Customer model."""

    def test_create_customer(self):
        """Test creating a customer."""
        customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="+1234567890"
        )
        self.assertEqual(customer.name, "Test Customer")
        self.assertEqual(customer.email, "test@example.com")
        self.assertTrue(Customer.objects.filter(email="test@example.com").exists())

    def test_customer_email_unique(self):
        """Test that customer email must be unique."""
        Customer.objects.create(
            name="Customer 1",
            email="duplicate@example.com"
        )
        with self.assertRaises(Exception):
            Customer.objects.create(
                name="Customer 2",
                email="duplicate@example.com"
            )


class ProductModelTest(TestCase):
    """Test Product model."""

    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(
            name="Test Product",
            price=Decimal("99.99"),
            stock=10
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Decimal("99.99"))
        self.assertEqual(product.stock, 10)


class OrderModelTest(TestCase):
    """Test Order model."""

    def test_create_order(self):
        """Test creating an order with products."""
        customer = Customer.objects.create(
            name="Test Customer",
            email="customer@example.com"
        )
        product1 = Product.objects.create(
            name="Product 1",
            price=Decimal("50.00"),
            stock=10
        )
        product2 = Product.objects.create(
            name="Product 2",
            price=Decimal("30.00"),
            stock=5
        )

        order = Order.objects.create(
            customer=customer,
            total_amount=Decimal("80.00")
        )
        order.products.add(product1, product2)

        self.assertEqual(order.customer, customer)
        self.assertEqual(order.products.count(), 2)
        self.assertEqual(order.total_amount, Decimal("80.00"))
        self.assertEqual(order.calculate_total(), Decimal("80.00"))


