import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Importa tus routers y servicios aquí
from app.controllers.chat_controller import router as chat_router
from app.controllers.usuario_controller import router as usuario_router
from app.controllers.estudiante_controller import router as estudiante_router
from app.controllers.general_controller import router as general_router
from app.controllers.docente_controller import router as docente_router
from app.services.face_service import FaceService
from app.models.usuario import Rostro

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rostros_cache = []
    rostros : list[Rostro] = await FaceService.obtener_rostros()
    if rostros:
        app.state.rostros_cache  = rostros
        print("rostro cargados", len(rostros))
    yield


app = FastAPI(lifespan=lifespan)

# Configuración de middleware y routers
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return JSONResponse(content={"message": "Hello World"})

app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(estudiante_router, prefix="/estudiante", tags=["estudiante"])
app.include_router(usuario_router, prefix="/usuario", tags=["usuario"])
app.include_router(docente_router, prefix="/docente", tags=["docente"])
app.include_router(general_router, prefix="/general", tags=["general"])
