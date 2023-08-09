import datetime
import json
import jwt
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from src.controllers.auth_controller import token_required
from src.models.apartment_model import Apartment
from src.models.client_model import Client
from src.models.hotel_model import Hotel
from jsonschema import validate, ValidationError
from src.models.reservation_model import Reservation
from src.repositories.reservation_repository import ReservationRepository
from src.schemas.reservation_schema import create_reservation_schema

reservation_blueprint = Blueprint('reservation', __name__)


@reservation_blueprint.route("/hotels/<hotel_id>/apartments/<apartment_id>/reservations", methods=["POST"])
@token_required
def create_reservation(current_user, hotel_id, apartment_id):
    """
    Create reservation
    ---
    tags:
      - reservations
    parameters:
      - name: hotel_id
        in: path
        required: true
      - name: apartment_id
        in: path
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: reservation
          required:
            - date_from
            - date_to
            - number_of_guests
            - room_deposit
          properties:
            date_from:
              type: date
              description: date from
              example: 2023-09-01
            date_to:
              type: date
              description: date to
              example: 2023-09-07
            number_of_guests:
              type: integer
              description: number of guests
              example: 2
            room_deposit:
              type: integer
              description: room deposit
              example: 100
    security:
      - Bearer: []
    responses:
      201:
        description: Reservation inserted in the database
    """
    rabbitmq = current_app.config["RABBITMQ"]
    data = request.json
    try:
        validate(data, create_reservation_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    client = Client.query.filter_by(id=current_user.id).first()

    if not client:
        return jsonify({'error': 'Bad request'}), 404

    hotel = Hotel.query.filter_by(id=hotel_id).first()
    apartment = Apartment.query.filter_by(id=apartment_id).first()

    apartment_price = apartment.price

    date_from = datetime.strptime(data["date_from"], "%Y-%m-%d").replace(hour=15, minute=0, second=0)
    date_to = datetime.strptime(data["date_to"], "%Y-%m-%d").replace(hour=12, minute=0, second=0)

    days = date_to - date_from
    if days.days == 0:
        price = apartment_price
    elif days.days > 1:
        price = apartment_price * days.days

    reservations = Reservation.query.filter(
        Reservation.hotel_id == hotel.id,
        (Reservation.date_from <= date_to) & (date_from <= Reservation.date_to)
    ).all()
    if reservations:
        return jsonify({'error': 'no free apartments'}), 404

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    if not apartment:
        return jsonify({'error': 'No apartment found!'}), 404

    reservation_data = ReservationRepository.create_reservation(hotel_id, apartment_id, current_user.id,
                                                                date_from, date_to, price,
                                                                data["room_deposit"])

    reservation = Reservation.query.filter_by(client_id=current_user.id).first()

    token = jwt.encode(
        {'id': str(reservation.id)},
        'thisissecret',
        algorithm='HS256')

    mail = {
        'email': current_user.email,
        'subject': "Reservation confirmation (BOOKING)",
        'body': f"Reservation id: {reservation.id}\n"
                f"Hotel name: {hotel.hotel_name}\n"
                f"Date from: {reservation.date_from}\n"
                f"Date to: {reservation.date_to}\n"
                f"Price: {reservation.price}\n "
                f"Copy to confirm: http://127.0.0.1:5000//hotels/apartments/reservations/confirm-reservation?token={token}"
    }
    rabbitmq.send_message(json.dumps(mail))

    return jsonify({'apartment': reservation_data}), 201


@reservation_blueprint.route("/hotels/apartments/reservations/<reservation_id>", methods=["GET"])
def get_one(reservation_id):
    """
        Get reservation
        ---
        tags:
          - reservations
        parameters:
          - name: reservation_id
            in: path
            required: true
        responses:
          200:
            description: The reservation successfully returned
        """
    reservation = Reservation.query.filter_by(id=reservation_id).first()

    if not reservation:
        return jsonify({'error': 'No reservation found!'}), 404

    reservation_data = ReservationRepository.get_one_by_id(reservation_id)

    return jsonify(reservation_data), 200


@reservation_blueprint.route("/hotels/apartments/reservations/confirm-reservation", methods=["GET"])
def confirm_email():
    token = request.args.get('token')
    data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
    if not token:
        return jsonify({'error': 'Bad request'}), 400

    reservation = Reservation.query.filter_by(id=data['id']).first()

    if not reservation or reservation.is_confirmed:
        return jsonify({'error': 'Bad request'}), 400

    ReservationRepository.confirm_reservation(reservation)

    return jsonify({'message': 'Reservation confirmed'}), 200
