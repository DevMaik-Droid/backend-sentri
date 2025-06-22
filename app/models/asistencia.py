
from typing import Optional
from pydantic import Field, BaseModel
from datetime import date, time

class Asistencia(BaseModel):

    id: Optional[int] = Field(None, gt=0)
    fecha: Optional[date] = None
    hora: Optional[time] = None
    metodo_registro: Optional[str] = Field(None, min_length=3)
    estado: Optional[str] = Field(None, min_length=3)
    usuario_id: int = Field(..., gt=0)