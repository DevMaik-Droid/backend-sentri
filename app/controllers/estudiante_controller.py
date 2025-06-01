from flask import request, jsonify, Blueprint
from ..models.usuario import Usuario
from ..models.estudiante import Estudiante
from ..services.estudiante_service import EstudianteService
from ..services.usuario_service import UsuarioService
from ..services.estudiante_service import EstudianteService

estudiante_bp = Blueprint('estudiante', __name__)

@estudiante_bp.route('/registrar', methods=['POST'])
def registrar():
    try:
        data = request.json

        usuario = Usuario(data["nombre"], data["apellido"], data["cedula"], data["email"], data["username"], data["password_hash"], "estudiante");
        id = UsuarioService.crear_usuario(usuario)

        estudiante = Estudiante(data["matricula"], Usuario(id=id))

        result = EstudianteService.crear_estudiante(estudiante)

        return jsonify({"result": "Estudiante registrado", "id": result}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
