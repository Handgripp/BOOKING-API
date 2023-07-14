from flask import Blueprint, request, jsonify
from src.repositories.owner_repository import OwnerRepository

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
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

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
