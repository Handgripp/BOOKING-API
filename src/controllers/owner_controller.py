import datetime
import json
import jwt
from flask import Blueprint, request, jsonify, current_app
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
    rabbitmq = current_app.config["RABBITMQ"]
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

    token = jwt.encode(
        {'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
         'user_type': 'owner'},
        'thisissecret',
        algorithm='HS256')

    mail = {
        'email': data['email'],
        'subject': "Email confirmation (BOOKING)",
        'body': f"http://127.0.0.1:5000/owners/confirm-email?token={token}"
    }
    rabbitmq.send_message(json.dumps(mail))

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


@owner_blueprint.route("/owners/confirm-email", methods=["GET"])
def confirm_email():
    token = request.args.get('token')
    print("ee1")
    data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
    if not token:
        return jsonify({'error': 'Bad request'}), 400
    print("ee2")
    owner = Owner.query.filter_by(email=data['email']).first()

    if not owner or owner.is_email_confirmed:
        return jsonify({'error': 'Bad request'}), 400

    OwnerRepository.confirm_email(owner)

    return jsonify({'message': 'Email confirmed'}), 200
