from dataclasses import asdict
import base64, os, cv2, numpy as np, uuid
import insightface
from datetime import datetime
from scipy.spatial.distance import cosine
from flask import request, jsonify, Blueprint
from ..models.usuario import Usuario
from ..models.estudiante import Estudiante
from ..services.estudiante_service import EstudianteService
from ..services.usuario_service import UsuarioService
from ..services.asistencia_service import AsistenciaService
from ..services.face_service import FaceService
from ..models.asistencia import Asistencia

estudiante_bp = Blueprint('estudiante', __name__)

model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)

UPLOAD_FOLDER = 'app/static/fotos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        #Registrando rostro
        imagen_b64 = data["imagen"]

        # Decodificar imagen base64
        img_data = base64.b64decode(imagen_b64.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #Detectar rostro
        faces = model.get(img)
        if not faces:
            return jsonify({"result":"error", "message":"No se encontraron rostros en la imagen"}), 400

        #Registrando usuario
        usuario = Usuario(nombre=data["usuario"]["nombre"],apellido= data["usuario"]["apellido"],cedula= data["usuario"] ["cedula"],email= data["usuario"]["email"],username= data["usuario"]["username"],password_hash= data["usuario"]["password_hash"], rol="ESTUDIANTE");
        id = UsuarioService.crear_usuario(usuario)
        #Registrando estudiante
        estudiante = Estudiante(matricula=data["matricula"], usuario=Usuario(id=id))
        id_estudiante = EstudianteService.crear_estudiante(estudiante)

        #Registra rostro
        face = faces[0]
        emmbedding = face.embedding.tolist()

        #guardar imagen
        file_name = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(image_path, "wb") as f:
            f.write(img_data)

        FaceService.registrar_rostro(id_estudiante, image_path, emmbedding);

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

@estudiante_bp.route('/asistencia/reconocer', methods=['POST'])
def reconocer_rostro():
    try:
        data = request.json
        umbral = 0.6

        # Decodificar imagen base64
        img_data = base64.b64decode(data["imagen"].split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #Detectar rostro
        faces = model.get(img)
        if not faces:
            return jsonify({"result":"error", "message":"No se encontraron rostros en la imagen"}), 400

        #Registra rostro
        emmbedding = faces[0].embedding

        estudiantes = EstudianteService.obtener_estudiantes_rostros()


        for estudiante_id, nombre, apellido, emm_guardado in estudiantes:
            dist = cosine(emmbedding, emm_guardado)
            if dist < umbral:
                return jsonify({"result":"ok", "message":"Estudiante reconocido", "data": {"estudiante": {"id": estudiante_id, "nombre": nombre, "apellido": apellido}}}), 200


        return jsonify({"result":"error", "message":"Estudiante no reconocido"}), 400

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