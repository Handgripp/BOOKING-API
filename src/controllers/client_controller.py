from flask import Blueprint, request, jsonify

from src.models.client_model import Client
from src.models.owner_model import Owner
from src.repositories.client_repository import ClientRepository
from jsonschema import validate, ValidationError
from src.schemas.client_schema import create_client_schema


client_blueprint = Blueprint('client', __name__)


@client_blueprint.route("/clients", methods=["POST"])
def create_client():
    """
    Create client
    ---
    tags:
      - clients
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Owner
          required:
            - first_name
            - last_name
            - city
            - email
            - password
          properties:
            first_name:
              type: string
              description: Client first_name
              example: "Kamil"
            last_name:
              type: string
              description: Client last_name
              example: "Malkowski"
            email:
              type: string
              description: Client email
              example: "johnnn@doe.com"
            password:
              type: string
              description: Client password
              example: "qwerty"
            city:
              type: string
              description: Client city
              example: "Kolobrzeg"
    responses:
      201:
        description: The owner inserted in the database
    """

    data = request.json
    try:
        validate(data, create_client_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    email_from_clients = Client.query.filter_by(email=data['email']).first()
    email_from_owners = Owner.query.filter_by(email=data['email']).first()

    if email_from_clients or email_from_owners:
        return jsonify({'error': 'User with that email already exists'}), 409

    ClientRepository.create_client(data["first_name"], data["last_name"], data["city"], data["email"], data["password"])

    return jsonify({'message': 'New user created'}), 201


@client_blueprint.route("/clients/<user_id>", methods=["GET"])
def get_one(user_id):
    """
        Get client
        ---
        tags:
          - clients
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          200:
            description: The owner successfully returned
        """
    user_data = ClientRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200
