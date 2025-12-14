# Project Summary: ALX Backend GraphQL CRM

## Overview

This project implements a complete GraphQL-based CRM system using Django and graphene-django. It includes customer, product, and order management with advanced filtering capabilities.

## Completed Tasks

### Task 0: Set Up GraphQL Endpoint ✅
- Created Django project `alx-backend-graphql_crm`
- Created `crm` app
- Installed `graphene-django` and `django-filter`
- Defined `hello` query returning "Hello, GraphQL!"
- Connected GraphQL endpoint at `/graphql` with GraphiQL interface

### Task 1 & 2: GraphQL Mutations ✅
Implemented all required mutations:

1. **CreateCustomer**
   - Validates unique email
   - Validates phone format (+1234567890 or 123-456-7890)
   - Returns created customer and success message

2. **BulkCreateCustomers**
   - Accepts list of customer inputs
   - Supports partial success (creates valid entries even if some fail)
   - Returns list of created customers and errors

3. **CreateProduct**
   - Validates positive price
   - Validates non-negative stock
   - Returns created product

4. **CreateOrder**
   - Validates customer and product IDs exist
   - Ensures at least one product is selected
   - Calculates total_amount automatically
   - Returns order with nested customer and product data

### Task 3: Filtering ✅
Implemented comprehensive filtering:

1. **CustomerFilter**
   - Name (case-insensitive partial match)
   - Email (case-insensitive partial match)
   - Created date range (gte, lte)
   - Custom phone pattern filter (starts with pattern)

2. **ProductFilter**
   - Name (case-insensitive partial match)
   - Price range (gte, lte)
   - Stock range (gte, lte)
   - Custom low stock filter (stock < 10)

3. **OrderFilter**
   - Total amount range (gte, lte)
   - Order date range (gte, lte)
   - Customer name (related field lookup)
   - Product name (related field lookup)
   - Product ID filter

## Project Structure

```
alx-backend-graphql_crm/
├── alx_backend_graphql_crm/      # Main project
│   ├── settings.py               # Django settings with GraphQL config
│   ├── urls.py                   # URL routing with GraphQL endpoint
│   └── schema.py                 # Main GraphQL schema
├── crm/                          # CRM app
│   ├── models.py                 # Customer, Product, Order models
│   ├── schema.py                 # GraphQL queries and mutations
│   ├── filters.py                # Django-filter classes
│   ├── admin.py                  # Django admin configuration
│   └── tests.py                  # Unit tests
├── manage.py
├── requirements.txt
├── seed_db.py                    # Database seeding script
├── pytest.ini                    # Pytest configuration
├── .flake8                        # Flake8 configuration
├── README.md
└── SETUP.md
```

## Key Features

### Models
- **Customer**: name, email (unique), phone, timestamps
- **Product**: name, price, stock, timestamps
- **Order**: customer (FK), products (M2M), total_amount, order_date

### GraphQL Queries
- `hello`: Simple greeting query
- `allCustomers`: Filtered customer list (Relay connection)
- `allProducts`: Filtered product list (Relay connection)
- `allOrders`: Filtered order list (Relay connection)

### GraphQL Mutations
- `createCustomer`: Create single customer
- `bulkCreateCustomers`: Create multiple customers with partial success
- `createProduct`: Create product
- `createOrder`: Create order with products

### Validation & Error Handling
- Email uniqueness validation
- Phone format validation (regex)
- Price and stock validation
- User-friendly error messages
- Partial success support for bulk operations

## Testing

Run tests with:
```bash
pytest
# or
python manage.py test
```

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Seed database (optional): `python seed_db.py`
4. Start server: `python manage.py runserver`
5. Visit: `http://localhost:8000/graphql`

## Example GraphQL Queries

### Hello Query
```graphql
{
  hello
}
```

### Create Customer
```graphql
mutation {
  createCustomer(input: {
    name: "Alice"
    email: "alice@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
    }
    message
  }
}
```

### Filter Customers
```graphql
query {
  allCustomers(filter: { nameIcontains: "Ali" }) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

## Notes

- All field names are automatically converted from snake_case to camelCase by Graphene
- Filter fields use the pattern: `fieldName` for exact, `fieldNameGte` for >=, `fieldNameLte` for <=
- Relay connection pattern is used for filtered queries (edges/node structure)
- Mutations use input objects for better organization


