import json
from datetime import date, timedelta
import jwt
from flask import current_app
from src.models.client_model import Client
from src.models.hotel_model import Hotel
from src.models.reservation_model import Reservation
from src.repositories.reservation_repository import ReservationRepository


def reservation_service():
    rabbitmq = current_app.config["RABBITMQ"]
    current_date = date.today()
    current_date_minus_4 = (current_date - timedelta(days=4))
    current_date_minus_7 = (current_date - timedelta(days=7))
    reservations = Reservation.query.all()

    for reservation in reservations:

        dates = reservation.created_at
        dates_to_check = dates.strftime("%Y-%m-%d")
        if str(current_date_minus_4) == str(dates_to_check) and reservation.is_confirmed is False:
            current_user = Client.query.filter_by(id=reservation.client_id).first()
            hotel = Hotel.query.filter_by(id=reservation.hotel_id).first()
            token = jwt.encode(
                {'id': str(reservation.id)},
                'thisissecret',
                algorithm='HS256')
            mail = {
                'email': current_user.email,
                'subject': "Please confirm your reservation",
                'body': f"You must to confirm this reservation\n"
                        f"Reservation id: {reservation.id}\n"
                        f"Hotel name: {hotel.hotel_name}\n"
                        f"Date from: {reservation.date_from}\n"
                        f"Date to: {reservation.date_to}\n"
                        f"Price: {reservation.price}\n "
                        f"Copy to confirm: http://127.0.0.1:5000//hotels/apartments/reservations/confirm-reservation?token={token}"
            }
            rabbitmq.send_message(json.dumps(mail))
        elif str(current_date_minus_7) == str(dates_to_check) and reservation.is_confirmed is False:
            current_user = Client.query.filter_by(id=reservation.client_id).first()
            hotel = Hotel.query.filter_by(id=reservation.hotel_id).first()
            mail = {
                'email': current_user.email,
                'subject': "Your reservation has cancelled",
                'body': f"Sorry, but your reservation was not confirmed within 7 days and has been cancelled \n"
                        f"Reservation id: {reservation.id}\n"
                        f"Hotel name: {hotel.hotel_name}\n"
                        f"Date from: {reservation.date_from}\n"
                        f"Date to: {reservation.date_to}\n"
                        f"Price: {reservation.price}\n "
            }
            rabbitmq.send_message(json.dumps(mail))
            ReservationRepository.delete_reservation(reservation)
