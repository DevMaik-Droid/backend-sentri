import os
from urllib.parse import urlparse
import asyncpg
from dotenv import load_dotenv

class Database:
    _pool = None

    @classmethod
    async def inicializar_pool(cls):
        try:
            if cls._pool is None:
                load_dotenv()

            _URL_DATABASE = os.getenv("URL_DATABASE")
            parsed = urlparse(_URL_DATABASE)

            cls._pool = await asyncpg.create_pool(
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:],
                host=parsed.hostname,
                port=parsed.port,
                min_size=1,
                max_size=10
            )
            print("✅ Conexión asyncpg establecida.")
        except:
            print("❌ Error al establecer la conexión asyncpg.")
        

    @classmethod
    async def obtener_conexion(cls):
        if cls._pool is None:
            await cls.inicializar_pool()
        return await cls._pool.acquire()

    @classmethod
    async def devolver_conexion(cls, conexion):
        if cls._pool:
            await cls._pool.release(conexion)
    
