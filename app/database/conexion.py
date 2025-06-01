
from dotenv import load_dotenv
import os
from psycopg2 import pool
from psycopg2.extras import DictConnection
from urllib.parse import urlparse
class Conexion:

    load_dotenv()
    _URL_DATA_BASE = os.getenv("URL_DATABASE")
    _DATA_BASE  = urlparse(_URL_DATA_BASE).path[1:]
    _USERNAME = urlparse(_URL_DATA_BASE).username
    _PASSWORD = urlparse(_URL_DATA_BASE).password
    _HOST = urlparse(_URL_DATA_BASE).hostname
    _PORT = urlparse(_URL_DATA_BASE).port

    _MAX = 10
    _MIN = 1
    _pool = None

    @classmethod
    def obtener_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN, cls._MAX, 
                                                      host=cls._HOST, 
                                                      user=cls._USERNAME, 
                                                      password=cls._PASSWORD, 
                                                      port=cls._PORT, 
                                                      database=cls._DATA_BASE,
                                                      connection_factory=DictConnection)
                print("Conexion exitosa")
            except Exception as e:
                print(f"Error al obtener la conexion: {str(e)}")
        return cls._pool
    
    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().getconn()
    
    @classmethod
    def devolver_conexion(cls, conexion):
        cls.obtener_pool().putconn(conexion)