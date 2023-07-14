import uuid
from werkzeug.security import generate_password_hash
from src.models.client_model import Client, db


class ClientRepository:

    @staticmethod
    def create_client(first_name, last_name, city, email, password):
        hashed_password = generate_password_hash(password, method='sha256')
        client = Client(id=str(uuid.uuid4()), first_name=first_name, last_name=last_name,
                        city=city, email=email, password=hashed_password)
        db.session.add(client)
        db.session.commit()
        user_data = {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'created_at': client.created_at,
            'updated_at': client.updated_at,
            'city': client.city,
            'email': client.email,
            'is_email_confirmed': client.is_email_confirmed,
            'rental_points': client.rental_points
        }

        return user_data

    @staticmethod
    def get_one_by_id(user_id):
        client = Client.query.get(user_id)
        if not client:
            return None

        user_data = {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'created_at': client.created_at,
            'updated_at': client.updated_at,
            'city': client.city,
            'email': client.email,
            'is_email_confirmed': client.is_email_confirmed,
            'rental_points': client.rental_points
        }

        return user_data

    @staticmethod
    def email_confirmation(user_id):
        client = Client.query.filter_by(id=user_id).first()
        client.is_email_confirmed = True
        db.session.commit()
