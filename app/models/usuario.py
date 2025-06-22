from datetime import date
from fastapi import UploadFile
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = Field(None, min_length=3)
    apellido: Optional[str] = Field(None, min_length=3)
    fecha_nacimiento: Optional[date] = None
    cedula: Optional[str] = Field(None, min_length=3)
    genero: Optional[str] = Field(None, length=1)
    direccion: Optional[str] = Field(None, min_length=3)
    telefono: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = Field(None, min_length=3)
    foto_perfil: Optional[UploadFile] | Optional[str] = None
    estado: Optional[str] = None
    rol_id: Optional[int] = Field(None, gt=0)
    rol: Optional[str] = None



class RostroUser(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    usuario_id: int = Field(..., gt=0)
    foto : UploadFile = Field(..., min_length=3)
    emmbedding: Optional[str] = Field(None, min_length=3)
    image_path: Optional[str] = None