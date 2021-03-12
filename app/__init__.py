from flask import Flask
from flask_cors import CORS
from flask_assets import Bundle, Environment

def create_app():
    app = Flask(__name__)
    CORS(app)
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    return app
