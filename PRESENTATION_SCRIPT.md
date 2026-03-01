# 5-Minute Video Presentation Script

## Mechanic Shop Advanced API

---

## **INTRO (30 seconds)**

_[Look at camera]_

"Hi! Today I'm presenting my Mechanic Shop API - a comprehensive RESTful API built with Flask that manages all aspects of a mechanic shop's operations including customer accounts, service tickets, mechanic assignments, and parts inventory."

---

## **WHAT IT DOES (45 seconds)**

_[Can show project structure in VS Code]_

"This API solves the problem of managing complex relationships in a service business. It handles:

- **Customer Management** - Secure account creation with password hashing and JWT authentication
- **Service Tickets** - Tracking repair jobs with vehicle information and service history
- **Mechanic Assignments** - Managing which mechanics work on which tickets through many-to-many relationships
- **Inventory Tracking** - Parts management with pricing and usage tracking
- **Security & Performance** - Rate limiting to prevent abuse, caching for better performance, and token-based authentication for protected routes"

---

## **HOW IT WORKS (1 minute)**

_[Can show models.py or architecture diagram]_

"The architecture uses:

**Backend Stack:**

- Flask framework with SQLAlchemy ORM
- MySQL database for data persistence
- Marshmallow for schema validation and serialization

**Key Technologies:**

- **Flask-Limiter** for rate limiting (default 200/day, 50/hour globally, plus route-specific limits)
- **Flask-Caching** for performance optimization
- **Python-JOSE** for JWT token generation and validation
- **Bcrypt** for secure password hashing

**Database Design:**

- Four main models: Customer, Mechanic, ServiceTicket, and Inventory
- Two junction tables for many-to-many relationships
- Service tickets can have multiple mechanics AND multiple parts

**Security:**

- All passwords are hashed with bcrypt before storage
- Token authentication protects sensitive routes
- Rate limiting prevents API abuse
- Token validation happens via a reusable decorator"

---

## **DEMONSTRATION (2.5 minutes)**

### **Setup (5 seconds)**

_[Show terminal/Postman ready]_

"Let me show you the API in action. I have the server running on localhost:5000."

---

### **Demo 1: Rate Limiting (20 seconds)**

```powershell
# Show this in terminal or Postman
POST http://127.0.0.1:5000/customers/
```

_[Execute 5 successful requests, then show 6th getting 429]_

"Here I'm testing the rate limiter - the first 5 customer creation requests succeed, but the 6th is blocked with HTTP 429 Too Many Requests. This protects against spam and abuse."

---

### **Demo 2: Authentication Flow (40 seconds)**

```powershell
POST http://127.0.0.1:5000/customers/login
Body: {"email": "john@example.com", "password": "password123"}
```

_[Show the response with JWT token]_

"Here's the authentication flow. When a customer logs in with valid credentials, they receive a JWT token. This token expires in 24 hours and contains the customer ID."

_[Copy token, then show protected route]_

```powershell
GET http://127.0.0.1:5000/customers/my-tickets
Header: Authorization: Bearer [paste token]
```

"Using this token in the Authorization header, customers can access their service tickets. Without a valid token, the request is rejected with 401 Unauthorized."

---

### **Demo 3: Advanced Query - Mechanics by Workload (25 seconds)**

```powershell
GET http://127.0.0.1:5000/mechanics/by-tickets
```

_[Show the response with ticket counts]_

"This advanced query uses SQL aggregation to rank mechanics by the number of tickets they've worked on. Mike has worked on 3 tickets, while Sarah and Tom each have 2. This helps managers balance workload distribution."

---

### **Demo 4: Pagination (20 seconds)**

```powershell
GET http://127.0.0.1:5000/customers/?page=1&per_page=5
```

_[Show pagination metadata in response]_

"Pagination prevents overwhelming responses. Here we see page 1 with 5 customers per page, and the metadata tells us there are 2 total pages with 8 customers. The API indicates has_next is true and has_prev is false."

---

### **Demo 5: Many-to-Many Relationships (30 seconds)**

**A) Inventory Management**

