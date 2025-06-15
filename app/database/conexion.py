from .database import Database

class Conexion:
    def __init__(self):
        self._conexion = None

    async def __aenter__(self):
        self._conexion = await Database.obtener_conexion()
        return self._conexion 

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # No hay commit/rollback en asyncpg a menos que uses transacciones explícitas
        await Database.devolver_conexion(self._conexion)
