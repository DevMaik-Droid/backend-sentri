from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..services.docente_service import DocenteService
from ..models.docente import DocenteData

router = APIRouter()
service = DocenteService()

@router.post('/registrar')
async def registrar(request : DocenteData):
    try:
        if (await service.crear_docente(request)):
            return JSONResponse(status_code=200,content={"result":"ok", "message":"Docente registrado"})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Docente no registrado"})
    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})
@router.put('/actualizar')
async def actualizar(request : DocenteData):

    if (await service.actualizar_docente(request)):
        return JSONResponse(status_code=200,content={"result":"ok", "message":"Docente actualizado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Docente no actualizado"})

@router.get('/obtener/{id}')
async def obtener(id: int):
    docente = await service.obtener_docente(id)
    if docente is None:
        return JSONResponse(status_code=404,content={"result":"error", "message":"Docente no encontrado"})
    else:
        return JSONResponse(status_code=200,content=docente)
@router.get('/obtener/todos')
async def obtener_todos():

    docentes : list[DocenteData] = await service.obtener_docentes_all()
    if docentes:
        return {"result":"ok", "message":"Docentes obtenidos","data": docentes}
    else:
        return {"result":"error", "message":"Docentes no encontrados"}