import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Hotel(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('owner.id'))
    hotel_name = db.Column(db.String(60))
    city = db.Column(db.String(60))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)


