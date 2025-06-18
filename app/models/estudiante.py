from typing import Optional
from pydantic import BaseModel, Field
from .usuario import Usuario

class Estudiante(BaseModel):
    id: Optional[int] = None
    codigo: Optional[str] = Field(None, min_length=8)
    nivel_id : Optional[int] = None
    usuario_id: Optional[int] = None

class EstudianteCreate(BaseModel):
    usuario: Usuario
    estudiante: Estudiante
    