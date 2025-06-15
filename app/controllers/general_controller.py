from fastapi import APIRouter
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

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Materias obtenidas","materias": json_materias})


@router.get('/aulas')
async def aulas():
    aulas = await service.obtener_aulas()

    json_aulas = [dict(aula) for aula in aulas]

    return JSONResponse(status_code=200,content={"result":"ok", "message":"Aulas obtenidas","aulas": json_aulas})