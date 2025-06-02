
from ..database.cursor_pool import CursorPool
from ..models.usuario import Usuario
class UsuarioService:

    @classmethod
    def crear_usuario(cls, usuario:Usuario):
        sql = "INSERT INTO usuarios (nombre, apellido, cedula, email, username, password_hash, rol) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
        with CursorPool() as cursor:
            cursor.execute(sql, (usuario.nombre, usuario.apellido, usuario.cedula, usuario.email, usuario.username, usuario.password_hash, usuario.rol))
            id = cursor.fetchone()[0]
            return id
    
    @classmethod
    def obtener_usuarios(cls):
        sql = "SELECT * FROM usuarios"
        with CursorPool() as cursor:
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return usuarios
        
    @classmethod
    def actualizar_usuario(self, usuario: Usuario):
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, cedula = %s, email = %s, username = %s, password_hash = %s, rol = %s WHERE id = %s;"
        with CursorPool() as cursor:
            cursor.execute(sql, (usuario.nombre, usuario.apellido, usuario.cedula, usuario.email, usuario.username, usuario.password_hash, usuario.rol, usuario.id))
            return cursor.rowcount

    @classmethod
    def eliminar_usuario(self, id):
        sql = "DELETE FROM usuarios WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            return cursor.rowcount

    @classmethod
    def obtener_usuario(cls, id):
        sql = "SELECT * FROM usuarios WHERE id = %s"
        with CursorPool() as cursor:
            cursor.execute(sql, (id,))
            usuario = cursor.fetchone()
            return usuario