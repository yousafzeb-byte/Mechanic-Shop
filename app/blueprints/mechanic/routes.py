from flask import request, jsonify
from app import db
from app.models import Mechanic
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from sqlalchemy import func

# POST / - Create a new mechanic
@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        data = request.get_json()
        mechanic = mechanic_schema.load(data)
        db.session.add(mechanic)
        db.session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET / - Get all mechanics
@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.execute(db.select(Mechanic)).scalars().all()
    return jsonify(mechanics_schema.dump(mechanics)), 200

# GET /by-tickets - Get mechanics ordered by number of tickets worked on
@mechanic_bp.route('/by-tickets', methods=['GET'])
def get_mechanics_by_tickets():
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
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return jsonify(mechanic_schema.dump(mechanic)), 200

# PUT /<int:id> - Update a mechanic
@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        data = request.get_json()
        mechanic.name = data.get('name', mechanic.name)
        mechanic.email = data.get('email', mechanic.email)
        mechanic.phone = data.get('phone', mechanic.phone)
        mechanic.address = data.get('address', mechanic.address)
        mechanic.salary = data.get('salary', mechanic.salary)
        
        db.session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

# DELETE /<int:id> - Delete a mechanic
@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully"}), 200
