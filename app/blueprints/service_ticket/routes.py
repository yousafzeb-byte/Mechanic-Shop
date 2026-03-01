from flask import request, jsonify
from app import db
from app.models import ServiceTicket, Mechanic, Inventory
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

# POST / - Create a new service ticket
@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    """
    Create a New Service Ticket
    ---
    tags:
      - Service Tickets
    summary: Create a new service ticket
    description: Creates a new service ticket for a customer's vehicle
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - VIN
            - description
            - service_date
            - customer_id
          properties:
            VIN:
              type: string
              example: "1HGBH41JXMN109186"
            description:
              type: string
              example: "Oil change and filter replacement"
            service_date:
              type: string
              format: date
              example: "2026-02-01"
            customer_id:
              type: integer
              example: 1
    responses:
      201:
        description: Service ticket created successfully
      400:
        description: Validation error
    """
    try:
        data = request.get_json()
        service_ticket = service_ticket_schema.load(data)
        db.session.add(service_ticket)
        db.session.commit()
        return jsonify(service_ticket_schema.dump(service_ticket)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid customer ID or constraint violation"}), 400

# GET / - Get all service tickets
@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    """
    Get All Service Tickets
    ---
    tags:
      - Service Tickets
    summary: Retrieve all service tickets
    description: Returns a list of all service tickets in the system
    responses:
      200:
        description: List of all service tickets
    """
    service_tickets = db.session.execute(db.select(ServiceTicket)).scalars().all()
    return jsonify(service_tickets_schema.dump(service_tickets)), 200

# GET /<int:id> - Get a specific service ticket
@service_ticket_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    """
    Get Service Ticket by ID
    ---
    tags:
      - Service Tickets
    summary: Retrieve a specific service ticket
    description: Returns detailed information about a single service ticket
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Service ticket ID
    responses:
      200:
        description: Service ticket details
      404:
        description: Service ticket not found
    """
    service_ticket = db.session.get(ServiceTicket, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

# PUT /<int:ticket_id>/edit - Add and remove mechanics from a service ticket
@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    """
    Bulk Edit Ticket Mechanics
    ---
    tags:
      - Service Tickets
    summary: Add and remove mechanics from a ticket in bulk
    description: Allows adding multiple mechanics and removing multiple mechanics from a service ticket in a single request
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
        description: Service ticket ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            remove_ids:
              type: array
              items:
                type: integer
              example: [1]
              description: Array of mechanic IDs to remove from this ticket
            add_ids:
              type: array
              items:
                type: integer
              example: [2, 3]
              description: Array of mechanic IDs to add to this ticket
    responses:
      200:
        description: Mechanics updated successfully
      404:
        description: Service ticket not found
    """
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
    """
    Add Part to Service Ticket
    ---
    tags:
      - Service Tickets
    summary: Add an inventory part to a service ticket
    description: Associates an inventory part with a service ticket, tracking which parts are used for each job
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
        description: Service ticket ID
      - in: path
        name: part_id
        type: integer
        required: true
        description: Inventory part ID
    responses:
      200:
        description: Part added to service ticket successfully
      400:
        description: Part already added to this ticket
      404:
        description: Service ticket or part not found
    """
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
    """
    Assign Mechanic to Ticket
    ---
    tags:
      - Service Tickets
    summary: Assign a single mechanic to a service ticket
    description: Adds a mechanic to the service ticket's assigned mechanics
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
        description: Service ticket ID
      - in: path
        name: mechanic_id
        type: integer
        required: true
        description: Mechanic ID
    responses:
      200:
        description: Mechanic assigned successfully
      400:
        description: Mechanic already assigned to this ticket
      404:
        description: Service ticket or mechanic not found
    """
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
    """
    Remove Mechanic from Ticket
    ---
    tags:
      - Service Tickets
    summary: Remove a mechanic from a service ticket
    description: Removes a mechanic from the service ticket's assigned mechanics
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
        description: Service ticket ID
      - in: path
        name: mechanic_id
        type: integer
        required: true
        description: Mechanic ID
    responses:
      200:
        description: Mechanic removed successfully
      400:
        description: Mechanic is not assigned to this ticket
      404:
        description: Service ticket or mechanic not found
    """
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
    """
    Delete Service Ticket
    ---
    tags:
      - Service Tickets
    summary: Delete a service ticket
    description: Removes a service ticket from the system
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Service ticket ID
    responses:
      200:
        description: Service ticket deleted successfully
      404:
        description: Service ticket not found
    """
    service_ticket = db.session.get(ServiceTicket, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket {id} deleted successfully"}), 200
