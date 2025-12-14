# Setup Instructions

## Prerequisites

- Python 3.11+
- pip
- PostgreSQL (optional, SQLite is used by default)

## Step-by-Step Setup

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example` if available):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For PostgreSQL (optional):
```env
DB_NAME=graphql_crm
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Seed Database (Optional)

```bash
python seed_db.py
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access GraphQL Interface

Open your browser and navigate to:
```
http://localhost:8000/graphql
```

## Testing

Run tests with pytest:

```bash
pytest
```

Or with Django test runner:

```bash
python manage.py test
```

## Linting

Check code style:

```bash
flake8 .
black --check .
```

Format code:

```bash
black .
```

## Git Setup

Initialize Git repository:

```bash
git init
git add .
git commit -m "Initial commit: GraphQL CRM setup"
```

Create feature branch:

```bash
git checkout -b feature/graphql-mutations
```


