# Quick Testing Guide

## Setup (One-time)

1. **Update database:**

   ```bash
   python update_database.py
   ```

2. **Populate sample data:**

   ```bash
   python populate_database.py
   ```

3. **Start the API:**

   ```bash
   python run.py
   ```

4. **Import Postman collection:**
   - Open Postman
   - Import `Mechanic_Shop_Advanced_API.postman_collection.json`

## Test Workflow in Postman

### Step 1: Login to Get Token

1. Go to **Customers** → **Customer Login**
2. Use credentials:
   ```json
   {
     "email": "john@example.com",
     "password": "password123"
   }
   ```
3. Click **Send**
4. Token is automatically saved to environment variable `{{auth_token}}`

### Step 2: Test Protected Routes

All routes marked "(Auth Required)" will now work automatically using the saved token.

1. **Get My Tickets** - See tickets for logged-in customer
2. **Update Customer** - Modify your profile
3. **Delete Customer** - Delete your account (careful!)

### Step 3: Test Rate Limiting

1. Go to **Customers** → **Create Customer (Rate Limited)**
2. Click **Send** multiple times quickly
3. After 5 requests in a minute, you should see a rate limit error

### Step 4: Test Pagination

1. Go to **Customers** → **Get All Customers (Paginated & Cached)**
2. Try different page numbers and per_page values:
   - `?page=1&per_page=2`
   - `?page=2&per_page=2`
3. Notice the pagination metadata in the response

### Step 5: Test Caching

1. **First request** to **Get All Customers** - Check response time
2. **Second request** within 60 seconds - Should be faster (cached)
3. **Wait 61 seconds** - Cache expires, response time increases

### Step 6: Test Advanced Queries

#### Mechanics by Tickets

1. Go to **Mechanics** → **Get Mechanics by Tickets**
2. See mechanics ranked by number of tickets worked on
3. Notice the `ticket_count` field in each mechanic

#### Edit Ticket Mechanics

1. Go to **Service Tickets** → **Edit Ticket Mechanics**
2. Use this body to add/remove mechanics:
   ```json
   {
     "add_ids": [2, 3],
     "remove_ids": [1]
   }
   ```
3. Verify changes by getting the ticket

### Step 7: Test Inventory (NEW)

#### Create Inventory Part

1. Go to **Inventory** → **Create Inventory Part**
2. Create a new part:
   ```json
   {
     "name": "New Part",
     "price": 49.99
   }
   ```

#### Add Part to Ticket

1. Go to **Service Tickets** → **Add Part to Ticket**
2. Change URL to use ticket ID and part ID
3. Verify part was added by getting the ticket

## Testing Scenarios

### Scenario 1: New Customer Journey

1. Create customer
2. Login with credentials
3. View my tickets (empty initially)
4. Update profile
5. View updated profile

### Scenario 2: Service Ticket Management

1. Create service ticket
2. Assign mechanics to ticket
3. Add inventory parts to ticket
4. Edit mechanics (add/remove)
5. View completed ticket

### Scenario 3: Advanced Queries

1. Create multiple service tickets
2. Assign different mechanics
3. Get mechanics ranked by tickets
4. Verify counts are correct

### Scenario 4: Rate Limiting

1. Rapidly create customers
2. Hit rate limit
3. Wait for reset
4. Try again

## Sample Data Reference

### Customers (all with password: password123)

- ID 1: john@example.com
- ID 2: jane@example.com
- ID 3: bob@example.com

### Mechanics

- ID 1: Mike Mechanic
- ID 2: Sarah Wrench
- ID 3: Tom Tools

### Service Tickets

- ID 1-5: Various tickets with mechanics and parts assigned

### Inventory Parts

- ID 1: Oil Filter ($12.99)
- ID 2: Air Filter ($15.99)
- ID 3: Spark Plugs ($24.99)
- ID 4-10: Various other parts

## Common Issues

### Issue: "Token is missing" error

**Solution:** Make sure you logged in first. The token is saved automatically.

### Issue: "Unauthorized to update this customer"

**Solution:** You can only update/delete your own account. The customer_id from login must match the ID in the URL.

### Issue: Rate limit error

**Solution:** Wait a minute and try again.

### Issue: "Customer not found" after deletion

**Solution:** You deleted the customer. Create a new one or login with a different account.

## Testing All Features

Use this checklist to ensure all features work:

- [ ] Create customer (rate limited)
- [ ] Login and get token
- [ ] Get my tickets (with token)
- [ ] Get all customers (paginated)
- [ ] Update customer (with token)
- [ ] Delete customer (with token)
- [ ] Get mechanics by tickets
- [ ] Edit ticket mechanics (add/remove)
- [ ] Create inventory part
- [ ] Add part to ticket
- [ ] Test rate limiting
- [ ] Test caching (response times)
- [ ] Test pagination (different pages)

## Tips

1. **Environment Variables**: Postman automatically saves `auth_token` and `customer_id` after login
2. **Rate Limits**: If testing rate limits, use a tool to send many requests quickly
3. **Caching**: Use browser dev tools or Postman to see response times
4. **Pagination**: Try large `per_page` values to see all data
5. **Token Expiry**: Tokens expire after 24 hours - login again if needed

## Export Postman Collection

After testing:

1. In Postman, click the collection
2. Click the three dots → Export
3. Save as `Mechanic_Shop_Advanced_API.postman_collection.json`
4. Include in your project submission

---

**Happy Testing! 🧪**

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
