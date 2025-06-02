from ..database.cursor_pool import CursorPool

class FaceService:



    @classmethod
    def registrar_rostro(cls, id_estudiante, image_path, emmbedding):
        sql = "INSERT INTO rostros (emmbedding, image_path, id_estudiante) VALUES (%s, %s, %s);"
        with CursorPool() as cursor:
            cursor.execute(sql, (emmbedding, image_path, id_estudiante))
            return cursor.rowcount