from ..database.conexion import Conexion
class GeneralService:


    @classmethod
    async def obtener_niveles(cls):
        sql = "SELECT * FROM niveles;"
        async with Conexion() as conn:
            return await conn.fetch(sql)

    @classmethod
    async def obtener_materias(cls, id_usuario):
        sql = "SELECT * FROM materias;"
        async with Conexion() as conn:
            return await conn.fetch(sql)
        
    @classmethod
    async def obtener_aulas(cls):
        sql = "SELECT * FROM aulas;"
        async with Conexion() as conn:
            return await conn.fetch(sql)