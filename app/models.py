from app import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from datetime import date

# Many-to-Many association table for Service_Tickets and Mechanics
service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

# Many-to-Many association table for Service_Tickets and Inventory
service_inventory = db.Table(
    'service_inventory',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('inventory_id', db.ForeignKey('inventory.id'))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    address: Mapped[str] = mapped_column(db.String(500), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # One-to-Many relationship: One customer can have many service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    description: Mapped[str] = mapped_column(db.String(1000), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    # Relationship back to Customer (Many-to-One)
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    
    # Many-to-Many relationship: A service ticket can have multiple mechanics
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanic, back_populates='service_tickets')
    
    # Many-to-Many relationship: A service ticket can have multiple inventory parts
    inventory_parts: Mapped[List['Inventory']] = db.relationship(secondary=service_inventory, back_populates='service_tickets')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    address: Mapped[str] = mapped_column(db.String(500), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-to-Many relationship: A mechanic can work on multiple service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_mechanic, back_populates='mechanics')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-to-Many relationship: An inventory part can be used in multiple service tickets
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_inventory, back_populates='inventory_parts')
