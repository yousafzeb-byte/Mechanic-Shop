from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

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
    
    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
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
