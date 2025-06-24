from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..services.general_service import GeneralService

router = APIRouter()
service = GeneralService()
@router.get('/niveles')
async def niveles():
    try:
        niveles = await service.obtener_niveles()

        if not niveles:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Niveles no encontrados"})
        
        return {"result":"ok", "message":"Niveles obtenidos","data": niveles}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})


@router.get('/materias')
async def materias():
    try:
        materias = await service.obtener_materias()

        if not materias:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Materias no encontradas"})
        
        return {"result":"ok", "message":"Materias obtenidas","data": materias}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})


@router.get('/aulas')
async def aulas():
    try:
        aulas = await service.obtener_aulas()

        if not aulas:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Aulas no encontradas"})
        
        return {"result":"ok", "message":"Aulas obtenidas","data": aulas}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})

@router.get('/paralelos')
async def paralelos():
    try:
        paralelos = await service.obtener_paralelos()

        if not paralelos:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Paralelos no encontrados"})
        
        return {"result":"ok", "message":"Paralelos obtenidos","data": paralelos}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})
    

@router.post('/paralelo/registrar')
async def registrar(request : Request):

    try:
        paralelos = await request.json()

        if await service.crear_paralelos(paralelos):
            return JSONResponse(status_code=201,content={"result":"ok", "message":"Paralelos registrados"})
        else:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Paralelos no registrados"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500,content={"reult":"error", "message": "error del servidor", "error": str(e)})
    

@router.post('/horario/registrar')
async def registrar(request : Request):

    try:
        horarios = await request.json()
        registrado, error = await service.crear_horario(horarios)
        if registrado:
            return JSONResponse(status_code=200,content={"result":"ok", "message":"Horarios registrados"})
        else:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Horarios no registrados"})
        
    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message": "error del servidor", "error": error})
    