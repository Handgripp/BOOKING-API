import uuid
from src.models.reservation_model import Reservation, db


class ReservationRepository:

    @staticmethod
    def create_reservation(hotel_id, apartment_id, client_id, date_from, date_to, price, room_deposit):
        reservation = Reservation(id=str(uuid.uuid4()), hotel_id=hotel_id, apartment_id=apartment_id,
                                  client_id=client_id, date_from=date_from,
                                  date_to=date_to, price=price, room_deposit=room_deposit)
        db.session.add(reservation)
        db.session.commit()
        apartment_data = {
            'id': reservation.id,
            'created_at': reservation.created_at,
            'updated_at': reservation.updated_at,
            'apartment_id': reservation.apartment_id,
            'client_id': reservation.client_id,
            'hotel_id': reservation.hotel_id,
            'date_from': reservation.date_from,
            'date_to': reservation.date_to,
            'price': reservation.price,
            'room_deposit': reservation.room_deposit
        }

        return apartment_data

    @staticmethod
    def get_one_by_id(apartment_id):
        reservation = Reservation.query.get(apartment_id)
        if not reservation:
            return None

        apartment_data = {
            'id': reservation.id,
            'created_at': reservation.created_at,
            'updated_at': reservation.updated_at,
            'hotel_id': reservation.hotel_id,
            'client_id': reservation.client_id,
            'apartment_id': reservation.apartment_id,
            'date_from': reservation.date_from,
            'date_to': reservation.date_to,
            'room_deposit': reservation.room_deposit,
            'price': reservation.price,
            'is_confirmed': reservation.is_confirmed
        }

        return apartment_data

    @staticmethod
    def confirm_reservation(reservation):
        reservation.is_confirmed = True
        db.session.commit()

    @staticmethod
    def delete_reservation(reservation_id):
        db.session.delete(reservation_id)
        db.session.commit()
