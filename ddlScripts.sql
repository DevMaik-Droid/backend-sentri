-- ========== DOMINIOS ==========
CREATE DOMAIN D_GENERO AS CHAR(1) CHECK (VALUE IN ('M', 'F'));
CREATE DOMAIN D_TEXT50 AS VARCHAR(50);
CREATE DOMAIN D_TEXT100 AS VARCHAR(100);
CREATE DOMAIN D_TEXT20 AS VARCHAR(20);
CREATE DOMAIN D_TEXT AS VARCHAR(255);
CREATE DOMAIN D_ACTIVO_CURSO AS VARCHAR(20) CHECK (VALUE IN ('PROXIMAMENTE', 'ACTIVO','FINALIZADO', 'CANCELADO'));
CREATE DOMAIN D_DIA_SEMANA AS VARCHAR(9) CHECK (VALUE IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'));
CREATE DOMAIN D_ESTADO_ASISTENCIA AS VARCHAR(15) CHECK (VALUE IN ('PRESENTE', 'AUSENTE', 'JUSTIFICADO', 'TARDE'));
CREATE DOMAIN D_METODO_REGISTRO AS VARCHAR(5) CHECK (VALUE IN ('QR', 'IA', 'Manual'));
CREATE DOMAIN D_ESTADO AS VARCHAR(10) CHECK (VALUE IN ('ACTIVO', 'INACTIVO','ELIMINADO'));



-- ========== ROLES ==========
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- ========== NIVELES ==========
CREATE TABLE niveles(
    id SERIAL PRIMARY KEY,
    nombre D_TEXT20 NOT NULL,
    descripcion D_TEXT
);

-- ========== USUARIOS ==========
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre D_TEXT50 NOT NULL,
    apellido D_TEXT50 NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    cedula D_TEXT20 UNIQUE NOT NULL,
    genero D_GENERO NOT NULL,
    direccion D_TEXT100,
    telefono D_TEXT20,
    email D_TEXT100 UNIQUE NOT NULL,
    password_hash D_TEXT NOT NULL,
    foto_perfil D_TEXT,
    estado D_ESTADO DEFAULT 'ACTIVO',
    rol_id INTEGER REFERENCES roles(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========== ESTUDIANTES ==========
CREATE TABLE estudiantes(
    id SERIAL PRIMARY KEY,
    codigo D_TEXT20 UNIQUE NOT NULL,
    nivel_id INTEGER REFERENCES niveles(id),
    usuario_id INTEGER UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ========== DOCENTES ==========
CREATE TABLE docentes (
    id SERIAL PRIMARY KEY,
    profesion D_TEXT50 NOT NULL,
    especialidad D_TEXT50,
    fecha_contratacion DATE NOT NULL,
    observaciones D_TEXT,
    usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ========== GESTIONES ACADEMICAS ==========
CREATE TABLE gestiones_academicas (
    id SERIAL PRIMARY KEY,
    nombre D_TEXT20 NOT NULL UNIQUE,
    tipo VARCHAR(10) CHECK (tipo IN ('Anual', 'Semestral')) DEFAULT 'Anual',
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    descripcion D_TEXT,
    CONSTRAINT chk_fechas_gestion CHECK (fecha_fin > fecha_inicio)
);

-- ========== AULAS ==========
CREATE TABLE aulas (
    id SERIAL PRIMARY KEY,
    nombre D_TEXT20 NOT NULL UNIQUE,
    descripcion D_TEXT,
    capacidad INTEGER CHECK (capacidad > 0),
    ubicacion D_TEXT100
);

-- ========== MATERIAS ==========
CREATE TABLE materias (
    id SERIAL PRIMARY KEY,
    nombre D_TEXT50 NOT NULL,
    descripcion D_TEXT,
    nivel_id INTEGER REFERENCES niveles(id)
);

-- ========== PARALELOS ==========
CREATE TABLE paralelos (
    id SERIAL PRIMARY KEY,
    nombre CHAR(1) NOT NULL, -- A, B, C, etc
    docente_id INTEGER REFERENCES docentes(id),
    gestion_id INTEGER NOT NULL REFERENCES gestiones_academicas(id),
    materia_id INTEGER NOT NULL REFERENCES materias(id),
    cupos INTEGER CHECK (cupos > 0),
    activo D_ACTIVO_CURSO DEFAULT 'PROXIMAMENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (materia_id, nombre, gestion_id)
);

-- ========== HORARIOS ==========
CREATE TABLE horarios (
    id SERIAL PRIMARY KEY,
    dia_semana D_DIA_SEMANA NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id),
    aula_id INTEGER NOT NULL REFERENCES aulas(id),
    UNIQUE (paralelo_id, dia_semana, hora_inicio, hora_fin),
    CONSTRAINT chk_horarios CHECK (hora_fin > hora_inicio)
);

-- ========== HISTORIAL_ACADEMICO (OPTIMIZADO) ==========
CREATE TABLE historial_academico (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id),
    estado D_ESTADO_ACADEMICO DEFAULT 'CURSANDO', -- 'APROBADO', 'REPROBADO', 'RETIRADO'
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nota_final DECIMAL(3,1) CHECK (nota_final BETWEEN 0 AND 100),
    observaciones TEXT,
    UNIQUE (estudiante_id, paralelo_id)
);


-- ========== INSCRIPCIONES ==========
CREATE TABLE inscripciones (
    id SERIAL PRIMARY KEY,
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id) ON DELETE CASCADE,
    fecha_inscripcion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado D_ESTADO DEFAULT 'ACTIVO',
    UNIQUE (estudiante_id, paralelo_id)
);


-- ========== ASISTENCIAS GENERALES ==========
CREATE TABLE asistencias (
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    hora TIME DEFAULT CURRENT_TIME,
    metodo_registro D_METODO_REGISTRO DEFAULT 'IA',
    estado D_ESTADO_ASISTENCIA DEFAULT 'PRESENTE',
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE (usuario_id, fecha)
);

-- ========== ASISTENCIAS POR PARALELO ==========
CREATE TABLE asistencias_paralelo (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id),
    fecha DATE DEFAULT CURRENT_DATE,
    hora TIME DEFAULT CURRENT_TIME,
    metodo_registro D_METODO_REGISTRO DEFAULT 'QR',
    estado D_ESTADO_ASISTENCIA DEFAULT 'PRESENTE',
    UNIQUE (usuario_id, paralelo_id, fecha)
);

