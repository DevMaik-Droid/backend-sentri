from ..database.conexion import Conexion
from ..models.asistencia import Asistencia

class AsistenciaService:
    
    @classmethod
    async def registrar_asistencia(cls, usuario_id):
        sql = "INSERT INTO asistencias (usuario_id) VALUES ($1, $2, $3);"
        async with Conexion() as conn:
            await conn.execute(sql, (usuario_id))
            return True

        return False