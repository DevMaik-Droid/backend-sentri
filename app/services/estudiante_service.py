
from datetime import datetime
from ..models.usuario import Usuario
from ..models.estudiante import Estudiante, EstudianteCreate, Inscripcion, Niveles
from ..database.conexion import Conexion
from ..services.usuario_service import UsuarioService
from ..models.general import Aula, Horario, Materia, Paralelo, ParaleloCompleto
from ..models.docente import Docente
from ..utils.utils import limpiar_nulls
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
    async def obtener_estudiante_by_usuario(cls, id):
        sql = "SELECT * FROM estudiantes WHERE usuario_id = $1;"
        async with Conexion() as conn:
            fila = await conn.fetchrow(sql, id)
            if fila:
                return Estudiante(
                    id=fila["id"],
                    codigo=fila["codigo"],
                    nivel_id=fila["nivel_id"],
                    usuario_id=fila["usuario_id"]
                )
            return None


    @classmethod
    async def obtener_estudiante(cls, id) -> EstudianteCreate | None:
        sql = """
        SELECT e.id, e.codigo, e.nivel_id,e.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email,n.nombre as nivel, u.foto_perfil, u.fecha_creacion 
        FROM estudiantes e
        INNER JOIN usuarios u ON u.id = e.usuario_id
        INNER JOIN niveles n ON n.id = e.nivel_id
        WHERE e.id = $1;
                """
        async with Conexion() as conn:
            fila = await conn.fetchrow(sql, id)
            if fila:
                estudiante = Estudiante(
                    id=fila["id"],
                    codigo=fila["codigo"],
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
                nivel = Niveles(
                    nombre=fila["nivel"]
                )
                return EstudianteCreate(estudiante=estudiante, usuario=usuario, niveles=nivel)
            
            return None
     
    
    @classmethod
    async def obtener_estudiantes_all(cls):
        sql = """
        SELECT e.id, e.codigo, e.nivel_id, e.usuario_id, n.nombre as nivel, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil,u.estado, u.fecha_creacion 
        FROM estudiantes e
        INNER JOIN usuarios u ON u.id = e.usuario_id
        INNER JOIN niveles n ON n.id = e.nivel_id;
        """
        lista_estudiantes: list[EstudianteCreate] = []

        async with Conexion() as conn:
            res = await conn.fetch(sql)
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
                    fecha_nacimiento=fila["fecha_nacimiento"],
                    cedula=fila["cedula"],
                    genero=fila["genero"],
                    direccion=fila["direccion"],
                    telefono=fila["telefono"],
                    email=fila["email"],
                    estado=fila["estado"],
                    foto_perfil=fila["foto_perfil"],
                    fecha_creacion=fila["fecha_creacion"]
                )
                nivel = Niveles(
                    nombre=fila["nivel"]
                )
                lista_estudiantes.append(EstudianteCreate(estudiante=estudiante, usuario=usuario, niveles=nivel))
        return lista_estudiantes

    @classmethod
    async def inscribir_estudiante(cls, inscripcion:Inscripcion):
        sql = "INSERT INTO inscripciones (estudiante_id, paralelo_id) VALUES ($1, $2);"
        async with Conexion() as conn:
            async with conn.transaction():
                await conn.execute(sql, inscripcion.estudiante_id, inscripcion.paralelo_id)
                return True
        return False
            
            
    @classmethod
    async def obtener_materias_estudiante(cls, estudiante_id):
        sql = """
            SELECT 
            u.nombre as docente_nombre,
            u.apellido as docente_apellido,
            m.id AS materia_id,
            m.nombre AS materia_nombre,
            m.descripcion,
            p.id AS paralelo_id,
            p.nombre AS paralelo_nombre,
            p.cupos,
            p.activo,
            h.dia_semana,
            h.hora_inicio,
            h.hora_fin,
            a.nombre AS aula
            FROM materias m
            JOIN paralelos p ON p.materia_id = m.id
            JOIN horarios h ON h.paralelo_id = p.id
            JOIN aulas a ON a.id = h.aula_id
            LEFT JOIN usuarios u ON u.id = p.docente_id
            LEFT JOIN inscripciones i ON i.paralelo_id = p.id AND i.estudiante_id = $1
            WHERE m.nivel_id = (
                SELECT nivel_id FROM estudiantes WHERE id = $1
            )
            AND i.id IS NULL
            ORDER BY m.nombre, p.nombre, h.dia_semana, h.hora_inicio;
            """
        paralelos : list[ParaleloCompleto]= []
        async with Conexion() as conn:
            filas = await conn.fetch(sql, estudiante_id)
            for fila in filas:
                docente = Docente(
                    nombre=fila["docente_nombre"],
                    apellido=fila["docente_apellido"]
                )
                materia = Materia(
                    id=fila["materia_id"],
                    nombre=fila["materia_nombre"],
                    descripcion=fila["descripcion"]
                )
                paralelo = Paralelo(
                    id=fila["paralelo_id"],
                    nombre=fila["paralelo_nombre"],
                    cupos=fila["cupos"],
                    activo=fila["activo"]
                )
                horario = Horario(
                    dia_semana=fila["dia_semana"],
                    hora_inicio=fila["hora_inicio"],
                    hora_fin=fila["hora_fin"]
                )
                aula = Aula(
                    nombre=fila["aula"]
                )
                paralelos.append(ParaleloCompleto(materia=materia, paralelo=paralelo, horario=horario, aula=aula, docente=docente))
        
        return limpiar_nulls(paralelos)

