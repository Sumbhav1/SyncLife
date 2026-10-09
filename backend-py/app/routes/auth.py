from flask import Blueprint, jsonify
from ..models.user import User
from ..utils import json_body, make_token, require_fields

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = json_body()
    require_fields(data, "email", "password")

    user = User.find_by_email(data["email"])
    # Same response for unknown email and wrong password, so emails can't be probed
    if user is None or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "token": make_token(user),
        "user": user.to_public_dict()
    }), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = json_body()
    require_fields(data, "name", "email", "password")

    user = User.create(data["name"], data["email"], data["password"])
    if user is None:
        return jsonify({"message": "Email already in use"}), 409

    return jsonify({
        "message": "Sign-up successful",
        "token": make_token(user),
        "user": user.to_public_dict()
    }), 201
