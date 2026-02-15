from flask import request, jsonify
from app import db
from app.models import ServiceTicket, Mechanic, Inventory
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError

# POST / - Create a new service ticket
@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        data = request.get_json()
        service_ticket = service_ticket_schema.load(data)
        db.session.add(service_ticket)
        db.session.commit()
        return jsonify(service_ticket_schema.dump(service_ticket)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET / - Get all service tickets
@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    service_tickets = db.session.execute(db.select(ServiceTicket)).scalars().all()
    return jsonify(service_tickets_schema.dump(service_tickets)), 200

# GET /<int:id> - Get a specific service ticket
@service_ticket_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    service_ticket = db.session.get(ServiceTicket, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

# PUT /<int:ticket_id>/edit - Add and remove mechanics from a service ticket
@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    data = request.get_json()
    remove_ids = data.get('remove_ids', [])
    add_ids = data.get('add_ids', [])
    
    # Remove mechanics
    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
    
    # Add mechanics
    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
    
    db.session.commit()
    
    return jsonify({
        "message": "Mechanics updated successfully",
        "service_ticket": service_ticket_schema.dump(service_ticket)
    }), 200

# PUT /<int:ticket_id>/add-part/<int:part_id> - Add a part to a service ticket
@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, part_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    
    # Check if part is already added
    if part in service_ticket.inventory_parts:
        return jsonify({"message": "Part already added to this service ticket"}), 400
    
    # Add part to service ticket
    service_ticket.inventory_parts.append(part)
    db.session.commit()
    
    return jsonify({
        "message": f"Part {part_id} added to Service Ticket {ticket_id}",
        "service_ticket": service_ticket_schema.dump(service_ticket)
    }), 200

# PUT /<ticket_id>/assign-mechanic/<mechanic_id> - Assign a mechanic to a service ticket
@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    # Check if mechanic is already assigned
    if mechanic in service_ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this service ticket"}), 400
    
    # Add mechanic to service ticket using the relationship
    service_ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return jsonify({
        "message": f"Mechanic {mechanic_id} assigned to Service Ticket {ticket_id}",
        "service_ticket": service_ticket_schema.dump(service_ticket)
    }), 200

# PUT /<ticket_id>/remove-mechanic/<mechanic_id> - Remove a mechanic from a service ticket
@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    # Check if mechanic is assigned
    if mechanic not in service_ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this service ticket"}), 400
    
    # Remove mechanic from service ticket using the relationship
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return jsonify({
        "message": f"Mechanic {mechanic_id} removed from Service Ticket {ticket_id}",
        "service_ticket": service_ticket_schema.dump(service_ticket)
    }), 200

# DELETE /<int:id> - Delete a service ticket
@service_ticket_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    service_ticket = db.session.get(ServiceTicket, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket {id} deleted successfully"}), 200
