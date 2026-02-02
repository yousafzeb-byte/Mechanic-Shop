from flask import request, jsonify
from app import db
from app.models import Customer
from . import customer_bp
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError

# POST / - Create a new customer
@customer_bp.route('/', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        customer = customer_schema.load(data)
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer_schema.dump(customer)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET / - Get all customers
@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = db.session.execute(db.select(Customer)).scalars().all()
    return jsonify(customers_schema.dump(customers)), 200

# GET /<int:id> - Get a specific customer
@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer_schema.dump(customer)), 200

# PUT /<int:id> - Update a customer
@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    try:
        data = request.get_json()
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)
        
        db.session.commit()
        return jsonify(customer_schema.dump(customer)), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

# DELETE /<int:id> - Delete a customer
@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully"}), 200
