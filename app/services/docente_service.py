from ..models.usuario import Usuario
from ..database.conexion import CursorPool
from ..models.docente import Docente

class DocenteService:

    @classmethod
    def obtener_docente_id(cls, id):
        sql = "SELECT * FROM docentes WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            docente = cursor.fetchone()
            return docente

    @classmethod
    def buscar_por_materia(cls, materia):
        sql = "SELECT * FROM docentes WHERE materia = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (materia,))
            docente = cursor.fetchone()
            return docente

    @classmethod
    def obtener_docentes_all(cls):
        sql = """
                SELECT d.id, d.materia, u.id, u.nombre, u.apellido, u.cedula, u.email, u.username, u.password_hash, u.rol, u.created_at
                FROM docentes d
                JOIN usuarios u ON d.id_usuario = u.id;
              """
        with CursorPool() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            docentes = []

            for fila in result:
                docente = Docente(
                    id=fila[0],
                    materia=fila[1],
                    usuario=Usuario(id=fila[2], nombre=fila[3], apellido=fila[4], cedula=fila[5], email=fila[6], username=fila[7], password_hash=fila[8], rol=fila[9], created_at=fila[10])
                )
                docentes.append(docente)

            return docentes

    @classmethod
    def obtener_docentes(cls):
        sql = "SELECT * FROM docentes;"
        with CursorPool() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            docentes = []

            for fila in result:
                docente = Docente(
                    id=fila[0],
                    materia=fila[1],
                    usuario=Usuario(id=fila[2])
                )
                docentes.append(docente)

            return docentes

    @classmethod
    def crear_docente(cls, docente: Docente):
        if docente.usuario.id is not None:
            sql = "INSERT INTO docentes (materia, id_usuario) VALUES (%s, %s);"
            with CursorPool() as cursor:
                cursor.execute(sql, (docente.materia, docente.usuario.id))
                return cursor.rowcount
        else:
            return None

    @classmethod
    def actualizar_docente(cls, docente: Docente):
        sql = "UPDATE docentes SET materia = %s WHERE id_usuario = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (docente.materia, docente.id))
            return cursor.rowcount

