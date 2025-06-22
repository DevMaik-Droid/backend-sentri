from dataclasses import asdict
from fastapi.responses import JSONResponse
import base64, os, cv2, numpy as np
import insightface
from datetime import datetime
from fastapi import APIRouter
from ..models.estudiante import EstudianteCreate
from ..services.estudiante_service import EstudianteService

router = APIRouter()

model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)

@router.post('/registrar')
async def registrar(request : EstudianteCreate):
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


@router.get('/obtener/todos')
async def obtener_todos():

    estudiantes : list[EstudianteCreate] = await EstudianteService.obtener_estudiantes_all()

    print(estudiantes)

    if estudiantes:
        return {"result":"ok", "message":"Estudiantes obtenidos","data": estudiantes}
    else:
        return {"result":"error", "message":"Estudiantes no encontrados"}

@router.get('/obtener/{id}')
async def obtener_id(id : int):
    estudiante : EstudianteCreate = await EstudianteService.obtener_estudiante(id)

    if estudiante:
        return {"result":"ok", "message":"Estudiante obtenido","data": estudiante}
    else:
        return {"result":"error", "message":"Estudiante no encontrado"}
    
@router.put('/actualizar')
async def actualizar(request : EstudianteCreate):

    if (await EstudianteService.actualizar_estudiante(request)):
        return JSONResponse(status_code=200,content={"result":"ok", "message":"Estudiante actualizado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no actualizado"})


@router.delete('/eliminar/{id}')
async def eliminar(id : int):

    if (await EstudianteService.eliminar_estudiante(id)):
        return JSONResponse(status_code=200,content={"result":"ok", "message":"Estudiante eliminado"})
    else:
        return JSONResponse(status_code=400,content={"result":"error", "message":"Estudiante no eliminado"})
    

