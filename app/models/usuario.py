from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UsuarioAPI(BaseModel):
    id: int | None = None 
    nombre: str = Field(..., min_length=3)
    apellido: str = Field(..., min_length=3)
    cedula: str = Field(..., min_length=3)
    email: EmailStr
    username: str = Field(..., min_length=3)
    password_hash: str = Field(..., min_length=3)
    rol: str = Field(..., min_length=3)

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    rol: Optional[str] = None

    