from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:

    id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    rol: Optional[str] = None
    created_at: Optional[str] = None
