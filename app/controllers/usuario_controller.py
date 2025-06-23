from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from scipy.spatial.distance import cosine
from ..services.usuario_service import UsuarioService
from ..models.usuario import Usuario
import insightface
import base64, numpy as np, cv2
from passlib.context import CryptContext
from ..services.face_service import FaceService
from ..utils.convertir_imagen import convertir_imagen_a_webp
from ..models.usuario import Usuario, RostroUser
from ..models.asistencia import Asistencia
from ..services.asistencia_service import AsistenciaService

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
        emmbedding = faces[0].embedding
        usuarios = request.app.state.rostros_cache

        for usuario_id, nombre, apellido, rol, emm_guardado in usuarios:
            dist = cosine(emmbedding, emm_guardado)
            if dist < umbral:
                return JSONResponse(status_code=200,content={"result":"ok", "message":"Usuario reconocido","confianza": 1-dist, "usuario": {"id": usuario_id, "nombre": nombre, "apellido": apellido, "rol": rol}})

        return JSONResponse(status_code=400,content={"result":"error", "message":"Usuario no reconocido"})

    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})
    
   

@router.post('/registrar/rostro')
async def registrar_rostro(request : RostroUser):

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
        emmbedding = faces[0].embedding
        request.emmbedding = emmbedding

#         #Obtener rostro
#         face = faces[0]
#         emmbedding = face.embedding.tolist()


        #guardar imagen
        image_path = convertir_imagen_a_webp(img_data)
        request.image_path = image_path

        if (await FaceService.registrar_rostro(request)):
            return JSONResponse(status_code=200,content={"result":"ok", "message":"Rostro registrado para el usuario"})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"No se pudo registrar el rostro para el usuario"})
        
    except Exception as e:
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

        usuario : Usuario = await UsuarioService.authenticate(data.get("username"));
        print(usuario)

        if pwd_context.verify(data.get("password"), usuario.password_hash):
            data = {"id": usuario.id, "nombre": usuario.nombre, "apellido": usuario.apellido, "email": usuario.email,"foto_perfil": usuario.foto_perfil, "rol": usuario.rol}

            return JSONResponse(status_code=200,content={"result":"ok", "message":"Usuario autenticado","data": data})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Credenciales incorrectas"})

    except Exception as e:
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