# app/__init__.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from .controllers.chat_controller import router as chat_router
from .controllers.estudiante_controller import router as estudiante_router
from .controllers.usuario_controller import router as usuario_router
from .controllers.general_controller import router as general_router
from .controllers.docente_controller import router as docente_router
from .services.face_service import FaceService


def create_app():

    # @asynccontextmanager
    # async def lifespan(app: FastAPI):
    #     app.state.rostros_cache = await FaceService.obtener_rostros()
    #     yield

    app = FastAPI()
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Origenes permitidos
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


    return app
