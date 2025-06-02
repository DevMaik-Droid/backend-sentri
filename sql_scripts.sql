-- Active: 1748552459214@@127.0.0.1@5432@db_sentri
CREATE DOMAIN TEXT100 AS VARCHAR(100);
CREATE DOMAIN TEXT255 AS VARCHAR(255);
CREATE DOMAIN D_EMAIL AS VARCHAR(150);
CREATE DOMAIN D_ROL AS VARCHAR(50)
CHECK (VALUE IN ('ADMIN', 'ESTUDIANTE', 'DOCENTE'));

CREATE DOMAIN D_ESTADO_AS AS VARCHAR(50)
CHECK (VALUE IN ('PRESENTE', 'AUSENTE', 'RETRASO'));

CREATE TABLE usuarios(
    id SERIAL PRIMARY KEY,
    nombre TEXT100 NOT NULL,
    apellido TEXT100 NOT NULL,
    cedula TEXT100 UNIQUE NOT NULL,
    email D_EMAIL NOT NULL,
    username TEXT100 UNIQUE NOT NULL,
    password_hash TEXT255 NOT NULL,
    rol D_ROL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_usuarios_cedula ON usuarios(cedula);

CREATE TABLE estudiantes(
    id SERIAL PRIMARY KEY,
    matricula TEXT100 UNIQUE NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE
);
CREATE INDEX idx_estudiantes_matricula ON estudiantes(matricula);

CREATE TABLE docentes(
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    materia TEXT100 NOT NULL,
);

CREATE TABLE rostros(
    id SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL REFERENCES estudiantes(id),
    image_path TEXT255 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE asistencias(
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado D_ESTADO_AS NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registrar usuarios
INSERT INTO usuarios (nombre, apellido,cedula,email,username,password_hash,rol)
VALUES ('Miguel Angel','Quispe Gutierrez','6067355','miguel@example.com','miguel','123456','ADMIN');

INSERT INTO usuarios (nombre, apellido,cedula,email,username,password_hash,rol)
VALUES ('Betty','Salinas Tangara','10923438','betty@example.com','whetsi','123456','ESTUDIANTE');

INSERT INTO estudiantes (matricula, id_usuario) VALUES ('2025-0001', 2);

SELECT e.id, e.matricula, u.id, u.nombre, u.apellido, u.cedula, u.email, u.username, u.password_hash, u.rol
FROM estudiantes e
JOIN usuarios u ON e.usuario_id = u.id;