from dataclasses import asdict
from fastapi.responses import JSONResponse
import base64, os, cv2, numpy as np
import insightface
from datetime import datetime

from fastapi import APIRouter
from ..database.conexion import Conexion

from ..models.estudiante import EstudianteCreate
from ..models.usuario import Usuario

from ..services.estudiante_service import EstudianteService
from ..services.usuario_service import UsuarioService
from ..services.face_service import FaceService
from ..utils.convertir_imagen import convertir_imagen_a_webp

router = APIRouter()

model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)

UPLOAD_FOLDER = 'app/static/fotos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get('/listar')
def listar():
    estudiantes = EstudianteService.obtener_estudiantes_all()

    if estudiantes:
        json_estudiantes = [asdict(e) for e in estudiantes]
        return {"result":"ok", "message":"Estudiantes listados","data": json_estudiantes}
    else:
        return {"result":"error", "message":"No se encontraron estudiantes"}


@router.post('/registrar')
async def registrar(request : EstudianteCreate):

    print(request)
    if (await EstudianteService.crear_estudiante(request)):

        return JSONResponse(status_code=200,content={"result":"ok", "message":"Estudiante registrado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no registrado"})

@router.post('/registrar/varios')
async def registrar_varios(estudiantes : list[EstudianteCreate]):

    if (await EstudianteService.crear_estudiantes(estudiantes)):

        return JSONResponse(status_code=200,content={"result":"ok", "message":"Estudiantes registrados"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiantes no registrados"})


# @router.post('/registrar')
# async def registrar(request : EstudianteCreate):

#     try:
#         #Registrando rostro
#         imagen_b64 = request.estudiante.imagen

#         # Decodificar imagen base64
#         img_data = base64.b64decode(imagen_b64.split(",")[1])
#         np_arr = np.frombuffer(img_data, np.uint8)
#         img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if img is None:
#                 return JSONResponse(status_code=400,content={"result": "error", "message": "Imagen no válida o corrupta"})
        
#         #Detectar rostro
#         faces = model.get(img)
#         if not faces:
#             return JSONResponse(status_code=400,content={"result":"error", "message":"No se encontraron rostros en la imagen"})

#         #Obtener rostro
#         face = faces[0]
#         emmbedding = face.embedding.tolist()

#         #guardar imagen
#         image_path = convertir_imagen_a_webp(img_data)

#         async with Conexion() as conn:
#             async with conn.transaction():
#                 #Registrando usuario
#                 usuario : Usuario = request.usuario
#                 id_usuario = await UsuarioService.crear_usuario(usuario, conn)

#                 #Registrando estudiante
#                 estudiante = Estudiante(matricula=request.estudiante.matricula,id_usuario = id_usuario)
#                 await EstudianteService.crear_estudiante(estudiante, conn)

#                 #Registrando rostro
#                 await FaceService.registrar_rostro(image_path, emmbedding,id_usuario, conn);

#         return JSONResponse(status_code=201,content={"result":"ok", "message":"Estudiante registrado"})
#     except KeyError as e:
#         return JSONResponse(status_code=400,content={"error": f"Falta campo requerido: {str(e)}"})
#     except Exception as e:
#         return JSONResponse(status_code=500,content={"error": str(e)})


# @estudiante_bp.route('/actualizar/<int:id>', methods=['PUT'])
# def actualizar(id):
#     try:
#         data = request.json
        
#         usuario = Usuario()
#         usuario.id = id
#         usuario.nombre = data["usuario"]["nombre"]
#         usuario.apellido = data["usuario"]["apellido"]
#         usuario.cedula = data["usuario"]["cedula"]
#         usuario.email = data["usuario"]["email"]
#         usuario.username = data["usuario"]["username"]
#         usuario.password_hash = data["usuario"]["password_hash"]
#         usuario.rol = "ESTUDIANTE"

#         UsuarioService.actualizar_usuario(usuario)
#         estudiante = Estudiante()
#         estudiante.id = id
#         estudiante.matricula = data["matricula"]

#         EstudianteService.actualizar_estudiante(estudiante)

#         return jsonify({"result":"ok", "message":"Estudiante actualizado"}), 200
#     except KeyError as e:
#         return jsonify({"error": f"Falta campo requerido: {str(e)}"}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    

# @estudiante_bp.route('/eliminar/<int:id>', methods=['DELETE'])
# def eliminar(id):
#     try:
#         UsuarioService.eliminar_usuario(id)
#         return jsonify({"result":"ok", "message":"Estudiante eliminado"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# @estudiante_bp.route('/asistencia/<int:id_estudiante>', methods=['GET'])
# def registrar_asistencia(id_estudiante):
#     try:

#         actual = datetime.now()
#         asistencia = Asistencia()
#         asistencia.fecha = actual.date()
#         asistencia.hora = actual.time()
#         asistencia.estado = "PRESENTE"
#         asistencia.estudiante_id = id_estudiante

#         AsistenciaService.registrar_asistencia(asistencia)

#         return jsonify({"result":"ok", "message":"Asistencia registrada"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500