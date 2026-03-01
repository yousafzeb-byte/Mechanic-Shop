from flask import request, jsonify
from app import db
from app.models import Mechanic
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, DatabaseError

# POST / - Create a new mechanic
@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    """
    Create a New Mechanic
    ---
    tags:
      - Mechanics
    summary: Add a new mechanic to the system
    description: Creates a new mechanic record with all relevant information
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
            - salary
          properties:
            name:
              type: string
              example: "Mike Mechanic"
            email:
              type: string
              example: "mike@mechanicshop.com"
            phone:
              type: string
              example: "555-0201"
            address:
              type: string
              example: "100 Shop St, City, ST 12345"
            salary:
              type: number
              format: float
              example: 65000.0
    responses:
      201:
        description: Mechanic created successfully
      400:
        description: Validation error
    """
    try:
        data = request.get_json()
        mechanic = mechanic_schema.load(data)
        db.session.add(mechanic)
        db.session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Email already exists or constraint violation"}), 409

# GET / - Get all mechanics
@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    """
    Get All Mechanics
    ---
    tags:
      - Mechanics
    summary: Retrieve all mechanics
    description: Returns a list of all mechanics in the system
    responses:
      200:
        description: List of all mechanics
    """
    mechanics = db.session.execute(db.select(Mechanic)).scalars().all()
    return jsonify(mechanics_schema.dump(mechanics)), 200

# GET /by-tickets - Get mechanics ordered by number of tickets worked on
@mechanic_bp.route('/by-tickets', methods=['GET'])
def get_mechanics_by_tickets():
    """
    Get Mechanics Ranked by Workload
    ---
    tags:
      - Mechanics
    summary: Retrieve mechanics sorted by number of tickets worked
    description: Returns mechanics ordered by the number of service tickets they've worked on (descending). Uses SQL aggregation for efficient querying.
    responses:
      200:
        description: List of mechanics with their ticket counts
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Mike Mechanic"
              email:
                type: string
                example: "mike@mechanicshop.com"
              phone:
                type: string
                example: "555-0201"
              address:
                type: string
                example: "100 Shop St, City, ST 12345"
              salary:
                type: number
                example: 65000.0
              ticket_count:
                type: integer
                example: 3
                description: Number of tickets this mechanic has worked on
    """
    from app.models import service_mechanic
    
    # Query mechanics with count of service tickets, ordered by count descending
    mechanics_with_counts = db.session.query(
        Mechanic,
        func.count(service_mechanic.c.service_ticket_id).label('ticket_count')
    ).outerjoin(
        service_mechanic, Mechanic.id == service_mechanic.c.mechanic_id
    ).group_by(
        Mechanic.id
    ).order_by(
        func.count(service_mechanic.c.service_ticket_id).desc()
    ).all()
    
    # Format the response
    result = []
    for mechanic, ticket_count in mechanics_with_counts:
        mechanic_data = mechanic_schema.dump(mechanic)
        mechanic_data['ticket_count'] = ticket_count
        result.append(mechanic_data)
    
    return jsonify(result), 200

# GET /<int:id> - Get a specific mechanic
@mechanic_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    """
    Get Mechanic by ID
    ---
    tags:
      - Mechanics
    summary: Retrieve a specific mechanic
    description: Returns detailed information about a single mechanic
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Mechanic ID
    responses:
      200:
        description: Mechanic details
      404:
        description: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return jsonify(mechanic_schema.dump(mechanic)), 200

# PUT /<int:id> - Update a mechanic
@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    """
    Update Mechanic
    ---
    tags:
      - Mechanics
    summary: Update mechanic information
    description: Updates mechanic details including name, contact info, and salary
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Mechanic ID
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
            salary:
              type: number
              format: float
    responses:
      200:
        description: Mechanic updated successfully
      404:
        description: Mechanic not found
      400:
        description: Validation error
    """
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        data = request.get_json()
        
        # Validate data types
        if 'salary' in data:
            if not isinstance(data['salary'], (int, float)):
                return jsonify({"error": {"salary": ["Not a valid number."]}}), 400
        
        mechanic.name = data.get('name', mechanic.name)
        mechanic.email = data.get('email', mechanic.email)
        mechanic.phone = data.get('phone', mechanic.phone)
        mechanic.address = data.get('address', mechanic.address)
        mechanic.salary = data.get('salary', mechanic.salary)
        
        db.session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 200
    except (ValidationError, ValueError, TypeError) as e:
        return jsonify({"error": "Invalid data provided"}), 400
    except DatabaseError as e:
        db.session.rollback()
        return jsonify({"error": "Database error - invalid data"}), 400

# DELETE /<int:id> - Delete a mechanic
@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    """
    Delete Mechanic
    ---
    tags:
      - Mechanics
    summary: Delete a mechanic
    description: Removes a mechanic from the system
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Mechanic ID
    responses:
      200:
        description: Mechanic deleted successfully
      404:
        description: Mechanic not found
    """
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully"}), 200
