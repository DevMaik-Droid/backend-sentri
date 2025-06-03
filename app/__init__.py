# app/__init__.py

from flask import Flask
from flask_cors import CORS
from .controllers.estudiante_controller import estudiante_bp
from .controllers.docente_controller import docente_bp
def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')
    app.register_blueprint(docente_bp, url_prefix='/docente')

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
