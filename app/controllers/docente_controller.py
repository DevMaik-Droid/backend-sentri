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
    


@router.get('/obtener/todos')
async def obtener_todos():

    try:
        docentes : list[DocenteData] = await service.obtener_docentes_all()
        if not docentes:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Docentes no encontrados"})
        
        return {"result":"ok", "message":"Docentes obtenidos","data": docentes}
    
    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})
        
    

@router.get('/obtener/{id}')
async def obtener_por_id(id: int):

    try:
        docente : DocenteData = await service.obtener_docente(id)
        if not docente:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Docente no encontrado"})
        
        return {"result":"ok", "message":"Docente obtenido","data": docente}
    
    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})
    
        

        
        
