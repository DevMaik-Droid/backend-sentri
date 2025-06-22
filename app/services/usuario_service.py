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
    async def crear_usuario_admin(cls, usuario:Usuario):
        async with Conexion() as conn:
            return await cls.crear_usuario(usuario, conn)

    @classmethod
    async def authenticate(cls, username):

        if '@' in username:
            tipo_autenticacion = "u.email = $1"
        else:
            tipo_autenticacion = "u.cedula = $1"

        sql = f"""
            SELECT u.id, u.nombre, u.apellido, u.email, u.password_hash, u.foto_perfil, upper(r.nombre) AS rol FROM 
            usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE {tipo_autenticacion};
            """
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




    