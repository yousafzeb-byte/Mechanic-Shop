from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
import os


def _normalize_base_url(value, default='localhost:5000'):
    if not value:
        return default
    normalized = value.strip().replace('http://', '').replace('https://', '')
    return normalized.rstrip('/')

# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Instantiate SQLAlchemy database
db = SQLAlchemy(model_class=Base)

# Instantiate Limiter for rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Instantiate Cache
cache = Cache()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default development configuration if no config provided
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Determine if we're in production based on environment or config
    is_production = os.getenv('FLASK_ENV') == 'production' or app.config.get('DEBUG') is False
    
    # Configure Swagger with dynamic host and scheme + custom styling
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api-docs/",
        "swagger_ui_config": {
            "docExpansion": "list",  # 'none', 'list', or 'full'
            "defaultModelsExpandDepth": 3,
            "defaultModelExpandDepth": 3,
            "displayRequestDuration": True,
            "filter": True,  # Enable search/filter box
            "showExtensions": True,
            "showCommonExtensions": True,
            "displayOperationId": False,
        }
    }
    
    # Swagger host must be the domain only (no scheme), e.g. api.example.com
    base_url = _normalize_base_url(os.getenv('BASE_URL'))
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "🔧 Mechanic Shop API",
            "description": """
## Welcome to Mechanic Shop API!

A comprehensive RESTful API for managing mechanic shop operations.

### Features:
- 👥 **Customer Management** - Register, login, and manage customer accounts
- 🔧 **Mechanic Management** - Track mechanics and their work assignments
- 🎫 **Service Tickets** - Create and manage service requests
- 📦 **Inventory Management** - Track parts and supplies
- 🔐 **JWT Authentication** - Secure API access with token-based auth
- ⚡ **Rate Limiting** - Built-in API rate limiting for security
- 💾 **Caching** - Optimized performance with intelligent caching

### Getting Started:
1. Register a customer account using `POST /customers/`
2. Login to receive a JWT token using `POST /customers/login`
3. Use the token in Authorization header: `Bearer {your-token}`
4. Explore the API endpoints below!

### Authentication:
Click the **Authorize** button (🔓) and enter: `Bearer {your-token}`
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Mechanic Shop Team",
                "url": "https://github.com/yousafzeb-byte/Mechanic-Shop"
            }
        },
        "host": base_url,
        "schemes": ["https" if is_production else "http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "tags": [
            {"name": "Customers", "description": "👥 Customer management endpoints - Registration, login, profile management"},
            {"name": "Mechanics", "description": "🔧 Mechanic management endpoints - Create and manage mechanic profiles"},
            {"name": "Service Tickets", "description": "🎫 Service ticket management - Create, assign, and track service requests"},
            {"name": "Inventory", "description": "📦 Inventory management - Track parts, supplies, and stock levels"}
        ]
    }
    
    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Enable CORS for all routes with explicit configuration
    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=True)
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Import and register blueprints
    from app.blueprints.customer import customer_bp
    from app.blueprints.mechanic import mechanic_bp
    from app.blueprints.service_ticket import service_ticket_bp
    from app.blueprints.inventory import inventory_bp
    
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    # Homepage route - redirect to API documentation
    @app.route('/')
    def index():
        """Redirect root URL to Swagger API documentation"""
        return redirect('/api-docs/')
    
    return app