-- ========== QR ASISTENCIA ==========
CREATE TABLE qr_asistencia (
    id SERIAL PRIMARY KEY,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id),
    codigo TEXT UNIQUE NOT NULL,           -- Token QR
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,                -- Tiempo válido del QR (ej: 10 mins)
    creado_por INTEGER REFERENCES usuarios(id), -- Docente que genera
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_horas_qr CHECK (hora_fin > hora_inicio)
);

-- ========== REGISTRO DE ROSTROS ==========
CREATE TABLE rostros (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    emmbedding FLOAT8[] NOT NULL,
    image_path TEXT NOT NULL,
    UNIQUE (usuario_id)
);

-- ========== TIPOS_EVALUACION ==========
CREATE TABLE tipos_evaluacion (
    id SERIAL PRIMARY KEY,
    nombre D_TEXT50 NOT NULL, -- 'Examen Parcial', 'Trabajo Práctico', etc.
    peso DECIMAL(3,2) CHECK (peso > 0 AND peso <= 1) -- Ponderación en la nota final
);

-- ========== CALIFICACIONES ==========
CREATE TABLE calificaciones (
    id SERIAL PRIMARY KEY,
    historial_id INTEGER NOT NULL REFERENCES historial_academico(id) ON DELETE CASCADE,
    tipo_evaluacion_id INTEGER NOT NULL REFERENCES tipos_evaluacion(id),
    nota DECIMAL(3,1) CHECK (nota BETWEEN 0 AND 100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    docente_id INTEGER NOT NULL REFERENCES docentes(id),
    comentario TEXT
);


-- ========== ACTIVIDADES ==========
CREATE TABLE actividades (
    id SERIAL PRIMARY KEY,
    paralelo_id INTEGER NOT NULL REFERENCES paralelos(id) ON DELETE CASCADE,
    docente_id INTEGER NOT NULL REFERENCES docentes(id),
    titulo D_TEXT100 NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega TIMESTAMP NOT NULL,
    tipo_actividad D_TIPO_ACTIVIDAD NOT NULL, -- 'TAREA', 'PROYECTO', 'EXPOSICION'
    archivo_adjunto TEXT -- Ruta del archivo si aplica
);

-- ========== ENTREGAS_ESTUDIANTES ==========
CREATE TABLE entregas_estudiantes (
    id SERIAL PRIMARY KEY,
    actividad_id INTEGER NOT NULL REFERENCES actividades(id) ON DELETE CASCADE,
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
    fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archivo_adjunto TEXT,
    estado D_ESTADO_ENTREGA DEFAULT 'ENTREGADO', -- 'CALIFICADO', 'PENDIENTE'
    calificacion_id INTEGER REFERENCES calificaciones(id), -- Relación opcional
    comentario_docente TEXT
);


-- ========== LOG DE ACCESOS =========
CREATE TABLE log_accesos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(45),
    navegador TEXT
);

-- ========== ÍNDICES ==========
-- Índices para usuarios
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_cedula ON usuarios(cedula);

-- Índices para docentes y estudiantes
CREATE INDEX idx_docente_usuario ON docentes(usuario_id);
CREATE INDEX idx_estudiante_usuario ON estudiantes(usuario_id);

-- Índices para asistencias
CREATE INDEX idx_asistencia_usuario_fecha ON asistencias(usuario_id, fecha);
CREATE INDEX idx_asistencia_paralelo_usuario ON asistencias_paralelo(usuario_id);
CREATE INDEX idx_asistencia_paralelo_fecha ON asistencias_paralelo(fecha);

-- Índices para paralelos e inscripciones
CREATE INDEX idx_paralelo_gestion ON paralelos(gestion_id);
CREATE INDEX idx_paralelo_materia ON paralelos(materia_id);
CREATE INDEX idx_inscripcion_paralelo ON inscripciones(paralelo_id);

-- Índices para horarios
CREATE INDEX idx_horario_paralelo ON horarios(paralelo_id);
CREATE INDEX idx_horario_dia_hora ON horarios(dia_semana, hora_inicio);

-- Índices para QR asistencia
CREATE INDEX idx_qr_paralelo ON qr_asistencia(paralelo_id);
CREATE INDEX idx_qr_fecha ON qr_asistencia(fecha);