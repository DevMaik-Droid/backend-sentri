from dataclasses import asdict
from datetime import datetime
from flask import request, jsonify, Blueprint
from ..models.usuario import Usuario
from ..models.estudiante import Estudiante
from ..services.estudiante_service import EstudianteService
from ..services.usuario_service import UsuarioService
from ..services.asistencia_service import AsistenciaService
from ..models.asistencia import Asistencia

estudiante_bp = Blueprint('estudiante', __name__)


@estudiante_bp.route('/listar', methods=['GET'])
def listar():
    estudiantes = EstudianteService.obtener_estudiantes_all()

    if estudiantes:
        json_estudiantes = [asdict(e) for e in estudiantes]
        return jsonify({"result":"ok", "message":"Estudiantes listados","data": json_estudiantes}), 200
    else:
        return jsonify({"result":"error", "message":"No se encontraron estudiantes"}), 404
    

@estudiante_bp.route('/registrar', methods=['POST'])
def registrar():
    try:
        data = request.json

        usuario = Usuario(nombre=data["usuario"]["nombre"],apellido= data["usuario"]["apellido"],cedula= data["usuario"] ["cedula"],email= data["usuario"]["email"],username= data["usuario"]["username"],password_hash= data["usuario"]["password_hash"], rol="ESTUDIANTE");
        id = UsuarioService.crear_usuario(usuario)
        
        estudiante = Estudiante(matricula=data["matricula"], usuario=Usuario(id=id))
        EstudianteService.crear_estudiante(estudiante)

        return jsonify({"result":"ok", "message":"Estudiante registrado"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@estudiante_bp.route('/actualizar/<int:id>', methods=['PUT'])
def actualizar(id):
    try:
        data = request.json
        
        usuario = Usuario()
        usuario.id = id
        usuario.nombre = data["usuario"]["nombre"]
        usuario.apellido = data["usuario"]["apellido"]
        usuario.cedula = data["usuario"]["cedula"]
        usuario.email = data["usuario"]["email"]
        usuario.username = data["usuario"]["username"]
        usuario.password_hash = data["usuario"]["password_hash"]
        usuario.rol = "ESTUDIANTE"

        UsuarioService.actualizar_usuario(usuario)

        estudiante = Estudiante()
        estudiante.id = id
        estudiante.matricula = data["matricula"]

        EstudianteService.actualizar_estudiante(estudiante)

        return jsonify({"result":"ok", "message":"Estudiante actualizado"}), 200
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@estudiante_bp.route('/eliminar/<int:id>', methods=['DELETE'])

def eliminar(id):
    try:
        UsuarioService.eliminar_usuario(id)
        return jsonify({"result":"ok", "message":"Estudiante eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@estudiante_bp.route('/asistencia/<int:id_estudiante>', methods=['GET'])
def registrar_asistencia(id_estudiante):
    try:

        actual = datetime.now()
        asistencia = Asistencia()
        asistencia.fecha = actual.date()
        asistencia.hora = actual.time()
        asistencia.estado = "PRESENTE"
        asistencia.estudiante_id = id_estudiante

        AsistenciaService.registrar_asistencia(asistencia)

        return jsonify({"result":"ok", "message":"Asistencia registrada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500