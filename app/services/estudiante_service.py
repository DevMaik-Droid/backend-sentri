
from ..models.usuario import Usuario
from ..database.cursor_pool import CursorPool
from ..models.estudiante import Estudiante
class EstudianteService:
    
    @classmethod
    def obtener_estudiante_id(cls, id):
        sql = "SELECT * FROM estudiantes WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            estudiante = cursor.fetchone()
            return estudiante
    
    @classmethod
    def buscar_por_matricula(cls, matricula):
        sql = "SELECT * FROM estudiantes WHERE matricula = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (matricula,))
            estudiante = cursor.fetchone()
            return estudiante
    
    @classmethod
    def obtener_estudiantes_all(cls):
        sql = """
                SELECT e.id, e.matricula, u.id, u.nombre, u.apellido, u.cedula, u.email, u.username, u.password_hash, u.rol, u.created_at
                FROM estudiantes e
                JOIN usuarios u ON e.usuario_id = u.id;
            """
        with CursorPool() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            estudiantes = []

            for fila in result:
                estudiante= Estudiante(
                    id=fila[0],
                    matricula=fila[1],
                    usuario=Usuario(id=fila[2],nombre=fila[3],apellido=fila[4],cedula=fila[5],email=fila[6],username=fila[7],password_hash=fila[8],rol=fila[9], created_at=fila[10])
                )
                estudiantes.append(estudiante)

            return estudiantes

    @classmethod
    def obtener_estudiantes(cls):
        sql = "SELECT * FROM estudiantes;"
        with CursorPool() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            estudiantes = []

            for fila in result:
                estudiante= Estudiante(
                    id=fila[0],
                    matricula=fila[1],
                    usuario=Usuario(id=fila[2])
                )
                estudiantes.append(estudiante)

            return estudiantes
    @classmethod
    def crear_estudiante(cls, estudiante:Estudiante):

        if estudiante.usuario.id is not None:
            sql = "INSERT INTO estudiantes (matricula, usuario_id) VALUES (%s, %s);"
            with CursorPool() as cursor:
                cursor.execute(sql, (estudiante.matricula, estudiante.usuario.id))
                return cursor.rowcount
        else:
            return None
        
    @classmethod
    def actualizar_estudiante(cls, estudiante: Estudiante):
        
        sql = "UPDATE estudiantes SET matricula = %s WHERE usuario_id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (estudiante.matricula, estudiante.id))
            return cursor.rowcount
    