```powershell
GET http://127.0.0.1:5000/inventory/
```

_[Show parts list with prices]_

"The inventory tracks parts with prices. We have oil filters, brake pads, batteries, and more."

**B) Adding Parts to Tickets**

```powershell
PUT http://127.0.0.1:5000/service-tickets/2/add-part/8
```

_[Show success response]_

"I'm adding a battery to service ticket 2. The many-to-many relationship allows multiple parts on one ticket, and the same part type can be used across many tickets."

**C) Bulk Mechanic Assignment**

```powershell
PUT http://127.0.0.1:5000/service-tickets/3/edit
Body: {"add_ids": [2, 3], "remove_ids": [1]}
```

_[Show the update]_

"This advanced endpoint allows bulk operations - here I'm removing mechanic 1 and adding mechanics 2 and 3 to ticket 3 in a single request."

---

### **Demo 6: Caching Performance (15 seconds)**

_[Show two consecutive GET requests to /customers/]_

"The caching system stores GET customer responses for 60 seconds. Subsequent requests within that window are served from cache, reducing database load and improving response times."

---

## **CONCLUSION (30 seconds)**

_[Look at camera, maybe show Postman collection or GitHub]_

"To summarize, this API demonstrates production-ready techniques:

- ✅ JWT authentication for security
- ✅ Rate limiting for protection
- ✅ Caching for performance
- ✅ Pagination for scalability
- ✅ Advanced SQL queries for business intelligence
- ✅ Clean blueprint architecture for maintainability

All endpoints are documented and tested in the included Postman collection. The complete code is on GitHub. Thank you!"

---

## **QUICK REFERENCE: Commands to Run**

### Start Server (if not running)

```powershell
cd "D:\Mechanic Shop"
& "D:/Mechanic Shop/venv/Scripts/python.exe" run.py
```

### Test Authentication

```powershell
# Login
Invoke-WebRequest -Uri "http://127.0.0.1:5000/customers/login" -Method POST -Body (@{email="john@example.com"; password="password123"} | ConvertTo-Json) -ContentType "application/json" -UseBasicParsing

# Get my tickets (use token from login response)
Invoke-WebRequest -Uri "http://127.0.0.1:5000/customers/my-tickets" -Headers @{Authorization="Bearer YOUR_TOKEN_HERE"} -UseBasicParsing
```

### Test Rate Limiting

```powershell
1..6 | ForEach-Object {
    $num = $_
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:5000/customers/" -Method POST -Body (@{name="Test$num"; email="test$num@test.com"; phone="555-000$num"; address="Test"; password="pass123"} | ConvertTo-Json) -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
        Write-Host "Request $num`: Success"
    } catch {
        Write-Host "Request $num`: BLOCKED (429)"
    }
}
```

### Show Mechanics by Workload

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/mechanics/by-tickets" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Show Pagination

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/customers/?page=1&per_page=5" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Show Inventory

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/inventory/" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Bulk Edit Mechanics on Ticket

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/service-tickets/3/edit" -Method PUT -Body (@{remove_ids=@(1); add_ids=@(2,3)} | ConvertTo-Json) -ContentType "application/json" -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## **TOTAL TIME BREAKDOWN**

- Intro: 30s
- What it does: 45s
- How it works: 60s
- Demonstrations: 150s
- Conclusion: 30s
- **TOTAL: 4 minutes 45 seconds** (leaves 15s buffer)

---

## **TIPS FOR RECORDING**

1. **Camera Setup**: Make sure you're well-lit and camera is at eye level
2. **Screen Sharing**: Use Zoom/OBS/Teams to record yourself + screen simultaneously
3. **Practice**: Run through once to hit the 5-minute mark
4. **Energy**: Speak clearly and enthusiastically
5. **Backup**: Have Postman as backup if terminal commands fail
6. **Cleanup**: Delete test customers before recording (test1-test5 from rate limit demo)
7. **Pre-load**: Have all URLs/commands ready in a text file to copy-paste
8. **Server**: Ensure server is running before you start recording

Good luck! 🎥
