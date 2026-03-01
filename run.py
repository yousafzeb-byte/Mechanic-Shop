"""
Local Development Server
Use this file for local development only.
For production deployment, use flask_app.py with Gunicorn.
"""
from app import create_app, db
from config import DevelopmentConfig

# Create app with development configuration
app = create_app(DevelopmentConfig)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
