# app/__init__.py

from flask import Flask
from .controllers.estudiante_controller import estudiante_bp
def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')

    return app
