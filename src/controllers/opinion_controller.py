from flask import Blueprint, request, jsonify
from src.controllers.auth_controller import token_required
from src.models.client_model import Client
from src.models.hotel_model import Hotel
from jsonschema import validate, ValidationError

from src.models.opinion_model import Opinion
from src.repositories.opinion_repository import OpinionRepository
from src.schemas.opinion_schema import create_opinion_schema

opinion_blueprint = Blueprint('opinion', __name__)


@opinion_blueprint.route("/hotels/<hotel_id>/opinions", methods=["POST"])
@token_required
def create_opinion(current_user, hotel_id):
    """
    Create opinion
    ---
    tags:
      - opinions
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Opinion
          required:
            - text
            - rating
          properties:
            text:
              type: string
              description: text
              example: "A very nice hotel"
            rating:
              type: integer
              description: rating
              example: 5
      - name: hotel_id
        in: path
        required: true
    security:
      - Bearer: []
    responses:
      201:
        description: The opinion inserted in the database
    """

    data = request.json
    try:
        validate(data, create_opinion_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    client = Client.query.filter_by(id=current_user.id).first()

    if not client:
        return jsonify({'error': 'Bad request'}), 404

    hotel = Hotel.query.filter_by(id=hotel_id).first()

    OpinionRepository.create_opinion(hotel.id, current_user.id, data["text"], data["rating"])

    return jsonify({'message': 'New opinion created'}), 201


@opinion_blueprint.route("/hotels/<hotel_id>/opinions/<opinion_id>", methods=["GET"])
def get_one_opinion(hotel_id, opinion_id):
    """
        Get opinion
        ---
        tags:
          - opinions
        parameters:
          - name: hotel_id
            in: path
            required: true
          - name: opinion_id
            in: path
            required: true
        responses:
          200:
            description: The opinion successfully returned
        """

    hotel = Hotel.query.filter_by(id=hotel_id).first()

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    opinion = Opinion.query.filter_by(id=opinion_id).first()

    if not opinion:
        return jsonify({'error': 'No opinion found!'}), 404

    opinion_data = OpinionRepository.get_one_by_id(hotel_id, opinion_id)

    return jsonify(opinion_data), 200


@opinion_blueprint.route("/hotels/<hotel_id>/opinions", methods=["GET"])
def get_opinions(hotel_id):
    """
        Get opinions
        ---
        tags:
          - opinions
        parameters:
          - name: hotel_id
            in: path
            required: true
        responses:
          200:
            description: The opinion successfully returned
        """

    hotel = Hotel.query.filter_by(id=hotel_id).first()

    if not hotel:
        return jsonify({'error': 'No hotel found!'}), 404

    opinion_data = OpinionRepository.get_all(hotel_id)

    return jsonify(opinion_data), 200
