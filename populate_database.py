from app import create_app, db
from app.models import Customer, ServiceTicket, Mechanic, Inventory
from app.utils import hash_password
from datetime import date

# Create the Flask app
app = create_app()

with app.app_context():
    print("Populating database with sample data...")
    
    # Create sample customers with hashed passwords
    customers = [
        Customer(
            name="John Doe",
            email="john@example.com",
            phone="555-0101",
            address="123 Main St, City, ST 12345",
            password=hash_password("password123")
        ),
        Customer(
            name="Jane Smith",
            email="jane@example.com",
            phone="555-0102",
            address="456 Oak Ave, City, ST 12345",
            password=hash_password("password123")
        ),
        Customer(
            name="Bob Johnson",
            email="bob@example.com",
            phone="555-0103",
            address="789 Pine Rd, City, ST 12345",
            password=hash_password("password123")
        )
    ]
    
    for customer in customers:
        db.session.add(customer)
    
    db.session.commit()
    print(f"Added {len(customers)} customers")
    
    # Create sample mechanics
    mechanics = [
        Mechanic(
            name="Mike Mechanic",
            email="mike@mechanicshop.com",
            phone="555-0201",
            address="100 Shop St, City, ST 12345",
            salary=65000.00
        ),
        Mechanic(
            name="Sarah Wrench",
            email="sarah@mechanicshop.com",
            phone="555-0202",
            address="101 Shop St, City, ST 12345",
            salary=72000.00
        ),
        Mechanic(
            name="Tom Tools",
            email="tom@mechanicshop.com",
            phone="555-0203",
            address="102 Shop St, City, ST 12345",
            salary=68000.00
        )
    ]
    
    for mechanic in mechanics:
        db.session.add(mechanic)
    
    db.session.commit()
    print(f"Added {len(mechanics)} mechanics")
    
    # Create sample inventory parts
    inventory_parts = [
        Inventory(name="Oil Filter", price=12.99),
        Inventory(name="Air Filter", price=15.99),
        Inventory(name="Spark Plugs (set of 4)", price=24.99),
        Inventory(name="Brake Pads (front)", price=89.99),
        Inventory(name="Brake Pads (rear)", price=79.99),
        Inventory(name="Wiper Blades (pair)", price=19.99),
        Inventory(name="Serpentine Belt", price=34.99),
        Inventory(name="Battery", price=149.99),
        Inventory(name="Transmission Fluid (quart)", price=8.99),
        Inventory(name="Coolant (gallon)", price=12.99)
    ]
    
    for part in inventory_parts:
        db.session.add(part)
    
    db.session.commit()
    print(f"Added {len(inventory_parts)} inventory parts")
    
    # Create sample service tickets
    service_tickets = [
        ServiceTicket(
            VIN="1HGBH41JXMN109186",
            description="Oil change and filter replacement",
            service_date=date(2026, 2, 1),
            customer_id=1
        ),
        ServiceTicket(
            VIN="1HGBH41JXMN109186",
            description="Brake pad replacement (front and rear)",
            service_date=date(2026, 2, 5),
            customer_id=1
        ),
        ServiceTicket(
            VIN="2HGFC2F59KH542891",
            description="Battery replacement and diagnostic",
            service_date=date(2026, 2, 10),
            customer_id=2
        ),
        ServiceTicket(
            VIN="3VWFE21C04M000001",
            description="Spark plug replacement and tune-up",
            service_date=date(2026, 2, 12),
            customer_id=3
        ),
        ServiceTicket(
            VIN="2HGFC2F59KH542891",
            description="Transmission fluid change",
            service_date=date(2026, 2, 14),
            customer_id=2
        )
    ]
    
    for ticket in service_tickets:
        db.session.add(ticket)
    
    db.session.commit()
    print(f"Added {len(service_tickets)} service tickets")
    
    # Assign mechanics to tickets
    service_tickets[0].mechanics.extend([mechanics[0]])  # Mike works on ticket 1
    service_tickets[1].mechanics.extend([mechanics[0], mechanics[1]])  # Mike and Sarah work on ticket 2
    service_tickets[2].mechanics.extend([mechanics[2]])  # Tom works on ticket 3
    service_tickets[3].mechanics.extend([mechanics[1]])  # Sarah works on ticket 4
    service_tickets[4].mechanics.extend([mechanics[0], mechanics[2]])  # Mike and Tom work on ticket 5
    
    # Add parts to tickets
    service_tickets[0].inventory_parts.extend([inventory_parts[0]])  # Oil filter for oil change
    service_tickets[1].inventory_parts.extend([inventory_parts[3], inventory_parts[4]])  # Brake pads
    service_tickets[2].inventory_parts.extend([inventory_parts[7]])  # Battery
    service_tickets[3].inventory_parts.extend([inventory_parts[2]])  # Spark plugs
    service_tickets[4].inventory_parts.extend([inventory_parts[8]])  # Transmission fluid
    
    db.session.commit()
    print("Assigned mechanics and parts to service tickets")
    
    print("\nDatabase populated successfully!")
    print("\nTest Login Credentials:")
    print("Email: john@example.com | Password: password123")
    print("Email: jane@example.com | Password: password123")
    print("Email: bob@example.com | Password: password123")
