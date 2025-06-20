from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..services.general_service import GeneralService

router = APIRouter()
service = GeneralService()
@router.get('/niveles')
async def niveles():
    niveles = await service.obtener_niveles()

    niveles = [dict(nivel) for nivel in niveles]

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Niveles obtenidos","data": niveles})


@router.get('/materias')
async def materias():
    materias = await service.obtener_materias()

    json_materias = [dict(materia) for materia in materias]

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Materias obtenidas","data": json_materias})


@router.get('/aulas')
async def aulas():
    aulas = await service.obtener_aulas()

    json_aulas = [dict(aula) for aula in aulas]

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Aulas obtenidas","data": json_aulas})

@router.get('/paralelos')
async def paralelos():
    paralelos = await service.obtener_paralelos()

    json_paralelos = [dict(paralelo) for paralelo in paralelos]

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Paralelos obtenidos","data": json_paralelos})

@router.post('/paralelo/registrar')
async def registrar(request : Request):

    try:
        paralelos = await request.json()

        if await service.crear_paralelos(paralelos):
            return JSONResponse(status_code=200,content={"result":"ok", "message":"Paralelos registrados"})
        else:
            return JSONResponse(status_code=400,content={"result":"error", "message":"Paralelos no registrados"})
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
            return JSONResponse(status_code=400,content={"result":"error", "message":"Horarios no registrados"})
        
    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message": "error del servidor", "error": error})
    