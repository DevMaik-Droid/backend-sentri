from pydantic import BaseModel, Field

from .usuario import UsuarioAPI

class EstudianteAPI(BaseModel):
    matricula: str = Field(..., min_length=8)
    imagen: str = Field(..., min_length=8)

class Estudiante(BaseModel):
    matricula: str
    id_usuario: int


class EstudianteCreate(BaseModel):
    estudiante: EstudianteAPI
    usuario: UsuarioAPI