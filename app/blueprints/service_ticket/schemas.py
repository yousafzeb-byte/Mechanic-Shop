from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import ServiceTicket
from app import db

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
        sqla_session = db.session

# Schema for single service ticket
service_ticket_schema = ServiceTicketSchema()

# Schema for multiple service tickets
service_tickets_schema = ServiceTicketSchema(many=True)
