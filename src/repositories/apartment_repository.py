import uuid
from src.models.apartment_model import Apartment, db


class ApartmentRepository:

    @staticmethod
    def create_apartment(hotel_id, apartment_name, number_of_rooms, number_of_guests, price):
        apartment = Apartment(id=str(uuid.uuid4()), hotel_id=hotel_id, apartment_name=apartment_name,
                              number_of_rooms=number_of_rooms, number_of_guests=number_of_guests, price=price)
        db.session.add(apartment)
        db.session.commit()
        apartment_data = {
            'id': apartment.id,
            'created_at': apartment.created_at,
            'updated_at': apartment.updated_at,
            'hotel_id': apartment.hotel_id,
            'apartment_name': apartment.apartment_name,
            'number_of_rooms': apartment.number_of_rooms,
            'number_of_guests': apartment.number_of_guests,
            'price': apartment.price
        }

        return apartment_data

    @staticmethod
    def get_one_by_id(apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if not apartment:
            return None

        apartment_data = {
            'id': apartment.id,
            'created_at': apartment.created_at,
            'updated_at': apartment.updated_at,
            'owner_id': apartment.hotel_id,
            'hotel_name': apartment.apartment_name,
            'apartment': apartment.number_of_rooms,
            'number_of_guests': apartment.number_of_guests,
            'price': apartment.price,
        }

        return apartment_data
