import uuid
from werkzeug.security import generate_password_hash
from src.models.owner_model import Owner, db


class OwnerRepository:

    @staticmethod
    def create_owner(email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        owner = Owner(id=str(uuid.uuid4()), email=email, password=hashed_password)
        db.session.add(owner)
        db.session.commit()
        user_data = {
            'id': owner.id,
            'created_at': owner.created_at,
            'updated_at': owner.updated_at,
            'email': owner.email,
            'is_email_confirmed': owner.is_email_confirmed
        }

        return user_data

    @staticmethod
    def create_owner_test(user_id, email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        owner = Owner(id=user_id, email=email, password=hashed_password)
        db.session.add(owner)
        db.session.commit()
        user_data = {
            'id': owner.id,
            'created_at': owner.created_at,
            'updated_at': owner.updated_at,
            'email': owner.email,
            'is_email_confirmed': owner.is_email_confirmed
        }

        return user_data

    @staticmethod
    def get_one_by_id(user_id):
        owner = Owner.query.get(user_id)
        if not owner:
            return None

        user_data = {
            'id': owner.id,
            'created_at': owner.created_at,
            'updated_at': owner.updated_at,
            'email': owner.email,
            'is_email_confirmed': owner.is_email_confirmed
        }

        return user_data

    @staticmethod
    def email_confirmation(user_id):
        owner = Owner.query.filter_by(id=user_id).first()
        owner.is_email_confirmed = True
        db.session.commit()
