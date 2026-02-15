from flask import request, jsonify
from app import db, limiter, cache
from app.models import Customer
from . import customer_bp
from .schemas import customer_schema, customers_schema, login_schema
from marshmallow import ValidationError
from app.utils import hash_password, verify_password, encode_token, token_required

# POST /login - Login a customer
@customer_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        validated_data = login_schema.load(data)
        
        # Find customer by email
        customer = db.session.execute(
            db.select(Customer).where(Customer.email == validated_data['email'])
        ).scalar_one_or_none()
        
        if not customer:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Verify password
        if not verify_password(validated_data['password'], customer.password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Generate token
        token = encode_token(customer.id)
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "customer_id": customer.id
        }), 200
        
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET /my-tickets - Get tickets for logged-in customer (requires token)
@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    # Get all service tickets for this customer
    from app.blueprints.service_ticket.schemas import service_tickets_schema
    return jsonify(service_tickets_schema.dump(customer.service_tickets)), 200

# POST / - Create a new customer (with rate limiting)
@customer_bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_customer():
    try:
        data = request.get_json()
        
        # Hash the password before creating customer
        if 'password' in data:
            data['password'] = hash_password(data['password'])
        
        customer = customer_schema.load(data)
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer_schema.dump(customer)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET / - Get all customers (with caching)
@customer_bp.route('/', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_customers():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query customers with pagination
    pagination = db.paginate(
        db.select(Customer).order_by(Customer.id),
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    customers = pagination.items
    
    return jsonify({
        "customers": customers_schema.dump(customers),
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200

# GET /<int:id> - Get a specific customer
@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer_schema.dump(customer)), 200

# PUT /<int:id> - Update a customer (requires token)
@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    # Check if the customer is updating their own account
    if customer_id != id:
        return jsonify({"error": "Unauthorized to update this customer"}), 403
    
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    try:
        data = request.get_json()
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)
        
        # If password is being updated, hash it
        if 'password' in data:
            customer.password = hash_password(data['password'])
        
        db.session.commit()
        return jsonify(customer_schema.dump(customer)), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

# DELETE /<int:id> - Delete a customer (requires token)
@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id, id):
    # Check if the customer is deleting their own account
    if customer_id != id:
        return jsonify({"error": "Unauthorized to delete this customer"}), 403
    
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully"}), 200
