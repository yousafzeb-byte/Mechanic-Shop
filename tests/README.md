# Testing Guide for Mechanic Shop API

## Overview

This directory contains comprehensive unit tests for all API endpoints using Python's built-in `unittest` framework.

## Test Files

- `test_customers.py` - Tests for Customer blueprint (22 tests)
- `test_mechanics.py` - Tests for Mechanic blueprint (13 tests)
- `test_service_tickets.py` - Tests for Service Ticket blueprint (19 tests)
- `test_inventory.py` - Tests for Inventory blueprint (17 tests)

**Total: 71+ test cases covering positive and negative scenarios**

## Setup

### 1. Create Test Database

```bash
python create_test_database.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

```bash
python -m unittest discover tests
```

### Run Specific Test File

```bash
python -m unittest tests.test_customers
python -m unittest tests.test_mechanics
python -m unittest tests.test_service_tickets
python -m unittest tests.test_inventory
```

### Run Specific Test Class

```bash
python -m unittest tests.test_customers.TestCustomerBlueprint
```

### Run Specific Test Method

```bash
python -m unittest tests.test_customers.TestCustomerBlueprint.test_login_success
```

### Run with Verbose Output

```bash
python -m unittest discover tests -v
```

## Test Coverage

### Customer Tests

- ✅ Create customer (positive & negative)
- ✅ Get all customers with pagination
- ✅ Get customer by ID
- ✅ Login with valid/invalid credentials
- ✅ Get my tickets with/without token
- ✅ Update customer (authorized & unauthorized)
- ✅ Delete customer (authorized & unauthorized)
- ✅ Rate limiting enforcement
- ✅ Validation errors
- ✅ Not found errors

### Mechanic Tests

- ✅ Create mechanic
- ✅ Get all mechanics
- ✅ Get mechanic by ID
- ✅ Get mechanics by ticket count (advanced query)
- ✅ Update mechanic
- ✅ Delete mechanic
- ✅ Missing required fields
- ✅ Invalid data types
- ✅ Duplicate email constraint

### Service Ticket Tests

- ✅ Create service ticket
- ✅ Get all service tickets
- ✅ Get service ticket by ID
- ✅ Assign/remove mechanic
- ✅ Bulk edit mechanics
- ✅ Add inventory parts to tickets
- ✅ Delete service ticket
- ✅ Invalid customer reference
- ✅ Duplicate assignment prevention
- ✅ Not found errors

### Inventory Tests

- ✅ Create inventory part
- ✅ Get all inventory
- ✅ Get inventory by ID
- ✅ Update inventory (full & partial)
- ✅ Delete inventory
- ✅ Multiple parts creation
- ✅ Missing required fields
- ✅ Invalid price types
- ✅ Edge cases (zero price, negative price)

## Test Database

Tests use a separate test database (`mechanic_shop_test`) to avoid interfering with development data.

The test database is automatically:

- Created before test class execution (`setUpClass`)
- Cleaned after each test (`tearDown`)
- Dropped after all tests complete (`tearDownClass`)

## Expected Output

Successful test run:

```
...................................................................
----------------------------------------------------------------------
Ran 71 tests in 45.234s

OK
```

## Notes

- Tests are independent and can be run in any order
- Each test cleans up its own data
- Negative tests verify proper error handling
- Tests cover authentication, authorization, and validation
- Rate limiting tests may take longer due to actual rate limiting
