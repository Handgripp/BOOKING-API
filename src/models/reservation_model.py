import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Reservation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apartment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('apartment.id'))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'))
    hotel_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hotel.id'))
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    is_confirmed = db.Column(db.Boolean, default=False)
    room_deposit = db.Column(db.Integer)


