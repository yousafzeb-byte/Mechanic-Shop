"""
Flask Application Entry Point for Production Deployment
This file is used by Gunicorn and Render for production deployment.
For local development, continue using run.py
"""
import os
from app import create_app, db
from config import ProductionConfig, DevelopmentConfig

# Select configuration based on environment
config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig

# Create the Flask application
app = create_app(config_class)

# Optional table creation on boot (disabled by default in production)
run_db_create_on_boot = os.getenv('RUN_DB_CREATE_ON_BOOT', 'false').lower() == 'true'
if run_db_create_on_boot:
    with app.app_context():
        db.create_all()

# Note: In production, Gunicorn will run the app
# No need for app.run() here
