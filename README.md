# E-Commerce REST API

A backend e-commerce REST API built with **Django** and **Django REST Framework**. It provides product management, order processing, authentication, filtering, caching, background email notifications, and API documentation.

## Features

- JWT authentication
- Product CRUD operations
- Order creation and management
- User-specific orders
- UUID-based order IDs
- Order status management
- Product search, filtering, and ordering
- Custom order ownership permissions
- Redis caching with automatic invalidation
- Celery background tasks
- Order confirmation emails
- API throttling
- Query optimization
- Swagger and ReDoc documentation
- Django Silk profiling

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- SimpleJWT
- Djoser
- django-filter
- drf-spectacular
- Django Silk

## Main API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT tokens |
| POST | `/api/token/refresh/` | Refresh access token |

### Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products/` | List products |
| POST | `/products/` | Create product |
| GET | `/products/{product_id}/` | Retrieve product |
| PUT/PATCH | `/products/{product_id}/` | Update product |
| DELETE | `/products/{product_id}/` | Delete product |
| GET | `/products/info/` | Product statistics |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders/` | List orders |
| POST | `/orders/` | Create order |
| GET | `/orders/{order_id}/` | Retrieve order |
| PUT/PATCH | `/orders/{order_id}/` | Update order |
| DELETE | `/orders/{order_id}/` | Delete order |
| GET | `/orders/user-orders/` | View current user's orders |

## API Documentation

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`
- OpenAPI Schema: `/api/schema/`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vrushang922/Ecommerce_backend.git
cd ecommerce_app
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv env
env\Scripts\activate
```

Linux/macOS:

```bash
python -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for your Django secret key, PostgreSQL configuration, and email settings.

Do not commit your `.env` file to GitHub.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start Redis

Redis is required for caching and Celery.

### 7. Start Celery

```bash
celery -A ecom_api worker --loglevel=info
```

On Windows:

```bash
celery -A ecom_api worker --loglevel=info --pool=solo
```

### 8. Run the development server

```bash
python manage.py runserver
```

## Project Highlights

This project demonstrates practical backend development with REST APIs, authentication, permissions, PostgreSQL, Redis caching, Celery background tasks, filtering, database transactions, query optimization, and API documentation.
