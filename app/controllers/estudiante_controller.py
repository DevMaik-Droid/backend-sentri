from collections import defaultdict
from dataclasses import asdict
from fastapi.responses import JSONResponse
import base64, os, cv2, numpy as np
from fastapi import APIRouter

from ..models.general import ParaleloCompleto
from ..models.estudiante import Estudiante, EstudianteCompleto, Inscripcion
from ..services.estudiante_service import EstudianteService

router = APIRouter()
service = EstudianteService()
@router.post('/registrar')
async def registrar(request : EstudianteCompleto):
    if (await service.crear_estudiante(request)):
        return {"result":"ok", "message":"Estudiante registrado"}
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no registrado"})


@router.post('/registrar/varios')
async def registrar_varios(estudiantes : list[EstudianteCompleto]):

    if (await service.crear_estudiantes(estudiantes)):

        return {"result":"ok", "message":"Estudiantes registrados"}
    else:
        return JSONResponse(status_code=404,content={"result":"error", "message":"Estudiantes no registrados"})


@router.get('/obtener/todos')
async def obtener_todos():

    try:
        estudiantes : list[EstudianteCompleto] = await service.obtener_estudiantes_all()

        if not estudiantes:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Estudiantes no encontrados"})
        
        return {"result":"ok", "message":"Estudiantes obtenidos","data": estudiantes}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})
    



@router.get('/obtener/{id}')
async def obtener_id(id : int):
    estudiante : EstudianteCompleto = await service.obtener_estudiante(id)

    if estudiante:
        return {"result":"ok", "message":"Estudiante obtenido","data": estudiante}
    else:
        return JSONResponse(status_code=404,content={"result":"error", "message":"Estudiante no encontrado"})
    
@router.get('/obtener/usuario/{id}')
async def obtener_id(id : int):
    estudiante : Estudiante = await service.obtener_estudiante_by_usuario(id)

    if estudiante:
        return {"result":"ok", "message":"Estudiante obtenido","data": estudiante}
    else:
        return JSONResponse(status_code=404,content={"result":"error", "message":"Estudiante no encontrado"})
    
@router.put('/actualizar')
async def actualizar(request : EstudianteCompleto):

    if (await service.actualizar_estudiante(request)):
        return {"result":"ok", "message":"Estudiante actualizado"}
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no actualizado"})


@router.post('/inscripcion/materias')
async def inscripcion(request : Inscripcion):

    if (await service.inscribir_estudiante(request)):
        return {"result":"ok", "message":"Estudiante inscrito"}
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no inscrito"})
    
@router.get('/paralelos/{id}')
async def paralelos(id : int):

    try:
        paralelos = await service.obtener_materias_estudiante(id)

        if not paralelos:
            return JSONResponse(status_code=404,content={"result":"error", "message":"Materias no encontradas"})
        
        return {"result":"ok", "message":"Materias obtenidas","data": paralelos}

    except Exception as e:
        return JSONResponse(status_code=500,content={"result":"error", "message":"error del servidor", "error": str(e)})
    