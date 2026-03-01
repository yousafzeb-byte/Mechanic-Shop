from marshmallow import fields, validate, validates_schema, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Inventory
from app import db

class InventorySchema(SQLAlchemyAutoSchema):
    price = fields.Float(required=False)
    
    @validates_schema
    def validate_price(self, data, **kwargs):
        if 'price' in data:
            if not isinstance(data['price'], (int, float)):
                raise ValidationError('Price must be a number', 'price')
    
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True
        sqla_session = db.session

# Schema for single inventory item
inventory_schema = InventorySchema()

# Schema for multiple inventory items
inventories_schema = InventorySchema(many=True)
