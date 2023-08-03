import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Apartment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hotel.id'))
    apartment_name = db.Column(db.String(60))
    price = db.Column(db.Integer)
    number_of_guests = db.Column(db.Integer)
    number_of_rooms = db.Column(db.Integer)
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)



