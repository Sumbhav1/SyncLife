import requests
from flask import Blueprint, jsonify, request
from ..config import Config
from ..utils import parse_number, require_auth

# Proxies Spoonacular so the API key stays on the server instead of in the browser bundle
ingredients_bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

SPOONACULAR_URL = "https://api.spoonacular.com/food/ingredients"


def _spoonacular_get(path, params):
    if not Config.SPOONACULAR_KEY:
        return None, (jsonify({"error": "Ingredient search is not configured"}), 503)
    try:
        response = requests.get(
            f"{SPOONACULAR_URL}{path}",
            params={**params, "apiKey": Config.SPOONACULAR_KEY},
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException:
        return None, (jsonify({"error": "Ingredient service unavailable"}), 502)
    return response.json(), None


@ingredients_bp.route('/search', methods=['GET'])
@require_auth
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"results": []}), 200
    data, error = _spoonacular_get("/search", {"query": query, "number": 5})
    if error:
        return error
    results = [{"id": r["id"], "name": r["name"]} for r in data.get("results", [])]
    return jsonify({"results": results}), 200


@ingredients_bp.route('/<int:ingredient_id>/calories', methods=['GET'])
@require_auth
def calories(ingredient_id):
    grams = parse_number(request.args.get("grams", 100), "grams", 1, 5000)
    data, error = _spoonacular_get(f"/{ingredient_id}/information", {"amount": grams, "unit": "g"})
    if error:
        return error
    nutrients = data.get("nutrition", {}).get("nutrients", [])
    kcal = next((n["amount"] for n in nutrients if n.get("name") == "Calories"), 0)
    return jsonify({"name": data.get("name"), "calories": kcal}), 200
