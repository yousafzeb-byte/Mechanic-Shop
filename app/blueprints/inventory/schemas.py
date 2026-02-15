from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Inventory
from app import db

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
        sqla_session = db.session

# Schema for single inventory item
inventory_schema = InventorySchema()

# Schema for multiple inventory items
inventories_schema = InventorySchema(many=True)
