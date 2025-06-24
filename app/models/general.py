from typing import Optional

from pydantic import BaseModel, Field
from datetime import date, time
from ..models.docente import Docente

class Horario(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    dia_semana: Optional[str] = Field(None, min_length=3)
    hora_inicio: time = None
    hora_fin: time = None
    paralelo_id: Optional[int] = Field(None, gt=0)
    aula_id: Optional[int] = Field(None, gt=0)


class Aula(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    nombre: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = Field(None, min_length=3)
    capacidad: Optional[int] = Field(None, gt=0)
    ubicacion: Optional[str] = Field(None, min_length=3)


class Materia(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    nombre: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = Field(None, min_length=3)
    nivel_id: Optional[int] = Field(None, gt=0)

class Paralelo(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    nombre: Optional[str] = Field(None, max_length=1)
    docente_id: Optional[int] = Field(None, gt=0)
    gestion_id: Optional[int] = Field(None, gt=0)
    materia_id: Optional[int] = Field(None, gt=0)
    cupos: Optional[int] = Field(None, gt=0)
    activo: Optional[str] = Field(None, min_length=3)

class ParaleloCompleto(BaseModel):
    docente : Optional[Docente] = None
    materia : Materia
    paralelo : Paralelo
    aula : Aula
    horario : Horario

class MateriaParalelo:
    materia : Materia
    paralelo : list[ParaleloCompleto]


