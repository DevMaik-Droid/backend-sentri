from ..database.conexion import Conexion
from ..models.usuario import Rostro
class FaceService:


    @classmethod
    async def registrar_rostro(cls, request:Rostro):
        sql = "INSERT INTO rostros (usuario_id,emmbedding, image_path) VALUES ($1, $2, $3);"
        async with Conexion() as conn:
            await conn.execute(sql,request.usuario_id, request.emmbedding, request.image_path)
            return True


    @classmethod
    async def obtener_rostros(cls):
        sql = """
                SELECT usuario_id, emmbedding FROM rostros;
                """
        async with Conexion() as conn:
            rostros : list[Rostro] = []
            filas = await conn.fetch(sql)
            for fila in filas:
                rostro : Rostro = Rostro(
                    usuario_id=fila["usuario_id"],
                    emmbedding=fila["emmbedding"]
                )
                rostros.append(rostro)
            return rostros