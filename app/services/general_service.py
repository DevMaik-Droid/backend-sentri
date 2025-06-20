from datetime import time
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
    async def obtener_paralelos(cls):
        sql = """
            SELECT p.id, p.nombre AS paralelo, m.nombre AS materia, m.nivel_id
            FROM paralelos p
            INNER JOIN materias m ON m.id = p.materia_id;
        """
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
    
    @classmethod
    async def crear_horario(cls, horarios : list):
        try:
            sql = "INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, paralelo_id, aula_id) VALUES ($1, $2, $3, $4, $5);"
            async with Conexion() as conn:
                for horario in horarios:
                    for dia in horario.get('dias_semana'):
                        # Convertir strings a objetos time
                        hora_inicio = time.fromisoformat(horario.get('hora_inicio'))
                        hora_fin = time.fromisoformat(horario.get('hora_fin'))

                        await conn.execute(sql, dia, hora_inicio, hora_fin, horario.get('paralelo_id'), horario.get('aula_id'))
                return True, None
        except Exception as e:
            if 'duplicate key value violates unique constraint' in str(e):
                return False, "Error: Las horas o el paralelo ya fueron registradas"

