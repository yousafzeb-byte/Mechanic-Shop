# Testing Guide - Mechanic Shop API

## Quick Test Flow

### 1. Import Postman Collection

1. Open Postman
2. Click "Import" button
3. Select `Mechanic_Shop_API.postman_collection.json`
4. All endpoints will be loaded and ready to test

### 2. Test Sequence (Follow this order)

#### Step 1: Create a Customer

**Endpoint:** `POST http://127.0.0.1:5000/customers/`

**Body:**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234",
  "address": "123 Main St, Springfield"
}
```

**Expected Response:** 201 Created

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234",
  "address": "123 Main St, Springfield"
}
```

#### Step 2: Create Mechanics

**Endpoint:** `POST http://127.0.0.1:5000/mechanics/`

**Body (Mechanic 1):**

```json
{
  "name": "Mike Johnson",
  "email": "mike.johnson@mechanicshop.com",
  "phone": "555-5678",
  "address": "456 Elm St, Springfield",
  "salary": 55000.0
}
```

**Body (Mechanic 2):**

```json
{
  "name": "Sarah Williams",
  "email": "sarah.williams@mechanicshop.com",
  "phone": "555-9012",
  "address": "789 Oak Ave, Springfield",
  "salary": 60000.0
}
```

**Expected Response:** 201 Created (for each)

#### Step 3: Create a Service Ticket

**Endpoint:** `POST http://127.0.0.1:5000/service-tickets/`

**Body:**

```json
{
  "VIN": "1HGBH41JXMN109186",
  "description": "Oil change, tire rotation, and brake inspection",
  "service_date": "2026-02-01",
  "customer_id": 1
}
```

**Expected Response:** 201 Created

```json
{
  "id": 1,
  "VIN": "1HGBH41JXMN109186",
  "description": "Oil change, tire rotation, and brake inspection",
  "service_date": "2026-02-01",
  "customer_id": 1
}
```

#### Step 4: Assign Mechanics to Service Ticket

**Endpoint 1:** `PUT http://127.0.0.1:5000/service-tickets/1/assign-mechanic/1`

**Expected Response:** 200 OK

```json
{
    "message": "Mechanic 1 assigned to Service Ticket 1",
    "service_ticket": { ... }
}
```

**Endpoint 2:** `PUT http://127.0.0.1:5000/service-tickets/1/assign-mechanic/2`

**Expected Response:** 200 OK

```json
{
    "message": "Mechanic 2 assigned to Service Ticket 1",
    "service_ticket": { ... }
}
```

#### Step 5: Verify Relationships

**Get Service Ticket:** `GET http://127.0.0.1:5000/service-tickets/1`

- Should show the service ticket with both mechanics assigned

**Get All Customers:** `GET http://127.0.0.1:5000/customers/`

- Should show all customers with their service tickets

**Get All Mechanics:** `GET http://127.0.0.1:5000/mechanics/`

- Should show all mechanics with their assigned service tickets

#### Step 6: Test Update Operations

**Update Customer:** `PUT http://127.0.0.1:5000/customers/1`

```json
{
  "phone": "555-9999"
}
```

**Update Mechanic:** `PUT http://127.0.0.1:5000/mechanics/1`

```json
{
  "salary": 58000.0
}
```

#### Step 7: Test Remove Mechanic

**Endpoint:** `PUT http://127.0.0.1:5000/service-tickets/1/remove-mechanic/2`

**Expected Response:** 200 OK

```json
{
    "message": "Mechanic 2 removed from Service Ticket 1",
    "service_ticket": { ... }
}
```

#### Step 8: Test Delete Operations (Optional)

⚠️ **Warning:** These will delete data from the database

**Delete Service Ticket:** `DELETE http://127.0.0.1:5000/service-tickets/1`

**Delete Mechanic:** `DELETE http://127.0.0.1:5000/mechanics/1`

**Delete Customer:** `DELETE http://127.0.0.1:5000/customers/1`

## Common Test Scenarios

### Test Error Handling

1. **Try to get non-existent resource:**
   - `GET http://127.0.0.1:5000/customers/999`
   - Expected: 404 Not Found

2. **Try to assign same mechanic twice:**
   - `PUT http://127.0.0.1:5000/service-tickets/1/assign-mechanic/1` (twice)
   - Expected: 400 Bad Request with message "Mechanic already assigned"

3. **Try to remove unassigned mechanic:**
   - `PUT http://127.0.0.1:5000/service-tickets/1/remove-mechanic/3`
   - Expected: 400 Bad Request with message "Mechanic is not assigned"

4. **Try to create customer with duplicate email:**
   - Create two customers with same email
   - Expected: Database constraint error

## Verification Checklist

✅ **Customer Endpoints:**

- [ ] Create customer
- [ ] Get all customers
- [ ] Get customer by ID
- [ ] Update customer
- [ ] Delete customer

✅ **Mechanic Endpoints:**

- [ ] Create mechanic
- [ ] Get all mechanics
- [ ] Get mechanic by ID
- [ ] Update mechanic
- [ ] Delete mechanic

✅ **Service Ticket Endpoints:**

- [ ] Create service ticket
- [ ] Get all service tickets
- [ ] Get service ticket by ID
- [ ] Assign mechanic to ticket
- [ ] Remove mechanic from ticket
- [ ] Delete service ticket

✅ **Relationship Tests:**

- [ ] One customer can have multiple service tickets
- [ ] One service ticket has one customer
- [ ] One service ticket can have multiple mechanics
- [ ] One mechanic can work on multiple service tickets

## Tips for Testing

1. **Use Postman Environment Variables:**
   - Save IDs from responses to use in subsequent requests
   - Example: `{{customer_id}}`, `{{mechanic_id}}`, `{{ticket_id}}`

2. **Test in Order:**
   - Always create resources before trying to use them
   - Create Customer → Create Mechanics → Create Service Tickets → Assign Mechanics

3. **Check Database:**
   - Use MySQL Workbench to verify data is being stored correctly
   - Run: `SELECT * FROM customers;`, `SELECT * FROM mechanics;`, etc.

4. **Monitor Console:**
   - Watch the Flask console for any errors or warnings
   - SQL queries will be logged if you enable SQLAlchemy echo mode

## Running the Server

Make sure the Flask server is running:

```bash
python run.py
```

You should see:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Happy Testing! 🚀
