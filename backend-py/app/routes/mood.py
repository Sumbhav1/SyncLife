from flask import Blueprint, g, jsonify
from ..models.user import MOODS
from ..utils import ValidationError, json_body, require_auth

mood_bp = Blueprint('mood', __name__, url_prefix='/mood')


@mood_bp.route('/set', methods=['POST'])
@require_auth
def set_mood():
    mood = json_body().get("mood")
    if mood not in MOODS:
        raise ValidationError(f"mood must be one of: {', '.join(MOODS)}")

    g.user.set_mood(mood)
    return jsonify({"message": "Mood updated successfully"}), 200
