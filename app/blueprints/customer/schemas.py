from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Customer
from app import db

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        sqla_session = db.session

# Schema for single customer
customer_schema = CustomerSchema()

# Schema for multiple customers
customers_schema = CustomerSchema(many=True)
