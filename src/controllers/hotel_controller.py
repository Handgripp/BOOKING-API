from flask import Blueprint, request, jsonify

from src.controllers.auth_controller import token_required
from src.models.hotel_model import Hotel
from src.repositories.hotel_repository import HotelRepository
from jsonschema import validate, ValidationError
from src.schemas.hotel_schema import create_hotel_schema
from src.services.distanceapi import DistanceCalculator
from src.services.geoapi import CityChecker

hotel_blueprint = Blueprint('hotel', __name__)


@hotel_blueprint.route("/hotels", methods=["POST"])
@token_required
def create_hotel(current_user):
    """
    Create hotel
    ---
    tags:
      - hotels
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Hotel
          required:
            - hotel_name
            - city
          properties:
            hotel_name:
              type: string
              description: Hotel name
              example: "Marine"
            city:
              type: string
              description: Hotel city
              example: "Kołobrzeg"
    security:
      - Bearer: []
    responses:
      201:
        description: The hotel inserted in the database
    """

    data = request.json
    try:
        validate(data, create_hotel_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    hotel = Hotel.query.filter_by(hotel_name=data["hotel_name"]).first()

    city = CityChecker(data["city"])
    city_checker = city.check_city_existence()

    if not city_checker:
        return jsonify({'error': 'City does not exist'}), 404

    if hotel:
        return jsonify({'error': 'Hotel with that name already exists'}), 409

    HotelRepository.create_hotel(current_user.id, data["hotel_name"], data["city"])

    return jsonify({'message': 'New hotel created'}), 201


@hotel_blueprint.route("/hotels/<hotel_id>", methods=["GET"])
def get_one(hotel_id):
    """
        Get hotel
        ---
        tags:
          - hotels
        parameters:
          - name: hotel_id
            in: path
            required: true
        responses:
          200:
            description: The hotel successfully returned
        """
    hotel_data = HotelRepository.get_one_by_id(hotel_id)

    if not hotel_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(hotel_data), 200


@hotel_blueprint.route("/hotels/search/<hotel_id>", methods=["GET"])
@token_required
def search_hotel(current_user, hotel_id):
    """
        Get hotel
        ---
        tags:
          - hotels
        parameters:
          - name: hotel_id
            in: path
            required: true
        security:
          - Bearer: []
        responses:
          200:
            description: Hotel found
        """

    user_city = current_user.city
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not user_city:
        return jsonify({'error': 'No user found'}), 404
    if not hotel:
        return jsonify({'error': 'No hotel found'}), 404

    city_user = CityChecker(current_user.city)
    city_hotel = CityChecker(hotel.city)
    coordinates_user = city_user.get_city_coordinates()
    coordinates_hotel = city_hotel.get_city_coordinates()

    coordinates_origin = coordinates_user['lon'], coordinates_user['lat']
    coordinates_destination = coordinates_hotel['lon'], coordinates_hotel['lat']

    distance = DistanceCalculator(coordinates_origin, coordinates_destination)
    distance_calculator = distance.calculate_distance()

    return jsonify(distance_calculator), 200
