from flask import Blueprint, jsonify, request
from models import User, db, Character, Location
from sqlalchemy import select


api = Blueprint("api", __name__)


@api.route("/users", methods=["GET"])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 400
    return jsonify(user.serialize()), 200


@api.route("/character", methods=["GET"])
def get_character():
    characters = db.session.execute(select(Character)).scalars().all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200

@api.route("/character/<int:character_id>", methods=["GET"])
def get_character_id(character_id):
    character = db.session.get(Character, character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 400
    return jsonify(character.serialize()), 200

@api.route("/location", methods=["GET"])
def get_location():
    locations = db.session.execute(select(Location)).scalars().all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200

@api.route("/location/<int:location_id>", methods=["GET"])
def get_location_id(location_id):
    location = db.session.get(Location, location_id)
    if not location:
        return jsonify({"error": "Location not found"}), 400
    return jsonify(location.serialize()), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"error" : "All data is required"}), 400
    new_user = User (
        email = data["email"],
        password = data["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"usuario" : "creado correctamente"}), 201


