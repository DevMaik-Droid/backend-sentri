from ..database.conexion import Conexion
from asyncpg import Connection
class FaceService:


    @classmethod
    async def registrar_rostro(cls, image_path, emmbedding, id_usuario, conn : Connection):
        sql = "INSERT INTO rostros (emmbedding, image_path, id_usuario) VALUES ($1, $2, $3);"
        await conn.execute(sql, emmbedding, image_path, id_usuario)


    @classmethod
    async def obtener_rostros(cls):
        sql = """
                SELECT u.id, u.nombre, u.apellido, u.rol, r.emmbedding
                FROM usuarios u
                JOIN rostros r ON u.id = r.id_usuario;
                """
        async with Conexion() as conn:
            return await conn.fetch(sql)