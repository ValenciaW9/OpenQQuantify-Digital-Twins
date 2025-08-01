# Valencia Walker's __init__.py
from flask import Flask
from backend.routes import other_existing_routes
from backend.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    # Existing route registrations...
    app.register_blueprint(auth_bp)
    # Other blueprint registrations
    return app
