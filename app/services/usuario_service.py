from ..database.conexion import Conexion
from asyncpg import Connection
from ..models.usuario import Rol, Rostro, Usuario, UsuarioCompleto
from passlib.context import CryptContext
from ..utils.utils import limpiar_nulls

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UsuarioService:

    @classmethod
    async def crear_usuario(cls, usuario:Usuario, conn : Connection):
        sql = "INSERT INTO usuarios (nombre, apellido,fecha_nacimiento, cedula, genero, direccion, telefono, email, password_hash, rol_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id;"
        hash_password = pwd_context.hash(usuario.password_hash)
        id = await conn.fetchval(sql, usuario.nombre, usuario.apellido, usuario.fecha_nacimiento, usuario.cedula, usuario.genero, usuario.direccion, usuario.telefono, usuario.email, hash_password, usuario.rol_id)
        return id
    
    @classmethod
    async def crear_usuario_admin(cls, usuario:Usuario):
        async with Conexion() as conn:
            return await cls.crear_usuario(usuario, conn)

    @classmethod
    async def authenticate(cls, username) -> UsuarioCompleto | None:

        if '@' in username:
            tipo_autenticacion = "u.email = $1"
        else:
            tipo_autenticacion = "u.cedula = $1"

        sql = f"""
            SELECT u.id, u.nombre, u.apellido, u.email, u.password_hash, u.foto_perfil, upper(r.nombre) AS rol, ro.image_path FROM 
            usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            LEFT JOIN rostros ro ON ro.usuario_id = u.id
            WHERE {tipo_autenticacion};
            """
        async with Conexion() as conn:
            user = await conn.fetchrow(sql, username)
            if user:
                usuario = Usuario(
                    id=user["id"],
                    nombre=user["nombre"],
                    apellido=user["apellido"],
                    email=user["email"],
                    password_hash=user["password_hash"],
                    foto_perfil=user["foto_perfil"]
                )
                roles = Rol(
                    nombre=user["rol"],
                )
                rostro = Rostro(
                    image_path=user["image_path"]
                )
                return UsuarioCompleto(usuario=usuario, rol=roles, rostro=rostro)

            return None

        
    @classmethod
    async def actualizar_usuario_all(self, usuario: Usuario, conn : Connection = None):
        sql = "UPDATE usuarios SET nombre = $1, apellido = $2, fecha_nacimiento = $3, cedula = $4, genero = $5, direccion = $6, telefono = $7, email = $8, password_hash = $9 WHERE id = $10;"
        if conn is not None:
            hash_password = pwd_context.hash(usuario.password_hash)
            await conn.execute(sql, usuario.nombre, usuario.apellido, usuario.fecha_nacimiento, usuario.cedula, usuario.genero, usuario.direccion, usuario.telefono, usuario.email, hash_password, usuario.id)
        else:
            async with Conexion() as conn:
                return await self.actualizar_usuario_all(usuario, conn)
            
    @classmethod
    async def obtener_usuario(cls, id):
        sql = "SELECT u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion FROM usuarios WHERE id = $1"
        async with Conexion() as conn:
            return await conn.fetchrow(sql, id)

    @classmethod
    async def eliminar_usuario(cls, id_usuario):
        sql = "DELETE FROM usuarios WHERE id = $1"
        async with Conexion() as conn:
            return await conn.execute(sql, id_usuario)




    