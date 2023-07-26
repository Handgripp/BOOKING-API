import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Opinion(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hotel.id'))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'))
    text = db.Column(db.String(240))
    rating = db.Column(db.Integer)
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    confirmed_stay = db.Column(db.Boolean, default=True)

