from ..models.usuario import Usuario
from ..database.conexion import Conexion
from ..models.docente import DocenteData
from ..services.usuario_service import UsuarioService

class DocenteService:

    @classmethod
    async def crear_docente(cls, data:DocenteData):
        sql = "INSERT INTO docentes (profesion, especialidad, fecha_contratacion, observaciones, usuario_id) VALUES ($1, $2, $3, $4, $5);"
        async with Conexion() as conn:
            async with conn.transaction():
                #Registrando usuario
                usuario_id = await UsuarioService.crear_usuario(data.usuario, conn)
                await conn.execute(sql, data.docente.profesion, data.docente.especialidad, data.docente.fecha_contratacion, data.docente.observaciones, usuario_id)
                return True
            
        return False

    @classmethod
    async def obtener_docente(cls, id):
        sql = """
        SELECT d.id, d.profesion, d.especialidad, d.fecha_contratacion, d.observaciones,d.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion 
        FROM docentes d
        INNER JOIN usuarios u ON u.id = d.usuario_id
        WHERE d.id = $1;
                """
        async with Conexion() as conn:
            fila = await conn.fetchrow(sql, id)
            if fila:
                docente = DocenteData(
                    id=fila["id"],
                    profesion=fila["profesion"],
                    especialidad=fila["especialidad"],
                    fecha_contratacion=fila["fecha_contratacion"],
                    observaciones=fila["observaciones"],
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
                return DocenteData(docente=docente, usuario=usuario)


    @classmethod
    async def obtener_docentes_all(cls):
        sql = """
        SELECT d.id, d.profesion, d.especialidad, d.fecha_contratacion, d.observaciones,d.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion 
        FROM docentes d
        INNER JOIN usuarios u ON u.id = d.usuario_id;
        """
        lista_docentes: list[DocenteData] = []

        async with Conexion() as conn:
            res = await conn.fetch(sql)
            print("resilta", res)
            for fila in res:
                docente = DocenteData(
                    id=fila["id"],
                    profesion=fila["profesion"],
                    especialidad=fila["especialidad"],
                    fecha_contratacion=fila["fecha_contratacion"],
                    observaciones=fila["observaciones"],
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
                lista_docentes.append(DocenteData(docente=docente, usuario=usuario))
            return lista_docentes

    @classmethod
    async def actualizar_docente(cls, data:DocenteData):
        sql = """UPDATE docentes SET profesion = $1, especialidad = $2, fecha_contratacion = $3, observaciones = $4 
                WHERE id = $5;"""
        async with Conexion() as conn:
            async with conn.transaction():
                #Actualizando usuario
                data.usuario.id = data.docente.usuario_id
                await UsuarioService.actualizar_usuario_(data.usuario, conn)

                await conn.execute(sql, data.docente.profesion, data.docente.especialidad, data.docente.fecha_contratacion, data.docente.observaciones, data.docente.id)
                return True
        
        return False
