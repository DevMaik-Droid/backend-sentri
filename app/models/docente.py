from typing import Optional

from pydantic import BaseModel, Field
from datetime import date
from .usuario import Usuario

class Docente(BaseModel):
    id : Optional[int] = Field(None, gt=0)
    profesion : Optional[str] = Field(None, min_length=3)
    especialidad : Optional[str] = Field(None, min_length=3)
    fecha_contratacion : date = None
    observaciones : Optional[str] = Field(None, min_length=3)
    usuario_id : Optional[int] = Field(None, gt=0)

class DocenteData(BaseModel):
    docente : Docente
    usuario : Usuario