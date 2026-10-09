from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from .config import Config
from .db import close_db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, origins=config.CORS_ORIGINS)
    app.teardown_appcontext(close_db)

    from .routes.auth import auth_bp
    from .routes.settings import settings_bp
    from .routes.meals import meal_bp
    from .routes.sleep import sleep_bp
    from .routes.dashboard import dashboard_bp
    from .routes.mood import mood_bp
    from .routes.ingredients import ingredients_bp
    from .utils import ValidationError

    app.register_blueprint(auth_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(meal_bp)
    app.register_blueprint(sleep_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(ingredients_bp)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        if isinstance(e, HTTPException):
            return e
        # Log the details server-side; don't leak internals to the client
        app.logger.exception("Unhandled error")
        return jsonify({"error": "Internal server error"}), 500

    return app
