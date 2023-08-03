import uuid

from src.models.apartment_model import Apartment
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
    def get_one_by_id(hotel_id):
        hotel = Hotel.query.get(hotel_id)
        apartments = Apartment.query.filter_by(hotel_id=hotel_id, is_free=False).all()
        number_free_apartment = 0

        for i in apartments:
            number_free_apartment += 1

        if not hotel:
            return None

        hotel_data = {
            'id': hotel.id,
            'created_at': hotel.created_at,
            'updated_at': hotel.updated_at,
            'hotel_name': hotel.hotel_name,
            'city': hotel.city,
            'owner_id': hotel.owner_id,
            'number_of_free_apartments': number_free_apartment
        }

        return hotel_data

    @staticmethod
    def get_one_by_id_with_distance(hotel_id, calculated_distance):
        hotel = Hotel.query.get(hotel_id)
        if not hotel:
            return None

        hotel_data = {
            'id': hotel.id,
            'created_at': hotel.created_at,
            'updated_at': hotel.updated_at,
            'hotel_name': hotel.hotel_name,
            'city': hotel.city,
            'owner_id': hotel.owner_id,
            'distance': calculated_distance
        }

        return hotel_data

    @staticmethod
    def get_all_from_city(city, calculated_distance):
        hotels = Hotel.query.filter_by(city=city).all()
        print(hotels)
        if not hotels:
            return None
        hotels_data = []
        for hotel in hotels:
            hotel_data = {
                'id': hotel.id,
                'created_at': hotel.created_at,
                'updated_at': hotel.updated_at,
                'hotel_name': hotel.hotel_name,
                'city': hotel.city,
                'owner_id': hotel.owner_id,
                'distance': calculated_distance
            }
            hotels_data.append(hotel_data)

        return hotels_data
