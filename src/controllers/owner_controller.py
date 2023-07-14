from flask import Blueprint, request, jsonify

from src.models.client_model import Client
from src.models.owner_model import Owner
from src.repositories.owner_repository import OwnerRepository
from jsonschema import validate, ValidationError
from src.schemas.owner_schema import create_owner_schema


owner_blueprint = Blueprint('owner', __name__)


@owner_blueprint.route("/owners", methods=["POST"])
def create_owner():
    """
    Create owner
    ---
    tags:
      - owners
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Owner
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: Owner email
              example: "john@doe.com"
            password:
              type: string
              description: Owner password
              example: "qwerty"
    responses:
      201:
        description: The owner inserted in the database
    """

    data = request.json
    try:
        validate(data, create_owner_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    email_from_clients = Client.query.filter_by(email=data['email']).first()
    email_from_owners = Owner.query.filter_by(email=data['email']).first()

    if email_from_clients or email_from_owners:
        return jsonify({'error': 'User with that email already exists'}), 409

    OwnerRepository.create_owner(data["email"], data["password"])

    return jsonify({'message': 'New user created'}), 201


@owner_blueprint.route("/owners/<user_id>", methods=["GET"])
def get_one(user_id):
    """
        Get owner
        ---
        tags:
          - owners
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          200:
            description: The owner successfully returned
        """
    user_data = OwnerRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200
