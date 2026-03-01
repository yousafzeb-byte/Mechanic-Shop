from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic
from app import db

class MechanicSchema(SQLAlchemyAutoSchema):
    email = fields.Email(required=True, validate=validate.Email())
    
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
        sqla_session = db.session

# Schema for single mechanic
mechanic_schema = MechanicSchema()

# Schema for multiple mechanics
mechanics_schema = MechanicSchema(many=True)
