from ..database.conexion import Conexion
from asyncpg import Connection
from ..models.usuario import Usuario
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UsuarioService:

    @classmethod
    async def crear_usuario(cls, usuario:Usuario, conn : Connection):
        sql = "INSERT INTO usuarios (nombre, apellido,fecha_nacimiento, cedula, genero, direccion, telefono, email, password_hash, rol_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id;"
        hash_password = pwd_context.hash(usuario.password_hash)
        id = await conn.fetchval(sql, usuario.nombre, usuario.apellido, usuario.fecha_nacimiento, usuario.cedula, usuario.genero, usuario.direccion, usuario.telefono, usuario.email, hash_password, usuario.rol_id)
        return id

    @classmethod
    async def authenticate(cls, username):
        sql = "SELECT * FROM usuarios WHERE cedula = $1 OR email = $1"
        async with Conexion() as conn:
            user = await conn.fetchrow(sql, username)
            if user:
                return Usuario(**user)
            return None
    
    # @classmethod
    # def obtener_usuarios(cls):
    #     sql = "SELECT * FROM usuarios"
    #     with CursorPool() as cursor:
    #         cursor.execute(sql)
    #         usuarios = cursor.fetchall()
    #         return usuarios
        
    # @classmethod
    # def actualizar_usuario(self, usuario: Usuario):
    #     sql = "UPDATE usuarios SET nombre = %s, apellido = %s, cedula = %s, email = %s, username = %s, password_hash = %s, rol = %s WHERE id = %s;"
    #     with CursorPool() as cursor:
    #         cursor.execute(sql, (usuario.nombre, usuario.apellido, usuario.cedula, usuario.email, usuario.username, usuario.password_hash, usuario.rol, usuario.id))
    #         return cursor.rowcount

    # @classmethod
    # def eliminar_usuario(self, id):
    #     sql = "DELETE FROM usuarios WHERE id = %s"
    #     with CursorPool() as cursor:
    #         cursor.execute(sql, (id,))
    #         return cursor.rowcount

    # @classmethod
    # def obtener_usuario(cls, id):
    #     sql = "SELECT * FROM usuarios WHERE id = %s"
    #     with CursorPool() as cursor:
    #         cursor.execute(sql, (id,))
    #         usuario = cursor.fetchone()
    #         return usuario


    