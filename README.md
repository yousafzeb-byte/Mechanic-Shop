# Mechanic Shop API - Advanced Features Edition

![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

## 🎯 Project: Advanced API Development

This project implements a complete RESTful API for a Mechanic Shop with advanced features including:

- ✅ **Rate Limiting** - Protection against API abuse
- ✅ **Token Authentication** - JWT-based customer authentication
- ✅ **Caching** - Improved performance for frequently accessed data
- ✅ **Pagination** - Efficient data retrieval for large datasets
- ✅ **Advanced Queries** - Complex database operations
- ✅ **Inventory Management** - New resource with many-to-many relationships

## 📋 Features Implemented

### 🔐 Authentication & Security

- JWT token-based authentication using `python-jose`
- Password hashing with `bcrypt`
- Protected routes requiring valid tokens
- Customer login system
- Authorization checks (users can only modify their own data)

### ⏱️ Rate Limiting

- Default rate limits: 200 requests/day, 50 requests/hour
- Customer creation endpoint: 5 requests/minute
- Implemented using `Flask-Limiter`

### 💾 Caching

- GET customers endpoint cached for 60 seconds
- Implemented using `Flask-Caching`
- Improves performance for frequently accessed data

### 📄 Pagination

- GET customers endpoint supports pagination
- Query parameters: `page` and `per_page`
- Returns comprehensive pagination metadata

### 🔧 Advanced Queries

- **Edit Ticket Mechanics**: Add and remove multiple mechanics in one request
- **Mechanics Ranking**: Get mechanics ordered by tickets worked on
- Complex SQL queries with aggregations

### 📦 Inventory Management (NEW)

- Full CRUD operations for inventory parts
- Many-to-many relationship with service tickets
- Track parts used in each service

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Update Database

```bash
python update_database.py
```

### 3. Populate Sample Data (Optional)

```bash
python populate_database.py
```

### 4. Run the API

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📚 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with all endpoints
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing instructions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview

## 🧪 Testing with Postman

1. Import the collection: `Mechanic_Shop_Advanced_API.postman_collection.json`
2. Test all endpoints in the following order:
   - Create a customer
   - Login to get a token
   - Test protected routes with the token
   - Test pagination, caching, and rate limiting
   - Explore inventory and advanced queries

### Sample Test Credentials

After running `populate_database.py`:

- **Email:** john@example.com | **Password:** password123
- **Email:** jane@example.com | **Password:** password123
- **Email:** bob@example.com | **Password:** password123

## 📊 Database Schema

### Tables

- **customers** - Customer information (includes password field)
- **mechanics** - Mechanic information
- **service_tickets** - Service ticket records
- **inventory** - Inventory parts (NEW)
- **service_mechanic** - Junction table (tickets ↔ mechanics)
- **service_inventory** - Junction table (tickets ↔ inventory) (NEW)

### Relationships

- Customer → Service Tickets (One-to-Many)
- Service Ticket ↔ Mechanics (Many-to-Many)
- Service Ticket ↔ Inventory (Many-to-Many) (NEW)

## 🔑 Key API Endpoints

### Authentication

- `POST /customers/` - Create account (rate limited)
- `POST /customers/login` - Login and get token
- `GET /customers/my-tickets` - Get my tickets (requires token)

### Customers

- `GET /customers/?page=1&per_page=10` - Paginated list (cached)
- `PUT /customers/<id>` - Update (requires token)
- `DELETE /customers/<id>` - Delete (requires token)

### Mechanics

- `GET /mechanics/by-tickets` - Ranked by tickets worked (advanced query)

### Service Tickets

- `PUT /service-tickets/<id>/edit` - Add/remove mechanics (advanced query)
- `PUT /service-tickets/<id>/add-part/<part_id>` - Add inventory part

### Inventory (NEW)

- `POST /inventory/` - Create part
- `GET /inventory/` - List all parts
- `PUT /inventory/<id>` - Update part
- `DELETE /inventory/<id>` - Delete part

## 🛠️ Technologies Used

- **Flask 3.1.2** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-Limiter 3.5.0** - Rate limiting
- **Flask-Caching 2.1.0** - Caching
- **Marshmallow 4.2.1** - Serialization/validation
- **python-jose 3.3.0** - JWT tokens
- **bcrypt 4.1.2** - Password hashing
- **MySQL Connector** - Database driver

## 📁 Project Structure

```
Mechanic Shop/
├── app/
│   ├── __init__.py           # App factory with rate limiting & caching
│   ├── models.py             # Database models (includes Inventory)
│   ├── utils.py              # Token auth utilities (NEW)
│   └── blueprints/
│       ├── customer/         # Customer routes (auth, pagination)
│       ├── mechanic/         # Mechanic routes (advanced queries)
│       ├── service_ticket/   # Service ticket routes
│       └── inventory/        # Inventory routes (NEW)
├── requirements.txt          # Updated with new packages
├── update_database.py        # Database update script (NEW)
├── populate_database.py      # Sample data script (NEW)
├── API_DOCUMENTATION.md      # Complete API docs (NEW)
└── Mechanic_Shop_Advanced_API.postman_collection.json (NEW)
```

## ✅ Project Checklist

### Rate Limiting & Caching

- ✅ Rate limiting on customer creation route
- ✅ Default rate limits applied to all routes
- ✅ Caching on GET customers route

### Token Authentication

- ✅ `encode_token()` function
- ✅ `login_schema` for validation
- ✅ POST `/customers/login` route
- ✅ `@token_required` decorator
- ✅ GET `/customers/my-tickets` with token
- ✅ Protected update/delete routes

### Advanced Queries

- ✅ PUT `/service-tickets/<id>/edit` for add/remove mechanics
- ✅ GET `/mechanics/by-tickets` for ranking
- ✅ Pagination on GET customers

### Inventory System

- ✅ Inventory model with id, name, price
- ✅ Many-to-many relationship with service tickets
- ✅ Inventory blueprint with CRUD routes
- ✅ Add part to ticket route

## 🔒 Security Notes

⚠️ **Important:** Change the secret key before production deployment!

In `app/utils.py`:

```python
SECRET_KEY = "your-secret-key-change-this-in-production"
```

Generate a secure key:

```python
import secrets
print(secrets.token_hex(32))
```

## 📝 Additional Features

Beyond the project requirements, this project includes:

- Comprehensive error handling
- Authorization checks
- Detailed API documentation
- Sample data population script
- Complete Postman collection
- Automatic token storage in Postman

## 🤝 Contributing

This is an educational project for learning advanced API development techniques.

## 📄 License

Educational use only.

---

**Project completed by:** Yousaf Zeb  
**Date:** February 15, 2026  
**Course:** Advanced API Development

A RESTful API built with Flask using the Application Factory Pattern for managing a mechanic shop's customers, mechanics, and service tickets.

## Project Structure

```
Mechanic Shop/
├── app/
│   ├── __init__.py                 # Application factory
│   ├── models.py                   # Database models
│   └── blueprints/
│       ├── customer/
│       │   ├── __init__.py         # Customer blueprint initialization
│       │   ├── routes.py           # Customer CRUD routes
│       │   └── schemas.py          # Customer Marshmallow schemas
│       ├── mechanic/
│       │   ├── __init__.py         # Mechanic blueprint initialization
│       │   ├── routes.py           # Mechanic CRUD routes
│       │   └── schemas.py          # Mechanic Marshmallow schemas
│       └── service_ticket/
│           ├── __init__.py         # Service Ticket blueprint initialization
│           ├── routes.py           # Service Ticket routes
│           └── schemas.py          # Service Ticket Marshmallow schemas
├── venv/                           # Virtual environment
├── run.py                          # Application entry point
└── Mechanic_Shop_API.postman_collection.json  # Postman tests
```

## Database Schema

### Models and Relationships

- **Customer**: Stores customer information
  - One-to-Many with ServiceTicket

- **Mechanic**: Stores mechanic/employee information
  - Many-to-Many with ServiceTicket

- **ServiceTicket**: Stores service records
  - Many-to-One with Customer
  - Many-to-Many with Mechanic (via service_mechanic association table)

## API Endpoints

### Customers (`/customers`)

- `POST /` - Create a new customer
- `GET /` - Get all customers
- `GET /<id>` - Get a specific customer
- `PUT /<id>` - Update a customer
- `DELETE /<id>` - Delete a customer

### Mechanics (`/mechanics`)

- `POST /` - Create a new mechanic
- `GET /` - Get all mechanics
- `GET /<id>` - Get a specific mechanic
- `PUT /<id>` - Update a mechanic
- `DELETE /<id>` - Delete a mechanic

### Service Tickets (`/service-tickets`)

- `POST /` - Create a new service ticket
- `GET /` - Get all service tickets
- `GET /<id>` - Get a specific service ticket
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` - Assign a mechanic to a service ticket
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` - Remove a mechanic from a service ticket
- `DELETE /<id>` - Delete a service ticket

## Setup and Installation

1. **Create virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**

   ```bash
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install flask flask-sqlalchemy mysql-connector-python marshmallow-sqlalchemy
   ```

4. **Create MySQL database:**

   ```sql
   CREATE DATABASE mechanic_shop;
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

The API will be available at `http://127.0.0.1:5000`

## Testing with Postman

Import the `Mechanic_Shop_API.postman_collection.json` file into Postman to test all endpoints.

### Sample Test Flow:

1. **Create a Customer**

   ```json
   POST /customers/
   {
       "name": "John Doe",
       "email": "john.doe@example.com",
       "phone": "555-1234",
       "address": "123 Main St, Springfield"
   }
   ```

2. **Create a Mechanic**

   ```json
   POST /mechanics/
   {
       "name": "Mike Johnson",
       "email": "mike.johnson@mechanicshop.com",
       "phone": "555-5678",
       "address": "456 Elm St, Springfield",
       "salary": 55000.00
   }
   ```

3. **Create a Service Ticket**

   ```json
   POST /service-tickets/
   {
       "VIN": "1HGBH41JXMN109186",
       "description": "Oil change and tire rotation",
       "service_date": "2026-02-01",
       "customer_id": 1
   }
   ```

4. **Assign Mechanic to Service Ticket**
   ```
   PUT /service-tickets/1/assign-mechanic/1
   ```

## Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Marshmallow** - Serialization/Deserialization
- **MySQL** - Database
- **Application Factory Pattern** - Project structure
