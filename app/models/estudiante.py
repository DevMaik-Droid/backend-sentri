from .usuario import Usuario
from dataclasses import dataclass
from typing import Optional

@dataclass
class Estudiante:

    id: Optional[int] = None
    matricula: Optional[str] = None
    usuario: Optional[Usuario] = None
    
