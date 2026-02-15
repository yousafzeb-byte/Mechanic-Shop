from flask import request, jsonify
from app import db
from app.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError

# POST / - Create a new inventory part
@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    try:
        data = request.get_json()
        inventory = inventory_schema.load(data)
        db.session.add(inventory)
        db.session.commit()
        return jsonify(inventory_schema.dump(inventory)), 201
    except ValidationError as e:
        return jsonify(e.messages), 400

# GET / - Get all inventory parts
@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    inventories = db.session.execute(db.select(Inventory)).scalars().all()
    return jsonify(inventories_schema.dump(inventories)), 200

# GET /<int:id> - Get a specific inventory part
@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory(id):
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    return jsonify(inventory_schema.dump(inventory)), 200

# PUT /<int:id> - Update an inventory part
@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    try:
        data = request.get_json()
        inventory.name = data.get('name', inventory.name)
        inventory.price = data.get('price', inventory.price)
        
        db.session.commit()
        return jsonify(inventory_schema.dump(inventory)), 200
    except ValidationError as e:
        return jsonify(e.messages), 400

# DELETE /<int:id> - Delete an inventory part
@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory = db.session.get(Inventory, id)
    if not inventory:
        return jsonify({"error": "Inventory part not found"}), 404
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f"Inventory part {id} deleted successfully"}), 200
