from flask import Blueprint, request, jsonify
from repositories.owner_repository import OwnerRepository
owner_blueprint = Blueprint('owner', __name__)


@owner_blueprint.route("/owners", methods=["POST"])
def create_owner():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing required fields'}), 400

    OwnerRepository.create_owner(data["email"], data["password"])

    return jsonify({'message': 'New user created'}), 201


@owner_blueprint.route("/owners/<user_id>", methods=["GET"])
def get_one(user_id):
    user_data = OwnerRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200
