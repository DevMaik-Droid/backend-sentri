from ..database.conexion import CursorPool
from ..models.asistencia import Asistencia

class AsistenciaService:
    
    @classmethod
    def registrar_asistencia(cls, asistencia : Asistencia):
        sql = "INSERT INTO asistencias (fecha, hora, estado, id_estudiante) VALUES (%s,%s,%s,%s);"
        with CursorPool() as cursor:
            cursor.execute(sql, (asistencia.fecha, asistencia.hora, asistencia.estado, asistencia.estudiante_id))
            return cursor.rowcount