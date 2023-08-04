from datetime import datetime
from flask import Blueprint, request, jsonify
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
    price = apartment_price * days.days

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    if not apartment:
        return jsonify({'error': 'No apartment found!'}), 404

    reservation_data = ReservationRepository.create_reservation(hotel_id, apartment_id, current_user.id,
                                                                date_from, date_to, price,
                                                                data["room_deposit"])

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
