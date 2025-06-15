from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from scipy.spatial.distance import cosine
from ..services.usuario_service import UsuarioService

import insightface
import base64, numpy as np, cv2


router = APIRouter()
model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)

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