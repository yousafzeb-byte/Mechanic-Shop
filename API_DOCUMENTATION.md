# Mechanic Shop API - Advanced Features Documentation

## Overview

This API now includes advanced features such as Rate Limiting, Token Authentication, Caching, Pagination, and Advanced Queries. A new Inventory resource has also been added.

## Setup Instructions

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

## New Features

### 🔐 Token Authentication

- JWT tokens are used to authenticate customers
- Tokens expire after 24 hours
- Protected routes require a Bearer token in the Authorization header

### ⏱️ Rate Limiting

- Default rate limits: 200 requests per day, 50 per hour
- Customer creation endpoint: 5 requests per minute
- Protects against API abuse

### 💾 Caching

- GET all customers endpoint is cached for 60 seconds
- Improves performance for frequently accessed data

### 📄 Pagination

- GET all customers endpoint supports pagination
- Parameters: `page` (default: 1), `per_page` (default: 10)
- Returns pagination metadata

---

## API Endpoints

### Customers (`/customers`)

#### POST `/customers/` - Create New Customer

Creates a new customer account with hashed password.

**Rate Limit:** 5 per minute

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0101",
  "address": "123 Main St",
  "password": "securepassword"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0101",
  "address": "123 Main St"
}
```

_Note: Password is hashed and not returned_

---

#### POST `/customers/login` - Customer Login

Authenticates a customer and returns a JWT token.

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK`

```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "customer_id": 1
}
```

---

#### GET `/customers/my-tickets` - Get My Tickets

Returns all service tickets for the authenticated customer.

**🔒 Requires Authentication**

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "VIN": "1HGBH41JXMN109186",
    "description": "Oil change",
    "service_date": "2026-02-01",
    "customer_id": 1
  }
]
```

---

#### GET `/customers/` - Get All Customers (Paginated)

Returns a paginated list of all customers.

**💾 Cached for 60 seconds**

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Example:** `GET /customers/?page=2&per_page=5`

**Response:** `200 OK`

```json
{
    "customers": [...],
    "pagination": {
        "page": 2,
        "per_page": 5,
        "total": 50,
        "pages": 10,
        "has_next": true,
        "has_prev": true
    }
}
```

---

#### GET `/customers/<id>` - Get Customer by ID

Returns a specific customer.

**Response:** `200 OK`

---

#### PUT `/customers/<id>` - Update Customer

Updates a customer's information.

**🔒 Requires Authentication** (Can only update own account)

**Headers:**

```
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "name": "John Updated",
  "phone": "555-9999",
  "password": "newpassword"
}
```

**Response:** `200 OK`

---

#### DELETE `/customers/<id>` - Delete Customer

Deletes a customer account.

**🔒 Requires Authentication** (Can only delete own account)

**Headers:**

```
Authorization: Bearer <token>
```

**Response:** `200 OK`

---

### Mechanics (`/mechanics`)

#### POST `/mechanics/` - Create Mechanic

#### GET `/mechanics/` - Get All Mechanics

#### GET `/mechanics/<id>` - Get Mechanic by ID

#### PUT `/mechanics/<id>` - Update Mechanic

#### DELETE `/mechanics/<id>` - Delete Mechanic

Standard CRUD operations for mechanics.

---

#### GET `/mechanics/by-tickets` - Get Mechanics Ranked by Tickets

Returns mechanics ordered by the number of tickets they've worked on (descending).

**Response:** `200 OK`

```json
[
    {
        "id": 1,
        "name": "Mike Mechanic",
        "email": "mike@mechanicshop.com",
        "phone": "555-0201",
        "address": "100 Shop St",
        "salary": 65000.0,
        "ticket_count": 15
    },
    {
        "id": 2,
        "name": "Sarah Wrench",
        "ticket_count": 12
        ...
    }
]
```

---

### Service Tickets (`/service-tickets`)

#### POST `/service-tickets/` - Create Service Ticket

#### GET `/service-tickets/` - Get All Service Tickets

#### GET `/service-tickets/<id>` - Get Service Ticket by ID

#### DELETE `/service-tickets/<id>` - Delete Service Ticket

Standard CRUD operations for service tickets.

---

#### PUT `/service-tickets/<ticket_id>/edit` - Edit Ticket Mechanics

Add and/or remove mechanics from a service ticket in one request.

**Request Body:**

```json
{
  "add_ids": [1, 3],
  "remove_ids": [2]
}
```

**Response:** `200 OK`

```json
{
    "message": "Mechanics updated successfully",
    "service_ticket": { ... }
}
```

---

#### PUT `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>`

Assigns a mechanic to a service ticket.

**Response:** `200 OK`

---

#### PUT `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>`

Removes a mechanic from a service ticket.

**Response:** `200 OK`

---

#### PUT `/service-tickets/<ticket_id>/add-part/<part_id>` - Add Part to Ticket

Adds an inventory part to a service ticket.

**Response:** `200 OK`

```json
{
    "message": "Part 5 added to Service Ticket 3",
    "service_ticket": { ... }
}
```

---

### Inventory (`/inventory`) **NEW**

#### POST `/inventory/` - Create Inventory Part

Creates a new inventory part.

**Request Body:**

```json
{
  "name": "Oil Filter",
  "price": 12.99
}
```

**Response:** `201 Created`

---

#### GET `/inventory/` - Get All Inventory Parts

Returns all inventory parts.

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Oil Filter",
    "price": 12.99
  },
  {
    "id": 2,
    "name": "Brake Pads",
    "price": 89.99
  }
]
```

