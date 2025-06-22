
from datetime import datetime
from ..models.usuario import Usuario
from ..models.estudiante import Estudiante, EstudianteCreate
from ..database.conexion import Conexion
from ..services.usuario_service import UsuarioService


class EstudianteService:
    

    @classmethod
    async def crear_estudiantes(cls, est : list[EstudianteCreate]):
        for estudiante in est:
            await cls.crear_estudiante(estudiante)
        return True

    @classmethod
    async def crear_estudiante(cls, est:EstudianteCreate):

        sql = "INSERT INTO estudiantes (codigo, nivel_id ,usuario_id) VALUES ($1, $2, $3);"
        async with Conexion() as conn:
            async with conn.transaction():
                #Registrando usuario
                usuario_id = await UsuarioService.crear_usuario(est.usuario, conn)
                await conn.execute(sql, est.estudiante.codigo, est.estudiante.nivel_id, usuario_id)
                return True
            
        return False
    
    @classmethod
    async def actualizar_estudiante(cls, est:EstudianteCreate):
        sql = "UPDATE estudiantes SET codigo = $1, nivel_id = $2 WHERE id = $3;"
        async with Conexion() as conn:
            async with conn.transaction():
                
                #Actualizando usuario
                est.usuario.id = est.estudiante.usuario_id
                await UsuarioService.actualizar_usuario_(est.usuario, conn)

                await conn.execute(sql, est.estudiante.codigo, est.estudiante.nivel_id, est.estudiante.id)
                
                return True
            
        return False
    
    @classmethod
    async def obtener_estudiante(cls, id) -> EstudianteCreate | None:
        sql = """
        SELECT e.id, e.codigo, e.nivel_id,e.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion 
        FROM estudiantes e
        INNER JOIN usuarios u ON u.id = e.usuario_id
        WHERE e.id = $1;
                """
        async with Conexion() as conn:
            fila = await conn.fetchrow(sql, id)
            if fila:
                estudiante = Estudiante(
                    id=fila["id"],
                    codigo=fila["codigo"],
                    nivel_id=fila["nivel_id"],
                    usuario_id=fila["usuario_id"]
                )
                usuario = Usuario(
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    fecha_nacimiento=fila["fecha_nacimiento"],
                    cedula=fila["cedula"],
                    genero=fila["genero"],
                    direccion=fila["direccion"],
                    telefono=fila["telefono"],
                    email=fila["email"],
                    foto_perfil=fila["foto_perfil"],
                    fecha_creacion=fila["fecha_creacion"]
                )
                return EstudianteCreate(estudiante=estudiante, usuario=usuario)
            
            return None
        
    @classmethod
    async def eliminar_estudiante(cls, id_usuario):
        sql = "DELETE FROM usuarios WHERE id = $1"
        async with Conexion() as conn:
            return await conn.execute(sql, id_usuario)
    
    
    @classmethod
    async def obtener_estudiantes_all(cls):
        sql = """
        SELECT e.id, e.codigo, e.nivel_id, e.usuario_id,
            u.nombre, u.apellido, u.fecha_nacimiento, u.cedula, u.genero,
            u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion 
        FROM estudiantes e
        INNER JOIN usuarios u ON u.id = e.usuario_id;
        """
        lista_estudiantes: list[EstudianteCreate] = []

        async with Conexion() as conn:
            res = await conn.fetch(sql)
            print("resilta", res)
            for fila in res:
                estudiante = Estudiante(
                    id=fila["id"],
                    codigo=fila["codigo"],
                    nivel_id=fila["nivel_id"],
                    usuario_id=fila["usuario_id"]
                )
                usuario = Usuario(
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    fecha_nacimiento=fila["fecha_nacimiento"].date() if isinstance(fila["fecha_nacimiento"], datetime) else fila["fecha_nacimiento"],
                    cedula=fila["cedula"],
                    genero=fila["genero"],
                    direccion=fila["direccion"],
                    telefono=fila["telefono"],
                    email=fila["email"],
                    foto_perfil=fila["foto_perfil"],
                    fecha_creacion=fila["fecha_creacion"]
                )
                lista_estudiantes.append(EstudianteCreate(estudiante=estudiante, usuario=usuario))
        return lista_estudiantes

            
            
            
