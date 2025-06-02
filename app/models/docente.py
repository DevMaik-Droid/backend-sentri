from dataclasses import dataclass
from typing import Optional

from .usuario import Usuario

@dataclass
class Docente:
    id: Optional[int] = None
    materia: Optional[str] = None
    usuario: Optional[Usuario] = None