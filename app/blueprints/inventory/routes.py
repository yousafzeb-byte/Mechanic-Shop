from flask import request, jsonify
from app import db
from app.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError

# POST / - Create a new inventory part
@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    """
    Create a New Inventory Part
    ---
    tags:
      - Inventory
    summary: Add a new part to inventory
    description: Creates a new inventory item with name and price
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: "Oil Filter"
            price:
              type: number
              format: float
              example: 12.99
    responses:
      201:
        description: Inventory part created successfully
      400:
        description: Validation error
    """
    try:
        data = request.get_json()
        inventory = inventory_schema.load(data)
        db.session.add(inventory)
        db.session.commit()
        return jsonify(inventory_schema.dump(inventory)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except DatabaseError as e:
        db.session.rollback()
        return jsonify({"error": "Database error - invalid data"}), 400

# GET / - Get all inventory parts
@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    """
    Get All Inventory Parts
    ---
    tags:
      - Inventory
    summary: Retrieve all inventory items
    description: Returns a list of all parts in inventory with their prices
    responses:
      200:
        description: List of all inventory parts
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
                example: "Oil Filter"
              price:
                type: number
                format: float
                example: 12.99
    """
    inventories = db.session.execute(db.select(Inventory)).scalars().all()
    return jsonify(inventories_schema.dump(inventories)), 200

# GET /<int:id> - Get a specific inventory part
@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory(id):
    """
    Get Inventory Part by ID
    ---
    tags:
      - Inventory
    summary: Retrieve a specific inventory part
    description: Returns detailed information about a single inventory item
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Inventory part ID
    responses:
      200:
        description: Inventory part details
      404:
        description: Inventory part not found
    """
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    return jsonify(inventory_schema.dump(inventory)), 200

# PUT /<int:id> - Update an inventory part
@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    """
    Update Inventory Part
    ---
    tags:
      - Inventory
    summary: Update inventory part information
    description: Updates inventory part name and/or price
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Inventory part ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Premium Oil Filter"
            price:
              type: number
              format: float
              example: 15.99
    responses:
      200:
        description: Inventory part updated successfully
      404:
        description: Inventory part not found
      400:
        description: Validation error
    """
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    try:
        data = request.get_json()
        
        # Validate data types
        if 'price' in data:
            if not isinstance(data['price'], (int, float)):
                return jsonify({"error": {"price": ["Not a valid number."]}}), 400
        
        inventory.name = data.get('name', inventory.name)
        inventory.price = data.get('price', inventory.price)
        
        db.session.commit()
        return jsonify(inventory_schema.dump(inventory)), 200
    except (ValidationError, ValueError, TypeError) as e:
        return jsonify({"error": "Invalid data provided"}), 400
    except DatabaseError as e:
        db.session.rollback()
        return jsonify({"error": "Database error - invalid data"}), 400

# DELETE /<int:id> - Delete an inventory part
@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    """
    Delete Inventory Part
    ---
    tags:
      - Inventory
    summary: Delete an inventory part
    description: Removes an inventory item from the system
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Inventory part ID
    responses:
      200:
        description: Inventory part deleted successfully
      404:
        description: Inventory part not found
    """
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f"Inventory part {id} deleted successfully"}), 200
