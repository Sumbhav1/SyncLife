from flask import Blueprint, g, jsonify
from ..utils import json_body, parse_number, parse_time, require_auth, require_fields

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route("/fetch", methods=["GET"])
@require_auth
def fetch_settings():
    settings = g.user.get_settings()
    if settings is None:
        return jsonify({"error": "No settings saved yet"}), 404
    return jsonify(settings), 200


@settings_bp.route('/set', methods=["POST"])
@require_auth
def set_settings():
    data = json_body()
    require_fields(data, "calories", "bedtime", "wakeupTime", "sleep", "meals")

    g.user.save_settings(
        calories=parse_number(data["calories"], "calories", 1, 20000, integer=True),
        meals=parse_number(data["meals"], "meals", 1, 20, integer=True),
        sleep=parse_number(data["sleep"], "sleep", 0, 24),
        bedtime=parse_time(data["bedtime"], "bedtime"),
        wakeup_time=parse_time(data["wakeupTime"], "wakeupTime"),
        notifications_meals=bool(data.get("notificationsMeals")),
        notifications_sleep=bool(data.get("notificationsSleep"))
    )
    return jsonify({
        "message": "Settings saved successfully",
        "user": g.user.to_public_dict()
    }), 200
