# Mechanic Shop API - Project Summary

## ✅ Completed Implementation

### Application Factory Pattern Structure

The project has been successfully restructured using the Application Factory Pattern with the following components:

### 📁 Project Structure

```
Mechanic Shop/
├── app/                                    # Main application package
│   ├── __init__.py                         # Factory function & blueprint registration
│   ├── models.py                           # All database models
│   └── blueprints/                         # Blueprint modules
│       ├── customer/
│       │   ├── __init__.py                 # Blueprint initialization
│       │   ├── routes.py                   # Customer CRUD endpoints
│       │   └── schemas.py                  # Marshmallow schemas
│       ├── mechanic/
│       │   ├── __init__.py                 # Blueprint initialization
│       │   ├── routes.py                   # Mechanic CRUD endpoints
│       │   └── schemas.py                  # Marshmallow schemas
│       └── service_ticket/
│           ├── __init__.py                 # Blueprint initialization
│           ├── routes.py                   # Service ticket endpoints
│           └── schemas.py                  # Marshmallow schemas
├── venv/                                   # Virtual environment
├── run.py                                  # Application entry point
├── requirements.txt                        # Package dependencies
├── README.md                              # Complete documentation
└── Mechanic_Shop_API.postman_collection.json  # Postman test collection
```

## 🎯 API Endpoints Implemented

### Customer Blueprint (`/customers`)

✅ POST `/` - Create new customer
✅ GET `/` - Get all customers
✅ GET `/<id>` - Get customer by ID
✅ PUT `/<id>` - Update customer
✅ DELETE `/<id>` - Delete customer

### Mechanic Blueprint (`/mechanics`)

✅ POST `/` - Create new mechanic
✅ GET `/` - Get all mechanics
✅ GET `/<id>` - Get mechanic by ID
✅ PUT `/<id>` - Update mechanic
✅ DELETE `/<id>` - Delete mechanic

### Service Ticket Blueprint (`/service-tickets`)

✅ POST `/` - Create new service ticket
✅ GET `/` - Get all service tickets
✅ GET `/<id>` - Get service ticket by ID
✅ PUT `/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign mechanic
✅ PUT `/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic
✅ DELETE `/<id>` - Delete service ticket

## 🗄️ Database Models

### Customer Model

- id (Primary Key)
- name (String, required)
- email (String, unique, required)
- phone (String, required)
- address (String, required)
- Relationship: One-to-Many with ServiceTicket

### Mechanic Model

- id (Primary Key)
- name (String, required)
- email (String, unique, required)
- phone (String, required)
- address (String, required)
- salary (Float, required)
- Relationship: Many-to-Many with ServiceTicket

### ServiceTicket Model

- id (Primary Key)
- VIN (String, required)
- description (String, required)
- service_date (Date, required)
- customer_id (Foreign Key to Customer)
- Relationships:
  - Many-to-One with Customer
  - Many-to-Many with Mechanic (via service_mechanic table)

## 🔧 Technologies & Packages

- Flask 3.1.2
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.46
- Marshmallow 4.2.1
- Marshmallow-SQLAlchemy 1.4.2
- MySQL Connector Python 9.5.0

## 📮 Postman Collection

The `Mechanic_Shop_API.postman_collection.json` file includes:

- 5 Customer endpoints with sample data
- 5 Mechanic endpoints with sample data
- 6 Service Ticket endpoints with sample data
- Ready-to-import collection for immediate testing

## 🚀 Running the Application

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the application
python run.py
```

The API will be available at: `http://127.0.0.1:5000`

## ✨ Key Features Implemented

1. ✅ Application Factory Pattern
2. ✅ Blueprint-based modular architecture
3. ✅ Marshmallow schemas for serialization/deserialization
4. ✅ Full CRUD operations for all resources
5. ✅ Many-to-Many relationship management (assign/remove mechanics)
6. ✅ Proper error handling with 404 and validation errors
7. ✅ RESTful URL structure with proper prefixes
8. ✅ Complete Postman collection for testing
9. ✅ Comprehensive documentation (README.md)

## 📝 Assignment Requirements Checklist

- ✅ Blueprint folders created for customer, mechanic, and service_ticket
- ✅ Each blueprint has **init**.py, routes.py, and schemas.py
- ✅ Blueprints registered in app/**init**.py with URL prefixes
- ✅ Marshmallow schemas using SQLAlchemyAutoSchema
- ✅ Full CRUD routes for Mechanic resource
- ✅ Service Ticket routes with assign/remove mechanic functionality
- ✅ Postman collection exported and included
- ✅ All endpoints tested and working

## 🎓 Assignment Complete!

All requirements have been successfully implemented following Dylan's pattern from the previous videos.
