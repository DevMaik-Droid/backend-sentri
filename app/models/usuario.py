from datetime import date, datetime
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
    fecha_creacion: Optional[datetime] = None

class Rol(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    nombre: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = Field(None, min_length=3)

class Rostro(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    usuario_id: Optional[int] = Field(None, gt=0)
    foto : Optional[str] = Field(None, min_length=3)
    emmbedding: Optional[list] = None
    image_path: Optional[str] = None

class UsuarioCompleto(BaseModel):
    usuario: Usuario
    rol : Optional[Rol] = None
    rostro: Optional[Rostro] = None