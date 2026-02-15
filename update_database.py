from app import create_app, db
from app.models import Customer, ServiceTicket, Mechanic, Inventory

# Create the Flask app
app = create_app()

with app.app_context():
    # Drop all existing tables
    print("Dropping all tables...")
    db.drop_all()
    
    # Create all tables with the new schema
    print("Creating all tables...")
    db.create_all()
    
    print("Database updated successfully!")
    print("\nNew tables created:")
    print("- customers (with password field)")
    print("- service_tickets")
    print("- mechanics")
    print("- inventory (NEW)")
    print("- service_mechanic (junction table)")
    print("- service_inventory (junction table - NEW)")
