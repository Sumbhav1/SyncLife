from flask import Blueprint, g, jsonify
from ..utils import json_body, parse_time, require_auth, require_fields

sleep_bp = Blueprint('sleep', __name__, url_prefix='/sleep')


@sleep_bp.route('/add', methods=['POST'])
@require_auth
def add():
    data = json_body()
    require_fields(data, "bedtime", "wakeuptime")

    hours = g.user.add_sleep(
        parse_time(data["bedtime"], "bedtime"),
        parse_time(data["wakeuptime"], "wakeuptime")
    )
    return jsonify({"message": "Sleep added successfully", "sleep_hours": hours}), 200
