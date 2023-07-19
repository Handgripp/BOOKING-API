import uuid
from src.models.hotel_model import Hotel, db


class HotelRepository:

    @staticmethod
    def create_hotel(owner_id, hotel_name, city):
        hotel = Hotel(id=str(uuid.uuid4()), owner_id=owner_id, hotel_name=hotel_name, city=city)
        db.session.add(hotel)
        db.session.commit()
        hotel_data = {
            'id': hotel.id,
            'created_at': hotel.created_at,
            'updated_at': hotel.updated_at,
            'owner_id': hotel.owner_id,
            'hotel_name': hotel.hotel_name,
            'city': hotel.city
        }

        return hotel_data

    @staticmethod
    def get_one_by_id(user_id):
        hotel = Hotel.query.get(user_id)
        if not hotel:
            return None

        hotel_data = {
            'id': hotel.id,
            'created_at': hotel.created_at,
            'updated_at': hotel.updated_at,
            'email': hotel.email,
            'is_email_confirmed': hotel.is_email_confirmed
        }

        return hotel_data

