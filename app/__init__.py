from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
import os

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
    
    # Configure Swagger with dynamic host and scheme
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
        "specs_route": "/api-docs/"
    }
    
    # Get the base URL from environment variable or use localhost for development
    base_url = os.getenv('BASE_URL', 'localhost:5000')
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Mechanic Shop API",
            "description": "A comprehensive RESTful API for managing mechanic shop operations including customers, mechanics, service tickets, and inventory",
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
            {"name": "Customers", "description": "Customer management endpoints"},
            {"name": "Mechanics", "description": "Mechanic management endpoints"},
            {"name": "Service Tickets", "description": "Service ticket management endpoints"},
            {"name": "Inventory", "description": "Inventory management endpoints"}
        ]
    }
    
    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    CORS(app)  # Enable CORS for all routes
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
