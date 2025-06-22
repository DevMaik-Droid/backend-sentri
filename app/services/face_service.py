from ..database.conexion import Conexion
from ..models.usuario import RostroUser
class FaceService:


    @classmethod
    async def registrar_rostro(cls, rostro : RostroUser):
        sql = "INSERT INTO rostros (usuario_id,emmbedding, image_path) VALUES ($1, $2, $3);"
        async with Conexion() as conn:
            await conn.execute(sql,rostro.usuario_id, rostro.emmbedding, rostro.image_path)


    @classmethod
    async def obtener_rostros(cls):
        sql = """
                SELECT u.id, u.nombre, u.apellido, u.rol, r.emmbedding
                FROM usuarios u
                JOIN rostros r ON u.id = r.id_usuario;
                """
        async with Conexion() as conn:
            return await conn.fetch(sql)