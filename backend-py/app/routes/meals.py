from flask import Blueprint, g, jsonify
from ..utils import json_body, parse_number, require_auth, require_fields

meal_bp = Blueprint('meals', __name__, url_prefix='/meals')


@meal_bp.route('/add', methods=['POST'])
@require_auth
def add():
    data = json_body()
    require_fields(data, "total_calories")
    calories = parse_number(data["total_calories"], "total_calories", 0, 20000)

    g.user.add_meal(round(calories))
    return jsonify({"message": "Meal added successfully"}), 200
