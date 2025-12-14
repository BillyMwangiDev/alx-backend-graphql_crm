# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API for managing customers, products, and orders.

## Features

- GraphQL API with queries and mutations
- Customer, Product, and Order management
- Bulk customer creation
- Advanced filtering and search capabilities
- Nested order creation with product associations
- Robust validation and error handling

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (or SQLite for development)
- pip

### Installation

1. **Create and activate virtual environment:**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional):**

```bash
python manage.py createsuperuser
```

6. **Seed database (optional):**

```bash
python seed_db.py
```

7. **Run development server:**

```bash
python manage.py runserver
```

## Usage

### GraphQL Endpoint

Visit `http://localhost:8000/graphql` to access the GraphiQL interface.

### Example Queries

#### Hello Query
```graphql
{
  hello
}
```

#### Create Customer
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
      phone
    }
    message
  }
}
```

#### Filter Customers
```graphql
query {
  allCustomers(filter: { nameIcontains: "Ali" }) {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}
```

## Project Structure

```
alx-backend-graphql_crm/
├── alx_backend_graphql_crm/  # Main project directory
│   ├── settings.py
│   ├── urls.py
│   └── schema.py
├── crm/                       # CRM app
│   ├── models.py
│   ├── schema.py
│   ├── filters.py
│   └── admin.py
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Development

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to public functions/classes

### Linting

```bash
flake8 .
black --check .
```

## License

MIT


