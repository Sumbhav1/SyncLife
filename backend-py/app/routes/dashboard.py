from flask import Blueprint, g, jsonify
from ..utils import require_auth

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

EMPTY_DAILY_LOG = {
    "total_calories": 0,
    "sleep_hours": 0,
    "meals_count": 0,
    "goals_met": False,
    "streak": 0,
    "mood": None
}


@dashboard_bp.route("/fetch", methods=["GET"])
@require_auth
def fetch_dashboard():
    settings = g.user.get_settings()
    if settings is None:
        return jsonify({"message": "Couldn't find user settings"}), 404

    return jsonify({
        "message": "Dashboard data fetched successfully",
        "payload": {
            "settings": {
                "caloriesNeeded": settings["calories"],
                "mealsNeeded": settings["meals"],
                "bedtime": settings["bedtime"],
                "wakeupTime": settings["wakeupTime"]
            },
            "dailyLog": g.user.get_daily_log() or EMPTY_DAILY_LOG,
            "recentLogs": g.user.get_recent_logs()
        }
    }), 200