---

#### GET `/inventory/<id>` - Get Inventory Part by ID

Returns a specific inventory part.

**Response:** `200 OK`

---

#### PUT `/inventory/<id>` - Update Inventory Part

Updates an inventory part.

**Request Body:**

```json
{
  "name": "Premium Oil Filter",
  "price": 15.99
}
```

**Response:** `200 OK`

---

#### DELETE `/inventory/<id>` - Delete Inventory Part

Deletes an inventory part.

**Response:** `200 OK`

---

## Testing in Postman

### 1. Create a Customer

- POST to `/customers/`
- Save the customer ID for later

### 2. Login

- POST to `/customers/login` with email and password
- Copy the token from the response

### 3. Test Protected Routes

- For routes requiring authentication, add a header:
  - Key: `Authorization`
  - Value: `Bearer <paste_token_here>`

### 4. Test Pagination

- GET `/customers/?page=1&per_page=5`

### 5. Test Advanced Queries

- GET `/mechanics/by-tickets` to see mechanics ranked by tickets
- PUT `/service-tickets/1/edit` with add_ids and remove_ids

### 6. Test Inventory

- Create parts with POST `/inventory/`
- Add parts to tickets with PUT `/service-tickets/<ticket_id>/add-part/<part_id>`

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "Validation error message"
}
```

### 401 Unauthorized

```json
{
  "error": "Token is missing"
}
```

```json
{
  "error": "Invalid or expired token"
}
```

### 403 Forbidden

```json
{
  "error": "Unauthorized to update this customer"
}
```

### 404 Not Found

```json
{
  "error": "Customer not found"
}
```

### 429 Too Many Requests

```json
{
  "error": "Rate limit exceeded"
}
```

---

## Sample Test Data

After running `populate_database.py`, you can use these credentials:

**Test Customers:**

- **Email:** john@example.com | **Password:** password123
- **Email:** jane@example.com | **Password:** password123
- **Email:** bob@example.com | **Password:** password123

**Test Mechanics:** IDs 1, 2, 3

**Test Inventory Parts:** IDs 1-10

**Test Service Tickets:** IDs 1-5

---

## Database Schema Changes

### New Tables

- `inventory` - Stores parts/inventory items
- `service_inventory` - Junction table for Service Tickets ↔ Inventory (many-to-many)

### Modified Tables

- `customers` - Added `password` field (VARCHAR(255), hashed)

### Existing Tables

- `service_tickets`
- `mechanics`
- `service_mechanic` - Junction table for Service Tickets ↔ Mechanics

---

## Security Notes

⚠️ **Important:** The secret key in `app/utils.py` should be changed to a secure random string in production.

```python
SECRET_KEY = "your-secret-key-change-this-in-production"
```

Generate a secure key:

```python
import secrets
secrets.token_hex(32)
```

---

## Rate Limiting Configuration

Current limits (configured in `app/__init__.py`):

- Default: 200 per day, 50 per hour
- Customer creation: 5 per minute

To modify, edit the `limiter` initialization:

```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
```

---

## Assignment Completion Checklist

✅ Rate Limiting - Applied to customer creation endpoint and default limits
✅ Caching - Applied to GET customers endpoint
✅ Token Authentication - encode_token, decode_token, login route
✅ Token Required Decorator - Applied to protected routes
✅ Login Route - POST /customers/login
✅ My Tickets Route - GET /customers/my-tickets (protected)
✅ Protected Routes - Update and Delete customer require token
✅ Pagination - Applied to GET customers
✅ Advanced Queries - Edit mechanics route with add/remove IDs
✅ Mechanics Ranking - GET /mechanics/by-tickets
✅ Inventory Model - Created with many-to-many relationship
✅ Inventory Blueprint - Full CRUD operations
✅ Add Part to Ticket - PUT /service-tickets/<id>/add-part/<part_id>

---

## Additional Features Implemented

🎯 **Beyond Requirements:**

- Password hashing with bcrypt
- Authorization checks (customers can only modify their own accounts)
- Comprehensive error handling
- Detailed pagination metadata
- Sample data population script

---

**Happy Testing! 🚀**
