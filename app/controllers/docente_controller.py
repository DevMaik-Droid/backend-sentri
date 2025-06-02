from dataclasses import asdict
from flask import request, jsonify, Blueprint

from ..services.docente_service import DocenteService
from ..models.docente import Docente
from ..services.usuario_service import UsuarioService
from ..models.usuario import Usuario

docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/registrar', methods=['POST'])
def registrar():
    try:
        data = request.json

        usuario = Usuario(nombre=data["usuario"]["nombre"],apellido= data["usuario"]["apellido"],cedula= data["usuario"] ["cedula"],email= data["usuario"]["email"],username= data["usuario"]["username"],password_hash= data["usuario"]["password_hash"], rol="DOCENTE");
        id = UsuarioService.crear_usuario(usuario)
        
        docente = Docente(materia=data["materia"], usuario=Usuario(id=id))
        DocenteService.crear_docente(docente)

        return jsonify({"result":"ok", "message":"Docente registrado"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@docente_bp.route('/listar', methods=['GET'])
def listar():
    docentes = DocenteService.obtener_docentes_all()

    if docentes:
        json_docentes = [asdict(d) for d in docentes]
        return jsonify({"result":"ok", "message":"Docentes listados","data": json_docentes}), 200
    else:
        return jsonify({"result":"error", "message":"No se encontraron docentes"}), 404

@docente_bp.route('/actualizar/<int:id>', methods=['PUT'])
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
        usuario.rol = "DOCENTE"

        UsuarioService.actualizar_usuario(usuario)

        docente = Docente()
        docente.id = id
        docente.materia = data["materia"]

        DocenteService.actualizar_docente(docente)

        return jsonify({"result":"ok", "message":"Docente actualizado"}), 200
    except KeyError as e:
        return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@docente_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    try:
        UsuarioService.eliminar_usuario(id)
        return jsonify({"result":"ok", "message":"Docente eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
