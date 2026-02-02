# Mechanic Shop API

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
