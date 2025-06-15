
from pydantic import Field, BaseModel
from datetime import datetime

class Asistencia(BaseModel):

    id: int = Field(..., gt=0)
    fecha: datetime.date = Field(..., min_length=3)
    hora: datetime.time = Field(..., min_length=3)
    estado: str = Field(..., min_length=3)
    estudiante_id: int = Field(..., min_length=3)