from flask import Blueprint, jsonify, request
from models import User, db, Character, Location
from sqlalchemy import select


api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200

