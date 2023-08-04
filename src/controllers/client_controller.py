import datetime
import json
import jwt
from flask import Blueprint, request, jsonify, current_app
from src.controllers.auth_controller import token_required
from src.models.client_model import Client
from src.models.owner_model import Owner
from src.repositories.client_repository import ClientRepository
from jsonschema import validate, ValidationError
from src.schemas.client_schema import create_client_schema
from src.services.geoapi import CityChecker

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
          id: Client
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
              example: "Kołobrzeg"
    responses:
      201:
        description: The client inserted in the database
    """
    rabbitmq = current_app.config["RABBITMQ"]
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

    try:
        city = CityChecker(data["city"])
        city_checker = city.check_city_existence()
    except ConnectionError:
        return jsonify({"error": "Connection error with external API"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 503

    if not city_checker:
        return jsonify({'error': 'City does not exist'}), 404

    ClientRepository.create_client(data["first_name"], data["last_name"], data["city"], data["email"], data["password"])

    token = jwt.encode(
        {'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
         'user_type': 'client'},
        'thisissecret',
        algorithm='HS256')

    mail = {
        'email': data['email'],
        'subject': "Email confirmation (BOOKING)",
        'body': f"http://127.0.0.1:5000/clients/confirm-email?token={token}"
    }
    rabbitmq.send_message(json.dumps(mail))

    return jsonify({'message': 'New user created'}), 201


@client_blueprint.route("/clients/<user_id>", methods=["GET"])
@token_required
def get_one(current_user, user_id):
    """
        Get client
        ---
        tags:
          - clients
        parameters:
          - name: user_id
            in: path
            required: true
        security:
          - Bearer: []
        responses:
          200:
            description: The client successfully returned
        """
    user_data = ClientRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200


@client_blueprint.route("/clients/confirm-email", methods=["GET"])
def confirm_email():
    token = request.args.get('token')
    data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
    if not token:
        return jsonify({'error': 'Bad request'}), 400

    client = Client.query.filter_by(email=data['email']).first()

    if not client or client.is_email_confirmed:
        return jsonify({'error': 'Bad request'}), 400

    ClientRepository.confirm_email(client)

    return jsonify({'message': 'Email confirmed'}), 200
