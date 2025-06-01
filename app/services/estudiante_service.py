
from ..database.cursor_pool import CursorPool
from ..models.estudiante import Estudiante
class EstudianteService:
    
    @classmethod
    def obtener_estudiante(cls, id):
        sql = "SELECT * FROM estudiante WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            estudiante = cursor.fetchone()
            return estudiante
        
    @classmethod
    def crear_estudiante(cls, estudiante:Estudiante):

        if estudiante.usuario.id is not None:
            sql = "INSERT INTO estudiante (matricula, usuario_id) VALUES (%s, %s)"
            with CursorPool() as cursor:
                cursor.execute(sql, (estudiante.matricula, estudiante.usuario.id))
                return cursor.rowcount
        else:
            return None
        
    @classmethod
    def actualizar_estudiante(self, estudiante: Estudiante):
        
        sql = "UPDATE usuario SET nombre = %s, apellido = %s, cedula = %s, email = %s, username = %s, password_hash = %s, rol = %s WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (estudiante.usuario.nombre, estudiante.usuario.apellido, estudiante.usuario.cedula, estudiante.usuario.email, estudiante.usuario.username, estudiante.usuario.password_hash, estudiante.usuario.rol, estudiante.usuario.id))

        sql = "UPDATE estudiante SET matricula = %s WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (estudiante.matricula, estudiante.id))
            return cursor.rowcount
        
    @classmethod
    def eliminar_estudiante(self, id):
        sql = "DELETE FROM estudiante WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            return cursor.rowcount