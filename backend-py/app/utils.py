import re
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import g, jsonify, request

from .config import Config
from .models.user import User

TOKEN_LIFETIME = timedelta(hours=1)
TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$")


class ValidationError(Exception):
    """Raised for bad client input; turned into a 400 by the app's error handler."""


def make_token(user):
    payload = {
        "id": user.id,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + TOKEN_LIFETIME
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def require_auth(view):
    """Reject requests without a valid Bearer token; expose the caller as g.user."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme != "Bearer" or not token:
            return jsonify({"error": "Missing or malformed token"}), 401
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = User.find_by_id(payload.get("id"))
        if user is None:
            return jsonify({"error": "User not found"}), 401
        g.user = user
        return view(*args, **kwargs)
    return wrapper


def json_body():
    """The request's JSON object, or an empty dict if the body is missing or not an object."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def require_fields(data, *fields):
    missing = [f for f in fields if data.get(f) in (None, "")]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")


def parse_number(value, name, minimum=None, maximum=None, integer=False):
    if isinstance(value, bool):
        raise ValidationError(f"{name} must be a number")
    try:
        number = int(value) if integer else float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{name} must be a {'whole ' if integer else ''}number")
    if isinstance(value, float) and integer and not value.is_integer():
        raise ValidationError(f"{name} must be a whole number")
    if (minimum is not None and number < minimum) or (maximum is not None and number > maximum):
        raise ValidationError(f"{name} must be between {minimum} and {maximum}")
    return number


def parse_time(value, name):
    if not isinstance(value, str) or not TIME_PATTERN.match(value):
        raise ValidationError(f"{name} must be a time in HH:MM format")
    return value[:5]
