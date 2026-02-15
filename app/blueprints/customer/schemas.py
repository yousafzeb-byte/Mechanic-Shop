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
        load_only = ('password',)  # Don't return password in responses

class LoginSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = False
        sqla_session = db.session
        fields = ('email', 'password')  # Only include email and password

# Schema for single customer
customer_schema = CustomerSchema()

# Schema for multiple customers
customers_schema = CustomerSchema(many=True)

# Schema for login
login_schema = LoginSchema()
