from ..database.conexion import Conexion
class GeneralService:


    @classmethod
    async def obtener_niveles(cls):
        sql = "SELECT * FROM niveles;"
        async with Conexion() as conn:
            return await conn.fetch(sql)

    @classmethod
    async def obtener_materias(cls, id_usuario=None):
        sql = "SELECT * FROM materias;"
        async with Conexion() as conn:
            return await conn.fetch(sql)
        
    @classmethod
    async def obtener_aulas(cls):
        sql = "SELECT * FROM aulas;"
        async with Conexion() as conn:
            return await conn.fetch(sql)
        

    @classmethod
    async def crear_paralelos(cls, paralelos : list):
        sql = "INSERT INTO paralelos (nombre, docente_id, gestion_id, materia_id, cupos) VALUES ($1, $2, $3, $4, $5);"
        async with Conexion() as conn:
            for paralelo in paralelos:
                await conn.execute(sql, paralelo.get('nombre'), paralelo.get('docente_id'), paralelo.get('gestion_id'), paralelo.get('materia_id'), paralelo.get('cupos'))
            return True
        
        return False
    
