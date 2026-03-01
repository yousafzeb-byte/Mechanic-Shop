from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import Swagger

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

def create_app():
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:112233@localhost/mechanic_shop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure caching
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    
    # Configure Swagger
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
    
    return app
