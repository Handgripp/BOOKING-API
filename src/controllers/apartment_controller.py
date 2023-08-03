from flask import Blueprint, request, jsonify
from src.controllers.auth_controller import token_required
from src.models.apartment_model import Apartment
from src.models.hotel_model import Hotel
from src.models.owner_model import Owner
from src.repositories.apartment_repository import ApartmentRepository
from jsonschema import validate, ValidationError
from src.schemas.apartment_schema import create_apartment_schema

apartment_blueprint = Blueprint('apartment', __name__)


@apartment_blueprint.route("/hotels/<hotel_id>/apartments", methods=["POST"])
@token_required
def create_apartment(current_user, hotel_id):
    """
    Create apartment
    ---
    tags:
      - apartments
    parameters:
      - name: hotel_id
        in: path
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: Apartment
          required:
            - apartment_name
            - number_of_rooms
            - number_of_guests
            - price
          properties:
            apartment_name:
              type: string
              description: apartment name
              example: "Blue sky"
            number_of_rooms:
              type: integer
              description: number of rooms
              example: 2
            number_of_guests:
              type: integer
              description: number of guests
              example: 4
            price:
              type: integer
              description: price
              example: 200
    security:
      - Bearer: []
    responses:
      201:
        description: The hotel inserted in the database
    """

    data = request.json
    try:
        validate(data, create_apartment_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    owner = Owner.query.filter_by(id=current_user.id).first()

    if not owner:
        return jsonify({'error': 'Bad request'}), 404

    apartment = Apartment.query.filter_by(apartment_name=data["apartment_name"]).first()

    if apartment:
        return jsonify({'error': 'Hotel with that name already exists'}), 409

    hotel = Hotel.query.filter_by(id=hotel_id).first()

    if current_user.id != hotel.owner_id:
        return jsonify({'error': 'You are not owner!'}), 403

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    apartment_data = ApartmentRepository.create_apartment(hotel_id, data["apartment_name"], data["number_of_rooms"],
                                                          data["number_of_guests"], data["price"])

    return jsonify({'apartment': apartment_data}), 201


@apartment_blueprint.route("/hotels/<hotel_id>/apartments/<apartment_id>", methods=["GET"])
def get_one(apartment_id, hotel_id):
    """
        Get apartment
        ---
        tags:
          - apartments
        parameters:
          - name: hotel_id
            in: path
            required: true
          - name: apartment_id
            in: path
            required: true
        responses:
          200:
            description: The apartment successfully returned
        """
    hotel = Hotel.query.filter_by(id=hotel_id).first()

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    apartment_data = ApartmentRepository.get_one_by_id(apartment_id)

    if not apartment_data:
        return jsonify({'error': 'No apartment found!'}), 404

    return jsonify(apartment_data), 200


