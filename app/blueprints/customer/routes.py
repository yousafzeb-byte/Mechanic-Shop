from flask import request, jsonify
from app import db, limiter, cache
from app.models import Customer
from . import customer_bp
from .schemas import customer_schema, customers_schema, login_schema
from marshmallow import ValidationError
from app.utils import hash_password, verify_password, encode_token, token_required
from sqlalchemy.exc import IntegrityError

# POST /login - Login a customer
@customer_bp.route('/login', methods=['POST'])
def login():
    """
    Customer Login
    ---
    tags:
      - Customers
    summary: Authenticate a customer and receive a JWT token
    description: Validates customer credentials and returns a JWT token for authentication
    parameters:
      - in: body
        name: body
        required: true
        description: Customer login credentials
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "john@example.com"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login successful"
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            customer_id:
              type: integer
              example: 1
      401:
        description: Invalid credentials
      400:
        description: Validation error
    """
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
    """
    Get My Service Tickets
    ---
    tags:
      - Customers
    summary: Retrieve all service tickets for the authenticated customer
    description: Returns a list of service tickets belonging to the logged-in customer
    security:
      - Bearer: []
    responses:
      200:
        description: List of customer's service tickets
      401:
        description: Unauthorized - Invalid or missing token
      404:
        description: Customer not found
    """
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
    """
    Create a New Customer
    ---
    tags:
      - Customers
    summary: Register a new customer account
    description: Creates a new customer with hashed password. Rate limited to 5 per minute.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - phone
            - address
            - password
          properties:
            name:
              type: string
              example: "John Doe"
            email:
              type: string
              example: "john@example.com"
            phone:
              type: string
              example: "555-0101"
            address:
              type: string
              example: "123 Main St, City, ST 12345"
            password:
              type: string
              example: "password123"
    responses:
      201:
        description: Customer created successfully
      400:
        description: Validation error
      429:
        description: Too many requests - rate limit exceeded
    """
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
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Email already exists or constraint violation"}), 409

# GET / - Get all customers (with caching)
@customer_bp.route('/', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_customers():
    """
    Get All Customers
    ---
    tags:
      - Customers
    summary: Retrieve all customers with pagination
    description: Returns a paginated list of all customers. Results are cached for 60 seconds.
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        default: 1
        description: Page number
      - in: query
        name: per_page
        type: integer
        required: false
        default: 10
        description: Number of items per page
    responses:
      200:
        description: Paginated list of customers with metadata
    """
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
    """
    Get Customer by ID
    ---
    tags:
      - Customers
    summary: Retrieve a specific customer
    description: Returns detailed information about a single customer
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer_schema.dump(customer)), 200

# PUT /<int:id> - Update a customer (requires token)
@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    """
    Update Customer
    ---
    tags:
      - Customers
    summary: Update customer information
    description: Updates customer details. Customers can only update their own account.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
            address:
              type: string
            password:
              type: string
    responses:
      200:
        description: Customer updated successfully
      401:
        description: Unauthorized - Invalid or missing token
      403:
        description: Forbidden - Cannot update another customer's account
      404:
        description: Customer not found
    """
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
    """
    Delete Customer
    ---
    tags:
      - Customers
    summary: Delete a customer account
    description: Deletes a customer account. Customers can only delete their own account.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer deleted successfully
      401:
        description: Unauthorized - Invalid or missing token
      403:
        description: Forbidden - Cannot delete another customer's account
      404:
        description: Customer not found
    """
    # Check if the customer is deleting their own account
    if customer_id != id:
        return jsonify({"error": "Unauthorized to delete this customer"}), 403
    
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully"}), 200

# DELETE /admin/<int:id> - Admin delete (no authentication required - for testing only)
@customer_bp.route('/admin/<int:id>', methods=['DELETE'])
def admin_delete_customer(id):
    """
    Admin Delete Customer
    ---
    tags:
      - Customers
    summary: Admin endpoint to delete any customer (Testing only)
    description: Deletes a customer without authentication. For testing and cleanup purposes only.
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer deleted successfully
      404:
        description: Customer not found
    """
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted successfully (admin)"}), 200
