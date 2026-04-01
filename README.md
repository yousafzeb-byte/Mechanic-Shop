# Mechanic Shop API - Flask | Python | MySQL | CI/CD Pipeline

[![Flask](https://img.shields.io/badge/Flask-3.1.2-black)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://www.mysql.com/)
[![CI](https://github.com/yousafzeb-byte/Mechanic-Shop/actions/workflows/main.yaml/badge.svg)](https://github.com/yousafzeb-byte/Mechanic-Shop/actions/workflows/main.yaml)

## 🎯 Project: Advanced API Development

This project implements a complete RESTful API for a Mechanic Shop with advanced features including:

## Recruiter Snapshot

- Built a production-style Flask API with authentication, authorization, caching, rate limiting, and OpenAPI docs.
- Implemented 27 documented endpoints across Customers, Mechanics, Service Tickets, and Inventory resources.
- Wrote 71 automated tests covering positive and negative flows, auth guards, and business rules.
- Added CI/CD automation and deployment configuration for cloud hosting.

## Architecture At A Glance

- Application Factory pattern for environment-specific app creation and testability.
- Blueprint-based route modules for clear domain separation.
- SQLAlchemy models for relational entities and many-to-many junction tables.
- Marshmallow validation/serialization to enforce request and response contracts.
- Token-based auth decorator to secure protected routes.

## Visual Showcase

Add screenshots and demo GIFs under `docs/media/` to make this project faster to evaluate for recruiters.

```md
![Swagger Docs](docs/media/swagger-docs.png)
![JWT Auth Flow](docs/media/jwt-auth-flow.gif)
![Postman Collection Run](docs/media/postman-collection.png)
```

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

### 📖 Documentation & Testing (NEW)

- **Swagger/OpenAPI Documentation**: Interactive API documentation with Flasgger
  - All 27 endpoints documented with request/response schemas
  - JWT authentication support in Swagger UI
  - Accessible at `/api-docs/`
- **Comprehensive Unit Tests**: 71 tests covering all endpoints
  - Positive and negative test cases
  - Separate test database configuration
  - Tests for authentication, authorization, validation, and business logic
  - Coverage for all CRUD operations and advanced features

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
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide with CI/CD setup (NEW)

### 📖 Swagger/OpenAPI Documentation

This API includes interactive Swagger documentation powered by Flasgger:

- **Swagger UI**: `http://localhost:5000/api-docs/` (local) or `https://your-app-url/api-docs/` (production)
- **OpenAPI Spec**: `http://localhost:5000/apispec.json`

The Swagger UI provides:

- ✅ Interactive API documentation for all 27 endpoints
- ✅ Try-it-out functionality to test endpoints directly
- ✅ Request/response examples with proper schemas
- ✅ JWT Bearer token authentication support (click "Authorize" button)
- ✅ Organized by tags: Customers, Mechanics, Service Tickets, Inventory

**To use protected endpoints in Swagger:**

1. Login via `POST /customers/login` endpoint
2. Copy the returned token
3. Click the "Authorize" button at the top right
4. Enter: `Bearer <your-token-here>`
5. Click "Authorize" and then "Close"
6. All protected endpoints will now include the token automatically

## 🧪 Unit Testing

This project includes comprehensive unit tests covering all endpoints:

### Running Tests

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_customers -v

# Run specific test
python -m unittest tests.test_customers.TestCustomerBlueprint.test_login_success -v
```

### Test Coverage

- **71 total tests** covering all 27 API endpoints
- **Positive tests**: Verify successful operations
- **Negative tests**: Verify error handling and validation
- **Test database**: Uses separate `mechanic_shop_test` database

#### Test Breakdown by Blueprint

- **Customers** (22 tests):
  - Authentication (login, tokens)
  - Authorization (protected routes)
  - Rate limiting validation
  - Pagination functionality
  - Email validation
  - CRUD operations

- **Mechanics** (13 tests):
  - CRUD operations
  - Email uniqueness validation
  - Advanced queries (ranking by tickets)
  - Data type validation

- **Service Tickets** (19 tests):
  - CRUD operations
  - Mechanic assignment/removal (many-to-many)
  - Inventory part management
  - Bulk editing mechanics
  - Foreign key constraint validation

- **Inventory** (17 tests):
  - CRUD operations
  - Price validation (type checking)
  - Partial updates
  - Edge cases (zero/negative prices)

### Setting Up Test Database

```bash
# Create test database
python create_test_database.py
```

This creates a separate `mechanic_shop_test` database to avoid interfering with development data.

### Test Best Practices

- Each test is independent (setUp/tearDown handle cleanup)
- Junction tables cleared before main tables (proper foreign key handling)
- Both success and failure scenarios tested
- Token authentication tested thoroughly
- Database constraints validated

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
- **Flasgger 0.9.7.1** - Swagger/OpenAPI documentation (NEW)
- **unittest** - Python built-in testing framework (NEW)
- **MySQL Connector** - Database driver

## 📁 Project Structure

```
Mechanic Shop/
├── app/
│   ├── __init__.py           # App factory with rate limiting, caching & Swagger
│   ├── models.py             # Database models (includes Inventory)
│   ├── utils.py              # Token auth utilities
│   └── blueprints/
│       ├── customer/         # Customer routes (auth, pagination, Swagger docs)
│       ├── mechanic/         # Mechanic routes (advanced queries, Swagger docs)
│       ├── service_ticket/   # Service ticket routes (Swagger docs)
│       └── inventory/        # Inventory routes (Swagger docs)
├── tests/                    # Unit tests (NEW)
│   ├── __init__.py           # Test package initialization
│   ├── test_customers.py     # Customer endpoint tests (22 tests)
│   ├── test_mechanics.py     # Mechanic endpoint tests (13 tests)
│   ├── test_service_tickets.py # Service ticket tests (19 tests)
│   ├── test_inventory.py     # Inventory endpoint tests (17 tests)
│   └── README.md             # Testing documentation
├── requirements.txt          # Updated with Flasgger
├── create_test_database.py   # Test database setup script (NEW)
├── update_database.py        # Database update script
├── populate_database.py      # Sample data script
├── API_DOCUMENTATION.md      # Complete API docs
└── Mechanic_Shop_Advanced_API.postman_collection.json
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

### Documentation & Testing

- ✅ Swagger/OpenAPI documentation for all 27 endpoints
- ✅ 71 comprehensive unit tests (positive and negative)
- ✅ Separate test database configuration
- ✅ Complete API documentation

### Deployment & CI/CD

- ✅ Production configuration with environment variables
- ✅ PostgreSQL support for Render deployment
- ✅ Gunicorn production server
- ✅ GitHub Actions CI/CD pipeline
- ✅ Automated testing on push
- ✅ Automated deployment to Render
- ✅ Dynamic Swagger configuration (http/https)

## 🚀 Production Deployment

This project is deployment-ready with full CI/CD pipeline support!

### Quick Deploy to Render

1. **Database**: Create PostgreSQL database on Render
2. **Web Service**: Deploy from your GitHub repository
3. **Environment Variables**: Set `DATABASE_URI`, `SECRET_KEY`, `FLASK_ENV=production`, `BASE_URL`
4. **CI/CD**: Add GitHub secrets (`RENDER_API_KEY`, `SERVICE_ID`)
5. **Done**: Auto-deploy on every push to main!

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step deployment guide.**

### CI/CD Pipeline Features

- ✅ **Build Job**: Python syntax validation
- ✅ **Test Job**: Runs all 71 unit tests with MySQL service
- ✅ **Deploy Job**: Auto-deploys to Render on successful tests
- ✅ **Workflow**: Triggered on push/PR to main branch

### Production Features

- **Configuration Management**: Separate dev/test/production configs
- **Environment Variables**: Secure credential management with `.env`
- **Database Support**: MySQL (development) + PostgreSQL (production)
- **Production Server**: Gunicorn WSGI server
- **Auto-scaling**: Ready for Render's scaling features
- **HTTPS**: Automatic SSL/TLS in production

## 🔒 Security Notes

⚠️ **Important:** Sensitive data is managed via environment variables in production!

**Secret Key Management:**

- Development: Set in `.env` file (not committed)
- Production: Set in Render environment variables
- Generate secure key: `python -c "import secrets; print(secrets.token_hex(32))"`

**Database Credentials:**

- Never commit database passwords to version control
- Use `.env` for local development (in `.gitignore`)
- Use Render environment variables for production

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
