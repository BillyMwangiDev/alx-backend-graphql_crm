"""
GraphQL schema for CRM app with queries and mutations.
"""
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import re

from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# Node Types
class CustomerType(DjangoObjectType):
    """GraphQL type for Customer model."""
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class CustomerNode(DjangoObjectType):
    """GraphQL node for Customer model."""
    class Meta:
        model = Customer
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class ProductNode(DjangoObjectType):
    """GraphQL node for Product model."""
    class Meta:
        model = Product
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class OrderNode(DjangoObjectType):
    """GraphQL node for Order model."""
    class Meta:
        model = Order
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


# Input Types
class CustomerInput(graphene.InputObjectType):
    """Input type for creating a customer."""
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class BulkCustomerInput(graphene.InputObjectType):
    """Input type for bulk customer creation."""
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    """Input type for creating a product."""
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class OrderInput(graphene.InputObjectType):
    """Input type for creating an order."""
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


# Output Types
class CreateCustomerOutput(graphene.ObjectType):
    """Output type for CreateCustomer mutation."""
    customer = graphene.Field(CustomerType)
    message = graphene.String()


class BulkCreateCustomersOutput(graphene.ObjectType):
    """Output type for BulkCreateCustomers mutation."""
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)


class CreateProductOutput(graphene.ObjectType):
    """Output type for CreateProduct mutation."""
    product = graphene.Field(ProductNode)


class CreateOrderOutput(graphene.ObjectType):
    """Output type for CreateOrder mutation."""
    order = graphene.Field(OrderNode)


# Mutations
class CreateCustomer(graphene.Mutation):
    """Mutation to create a single customer."""
    customer = graphene.Field(CustomerType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    def mutate(self, info, name, email, phone):
        """Create a new customer."""
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)


class BulkCreateCustomers(graphene.Mutation):
    """Mutation to create multiple customers in bulk."""
    class Arguments:
        input = graphene.List(BulkCustomerInput, required=True)

    Output = BulkCreateCustomersOutput

    @staticmethod
    def mutate(root, info, input):
        """Create multiple customers with partial success support."""
        customers = []
        errors = []

        # Process each customer independently for partial success
        for idx, customer_data in enumerate(input):
            try:
                # Validate email uniqueness
                if Customer.objects.filter(email=customer_data.email).exists():
                    errors.append(
                        f"Row {idx + 1}: Email '{customer_data.email}' already exists"
                    )
                    continue

                # Validate phone format
                if customer_data.phone and not CreateCustomer.validate_phone(
                    customer_data.phone
                ):
                    errors.append(
                        f"Row {idx + 1}: Invalid phone format for '{customer_data.phone}'"
                    )
                    continue

                customer = Customer.objects.create(
                    name=customer_data.name,
                    email=customer_data.email,
                    phone=customer_data.phone or None
                )
                customers.append(customer)

            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        return BulkCreateCustomersOutput(
            customers=customers,
            errors=errors
        )


class CreateProduct(graphene.Mutation):
    """Mutation to create a product."""
    class Arguments:
        input = ProductInput(required=True)

    Output = CreateProductOutput

    @staticmethod
    def mutate(root, info, input):
        """Create a new product."""
        # Validate price is positive
        if input.price <= 0:
            raise ValidationError("Price must be positive")

        # Validate stock is non-negative
        stock = input.stock if input.stock is not None else 0
        if stock < 0:
            raise ValidationError("Stock cannot be negative")

        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=stock
        )

        return CreateProductOutput(product=product)


class CreateOrder(graphene.Mutation):
    """Mutation to create an order with products."""
    class Arguments:
        input = OrderInput(required=True)

    Output = CreateOrderOutput

    @staticmethod
    def mutate(root, info, input):
        """Create a new order with associated products."""
        # Validate customer exists
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise ValidationError(f"Customer with ID '{input.customer_id}' does not exist")

        # Validate at least one product
        if not input.product_ids or len(input.product_ids) == 0:
            raise ValidationError("At least one product must be selected")

        # Validate products exist
        products = []
        for product_id in input.product_ids:
            try:
                product = Product.objects.get(pk=product_id)
                products.append(product)
            except Product.DoesNotExist:
                raise ValidationError(f"Product with ID '{product_id}' does not exist")

        # Calculate total amount
        total_amount = sum(product.price for product in products)

        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_date=input.order_date or timezone.now()
        )

        # Associate products
        order.products.set(products)

        return CreateOrderOutput(order=order)


# Query Class
class Query(graphene.ObjectType):
    """Query class for CRM app."""
    hello = graphene.String(default_value="Hello, GraphQL!")

    # Simple list query for customers
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(self, info):
        """Resolve all customers."""
        return Customer.objects.all()

    # Filtered queries using DjangoFilterConnectionField
    all_customers_filtered = DjangoFilterConnectionField(
        CustomerNode,
        filterset_class=CustomerFilter
    )
    all_products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter
    )
    all_orders = DjangoFilterConnectionField(
        OrderNode,
        filterset_class=OrderFilter
    )


# Mutation Class
class Mutation(graphene.ObjectType):
    """Mutation class for CRM app."""
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

