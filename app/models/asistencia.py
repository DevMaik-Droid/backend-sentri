
from dataclasses import dataclass
from typing import Optional

from datetime import datetime

@dataclass
class Asistencia:
    id: Optional[int] = None
    fecha: Optional[datetime.date] = None
    hora: Optional[datetime.time] = None
    estado: Optional[str] = None
    estudiante_id: Optional[int] = None