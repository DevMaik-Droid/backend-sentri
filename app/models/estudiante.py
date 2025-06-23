from typing import Optional
from pydantic import BaseModel, Field
from .usuario import Usuario
from datetime import date

class Estudiante(BaseModel):
    id: Optional[int] = None
    codigo: Optional[str] = Field(None, min_length=8)
    nivel_id : Optional[int] = None
    usuario_id: Optional[int] = None

class EstudianteCreate(BaseModel):
    usuario: Usuario
    estudiante: Estudiante

class Inscripcion(BaseModel):
    id: Optional[int] = None
    estudiante_id: int = Field(..., gt=0)
    paralelo_id: int = Field(..., gt=0)
    fecha_inscripcion: Optional[date] = None
    estado: Optional[str] = Field(None, min_length=3)

    