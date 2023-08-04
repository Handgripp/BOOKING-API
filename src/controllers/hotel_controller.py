from datetime import datetime
from flask import Blueprint, request, jsonify
from src.controllers.auth_controller import token_required
from src.models.client_model import Client
from src.models.hotel_model import Hotel
from src.models.owner_model import Owner
from src.models.reservation_model import Reservation
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

    owner = Owner.query.filter_by(id=current_user.id).first()

    if not owner:
        return jsonify({'error': 'Bad request'}), 404

    hotel = Hotel.query.filter_by(hotel_name=data["hotel_name"]).first()
    try:
        city = CityChecker(data["city"])
        city_checker = city.check_city_existence()
    except ConnectionError:
        return jsonify({"error": "Connection error with external API"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 503

    if not city_checker:
        return jsonify({'error': 'City does not exist'}), 404

    if hotel:
        return jsonify({'error': 'Hotel with that name already exists'}), 409

    hotel_data = HotelRepository.create_hotel(current_user.id, data["hotel_name"], data["city"])

    return jsonify({'hotel': hotel_data}), 201


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
        return jsonify({'error': 'No hotel found!'}), 404

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

    hotel = Hotel.query.filter_by(id=hotel_id).first()
    client = Client.query.filter_by(id=current_user.id).first()

    calculated_distance = 0
    if client:
        try:
            city_user = CityChecker(current_user.city)
            city_hotel = CityChecker(hotel.city)
            coordinates_user = city_user.get_city_coordinates()
            coordinates_hotel = city_hotel.get_city_coordinates()

            coordinates_origin = coordinates_user['lon'], coordinates_user['lat']
            coordinates_destination = coordinates_hotel['lon'], coordinates_hotel['lat']

            distance = DistanceCalculator(coordinates_origin, coordinates_destination)
            calculated_distance += distance.calculate_distance()
        except ConnectionError:
            return jsonify({"error": "Connection error with external API"}), 503
        except Exception as e:
            return jsonify({"error": str(e)}), 503

    else:
        return jsonify({'error': 'No user found'}), 404
    hotel_data = HotelRepository.get_one_by_id_with_distance(hotel_id, calculated_distance)

    if not hotel:
        return jsonify({'error': 'No hotel found'}), 404

    return jsonify(hotel_data), 200


@hotel_blueprint.route("/hotels/search", methods=["GET"])
@token_required
def search_hotel_params(current_user):
    """
        Get hotel
        ---
        tags:
          - hotels
        parameters:
          - name: date_from
            in: query
            required: true
          - name: date_to
            in: query
            required: true
          - name: city
            in: query
            required: false
          - name: hotel_name
            in: query
            required: false
        security:
          - Bearer: []
        responses:
          200:
            description: Hotel found
        """
    hotel_name = request.args.get('hotel_name')
    city = request.args.get('city')
    date_from_params = request.args.get('date_from')
    date_to_params = request.args.get('date_to')

    hotel = Hotel.query.filter_by(hotel_name=hotel_name).first()
    client = Client.query.filter_by(id=current_user.id).first()

    date_from = datetime.strptime(date_from_params, "%Y-%m-%d").replace(hour=15, minute=0, second=0)
    date_to = datetime.strptime(date_to_params, "%Y-%m-%d")

    reservations = Reservation.query.filter(
        Reservation.hotel_id == hotel.id,
        (Reservation.date_from <= date_to) & (date_from <= Reservation.date_to)
    ).all()
    if reservations:
        return jsonify({'error': 'no free apartments'}), 404

    if hotel_name:
        if not hotel:
            return jsonify({'error': 'No hotel found'}), 404
        calculated_distance = 0
        if client:
            try:
                city_user = CityChecker(current_user.city)
                city_hotel = CityChecker(hotel.city)
                coordinates_user = city_user.get_city_coordinates()
                coordinates_hotel = city_hotel.get_city_coordinates()

                coordinates_origin = coordinates_user['lon'], coordinates_user['lat']
                coordinates_destination = coordinates_hotel['lon'], coordinates_hotel['lat']

                distance = DistanceCalculator(coordinates_origin, coordinates_destination)
                calculated_distance += distance.calculate_distance()
            except ConnectionError:
                return jsonify({"error": "Connection error with external API"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 503

        else:
            return jsonify({'error': 'No user found'}), 404
        hotel_data = HotelRepository.get_one_by_id_with_distance(hotel.id, calculated_distance)

        return jsonify(hotel_data), 200

    if city:
        calculated_distance = 0
        if client:
            try:
                city_user = CityChecker(current_user.city)
                searched_city = CityChecker(city)
                city_exists = searched_city.check_city_existence()
                if not city_exists:
                    return jsonify({'error': 'No city found'}), 404

                coordinates_user = city_user.get_city_coordinates()
                coordinates_city = searched_city.get_city_coordinates()

                coordinates_origin = coordinates_user['lon'], coordinates_user['lat']
                coordinates_destination = coordinates_city['lon'], coordinates_city['lat']

                distance = DistanceCalculator(coordinates_origin, coordinates_destination)
                calculated_distance += distance.calculate_distance()
            except ConnectionError:
                return jsonify({"error": "Connection error with external API"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 503

        else:
            return jsonify({'error': 'No user found'}), 404

        hotel_data = HotelRepository.get_all_from_city(city, calculated_distance)

        return jsonify(hotel_data), 200
