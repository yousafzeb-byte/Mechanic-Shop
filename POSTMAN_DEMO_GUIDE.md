# Postman Demonstration Guide

## For 5-Minute Video Presentation

This guide shows you exactly what to click in Postman during your video demo.

---

## **SETUP BEFORE RECORDING**

1. Open Postman
2. Import the collection: `Mechanic_Shop_Advanced_API.postman_collection.json`
3. Start your Flask server
4. Clean up test data (delete test1-test5 customers if they exist)
5. Arrange windows: Camera view in corner, Postman taking main screen

---

## **DEMO SEQUENCE (Use your imported collection)**

### **1. Rate Limiting Demo (20 seconds)**

**Request:** Create Customer (POST /customers/)

Click the request 5 times rapidly:

- Request 1: ✅ 201 Created
- Request 2: ✅ 201 Created
- Request 3: ✅ 201 Created
- Request 4: ✅ 201 Created
- Request 5: ✅ 201 Created
- Request 6: ❌ **429 Too Many Requests**

**What to say:** "The rate limiter allows 5 customer creations per minute. The 6th request is blocked to prevent abuse."

---

### **2. Authentication Flow (40 seconds)**

#### Step A: Login

**Request:** Login Customer (POST /customers/login)

Body should have:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Click SEND** → You'll get a response with a token

**What to say:** "When logging in with valid credentials, the customer receives a JWT token that expires in 24 hours."

#### Step B: Copy Token

- Highlight and copy the token from the response
- Show the token value briefly

#### Step C: Use Token for Protected Route

**Request:** Get My Tickets (GET /customers/my-tickets)

- Go to the **Headers** tab
- Show the Authorization header: `Bearer [token]`
- **Click SEND** → You'll see the customer's tickets

**What to say:** "Using this token in the Authorization header, customers can access their personal service tickets. Without it, access is denied."

---

### **3. Advanced Query - Mechanics Ranked by Workload (25 seconds)**

**Request:** Get Mechanics by Tickets (GET /mechanics/by-tickets)

**Click SEND** → Shows mechanics sorted by ticket count

**What to say:** "This advanced SQL query aggregates and ranks mechanics by workload. Mike has 3 tickets, Sarah and Tom each have 2. This helps balance work distribution."

**Point out in response:**

```json
{
  "name": "Mike Mechanic",
  "ticket_count": 3
}
```

---

### **4. Pagination (20 seconds)**

**Request:** Get Customers with Pagination (GET /customers/?page=1&per_page=5)

**Click SEND** → Show pagination metadata

**What to say:** "Pagination prevents overwhelming responses. Here's page 1 with 5 items per page."

**Point out in response:**

```json
"pagination": {
    "page": 1,
    "per_page": 5,
    "total": 8,
    "pages": 2,
    "has_next": true,
    "has_prev": false
}
```

---

### **5. Inventory & Many-to-Many Relationships (30 seconds)**

#### Step A: View Inventory

**Request:** Get All Inventory (GET /inventory/)

**Click SEND** → Shows parts list with prices

**What to say:** "The inventory tracks all parts with pricing - oil filters, brake pads, batteries, etc."

#### Step B: Add Part to Service Ticket

**Request:** Add Part to Ticket (PUT /service-tickets/1/add-part/3)

**Click SEND** → Shows success message

**What to say:** "I'm adding spark plugs to service ticket 1. The many-to-many relationship allows multiple parts per ticket."

---

### **6. Bulk Mechanic Assignment (30 seconds)**

**Request:** Edit Ticket Mechanics (PUT /service-tickets/3/edit)

Body:

```json
{
  "remove_ids": [1],
  "add_ids": [2, 3]
}
```

**Click SEND** → Shows updated ticket

**What to say:** "This advanced endpoint performs bulk operations - removing mechanic 1 and adding mechanics 2 and 3 in a single request, demonstrating efficient relationship management."

---

### **7. Caching (Optional - 15 seconds if time permits)**

**Request:** Get All Customers (GET /customers/)

- **First click SEND** (uncached - normal speed)
- **Immediately click SEND again** (cached - faster)

**What to say:** "The first request queries the database, but responses are cached for 60 seconds. Subsequent requests are served from cache, improving performance."

---

## **POSTMAN TIPS**

### Make Responses Easy to Read:

1. Click **Beautify** button (if available)
2. Use **Pretty** view (not Raw)
3. Expand relevant JSON sections before recording
4. Increase font size (Settings → Font Size → 14-16)

### Visual Clarity:

- Close unnecessary tabs
- Full screen Postman for demos
- Highlight important parts of JSON responses with cursor
- Use the status code (200, 201, 429) to emphasize points

### Time Management:

- Have all requests pre-arranged in order
- Don't wait for long responses - they're fast
- Skip typing - use saved requests from collection
- Practice clicking through the sequence 2-3 times

---

## **IF SOMETHING GOES WRONG**

**Token expired?**

- Just run the Login request again and copy new token

**Rate limit hit?**

- Wait 1 minute OR restart the Flask server

**Server not responding?**

- Check terminal - server should show requests coming in
- Restart with: `& "D:/Mechanic Shop/venv/Scripts/python.exe" run.py`

**Wrong response?**

- Check your collection is up to date
- Verify request method (GET vs POST vs PUT)

---

## **CAMERA + SCREEN RECORDING TOOLS**

**Option 1: Zoom (Recommended)**

- Start a meeting with yourself
- Share screen
- Enable "Side by side mode" in View Options
- Record to computer

**Option 2: OBS Studio (Free)**

- Add Video Capture Device (your camera)
- Add Display Capture (your screen)
- Arrange camera as small overlay in corner
- Hit Record

**Option 3: Microsoft Teams**

- Start a meeting
- Share screen
- Turn on camera
- Record

**Option 4: Loom**

- Simple browser extension
- Automatically handles camera + screen
- Easy to use

---

## **FINAL CHECKLIST BEFORE RECORDING**

- [ ] Flask server is running
- [ ] Postman collection is imported and all requests work
- [ ] Camera angle is good, lighting is decent
- [ ] Audio is clear (test recording)
- [ ] Closed distracting windows/notifications
- [ ] Have script/outline visible (second monitor or printed)
- [ ] Tested the full demo flow at least once
- [ ] Timer ready (phone or online timer for 5 minutes)

**You've got this! 🎬**
