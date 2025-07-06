from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from scipy.spatial.distance import cosine

from app.models.docente import Docente
from app.services.docente_service import DocenteService
from ..services.usuario_service import UsuarioService
from ..models.usuario import Usuario, UsuarioCompleto
import insightface
import base64, numpy as np, cv2
from passlib.context import CryptContext
from ..services.face_service import FaceService
from ..utils.convertir_imagen import convertir_imagen_a_webp
from ..models.usuario import Usuario, Rostro
from ..models.estudiante import Estudiante, EstudianteCompleto
from ..models.asistencia import Asistencia
from ..services.asistencia_service import AsistenciaService
from ..services.estudiante_service import EstudianteService

router = APIRouter()
model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post('/asistencia/registrar')
async def reconocer_rostro(request : Request): 
    
    try:
        umbral = 0.6
        data = await request.json()
        # Decodificar imagen base64
        img_data = base64.b64decode(data.get("imagen").split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #Detectar rostro
        faces = model.get(img)

        if not faces:
            return JSONResponse(status_code=400,content={"result":"error", "message":"No se encontraron rostros en la imagen"})

        #Obtener rostro
        emmbedding_detectado = faces[0].embedding
        usuarios = request.app.state.rostros_cache


        for item in usuarios:

            dist = cosine(emmbedding_detectado, item.emmbedding)
            if dist < umbral:
                return JSONResponse(status_code=200,content={"result":"ok", "message":"Usuario reconocido","confianza": 1-dist, "usuario": {"id": item.usuario_id}})

        return JSONResponse(status_code=400,content={"result":"error", "message":"Usuario no reconocido"})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500,content={"error": str(e)})
    
   

@router.post('/registrar/rostro')
async def registrar_rostro(request : Rostro):

    try:
        #Registrando rostro
        imagen_b64 = request.foto

        # Decodificar imagen base64
        img_data = base64.b64decode(imagen_b64.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #Detectar rostro
        faces = model.get(img)
        if not faces:
            return JSONResponse(status_code=400,content={"result":"error", "message":"No se encontraron rostros en la imagen"})

        #Obtener rostro
        face = faces[0]
        emmbedding = face.embedding.tolist()

        #guardar imagen
        image_path = convertir_imagen_a_webp(img_data)

        request.emmbedding = emmbedding
        request.image_path = image_path

        if (await FaceService.registrar_rostro(request)):

            return JSONResponse(status_code=200,content={"result":"ok", "message":"Rostro registrado para el usuario"})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"No se pudo registrar el rostro para el usuario"})
        
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500,content={"error": str(e)})

@router.post('/registrar')
async def registrar(request : Usuario):
    if (await UsuarioService.crear_usuario_admin(request)):
        return JSONResponse(status_code=200,content={"result":"ok", "message":"Usuario registrado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Usuario no registrado"})



@router.post('/login')
async def login(request : Request):
    try:
        data = await request.json()

        user : UsuarioCompleto = await UsuarioService.authenticate(data.get("username"));

        if not user:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Credenciales incorrectas"})

        if pwd_context.verify(data.get("password"), user.usuario.password_hash):

            if user.rostro.image_path:
                url = f"http://localhost:5000/static/fotos/{user.rostro.image_path}"
                user.rostro.image_path = url

            if  user.rol.nombre == "ESTUDIANTE":
                estudiante : Estudiante = await EstudianteService.obtener_estudiante_by_usuario(user.usuario.id)
                return {"result":"ok", "message":"Usuario autenticado","data": {"usuario": user, "estudiante": estudiante}}
            elif user.rol.nombre == "DOCENTE":
                docente : Docente = await DocenteService.obtener_docente_by_usuario(user.usuario.id)
                return {"result":"ok", "message":"Usuario autenticado","data": {"usuario": user, "docente": docente}}
        
            return {"result":"ok", "message":"Usuario autenticado","data": {"usuario": user}}
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Credenciales incorrectas"})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500,content={"error": str(e)})
    

@router.get('/asistencia/registrar/{usuario_id}')
def registrar_asistencia(usuario_id : int):

    try:
        if AsistenciaService.registrar_asistencia(usuario_id):
            return JSONResponse(status_code=200,content={"result":"ok", "message":"Asistencia registrada"})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Asistencia no registrada"})

    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})
    
@router.delete('/eliminar/{id}')
async def eliminar(id : int):

    if (await UsuarioService.eliminar_usuario(id)):
        return JSONResponse(status_code=200,content={"result":"ok", "message":"Usuario eliminado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Usuario no eliminado"})
    
@router.post('/actualizar/cache')
async def actualizar_cache(request : Request):
    request.app.state.rostros_cache = await FaceService.obtener_rostros()