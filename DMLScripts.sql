INSERT INTO roles (nombre, descripcion) VALUES 
('admin', 'Administrador del sistema'),
('docente', 'Personal docente'),
('estudiante', 'Estudiantes');

-- Insertar semestres de la carrera Ingenieria de sistemas
INSERT INTO niveles (nombre, descripcion) 
VALUES 
    ('Primer Semestre', 'Se lleva una introduccion a las materias basicas'),
    ('Segundo Semestre', 'Se busca desarrollar las habilidades basicas de programacion'),
    ('Tercer Semestre', 'Los estudiantes tienen que tener los conocimientos intermedios de programacion'),
    ('Cuarto Semestre', 'Se busca desarrollar las habilidades basicas de programacion'),
    ('Quinto Semestre', 'Los estudiantes tienen que tener los conocimientos intermedios de programacion'),
    ('Sexto Semestre', 'Se busca afianzar los conocimientos de programacion'),
    ('Septimo Semestre', 'Se busca afianzar los conocimientos de programacion'),
    ('Octavo Semestre', 'Los estudiantes tienen que tener los conocimientos avanzados de programacion'),
    ('Noveno Semestre', 'Se busca afianzar los conocimientos de programacion'),
    ('Decimo Semestre', 'Los estudiantes tienen que tener los conocimientos avanzados de programacion');

INSERT INTO materias (nombre, descripcion, nivel_id)
VALUES 
('INTRODUCCION A LA PROGRAMACION', 'Conceptos basicos de la programacion, diagramas de flujo, etc',1),
('CALCULO I', 'Derivadas, integrales, etc',1),
('ALGEBRA I', 'Matrices, sistemas de ecuaciones, etc',1),
('QUIMICA GENERAL', 'Propiedades de los elementos quimicos, reacciones quimicas, etc',1),
('FISICA I', 'Mecanica, electricidad, etc',1);


INSERT INTO aulas (nombre, descripcion, capacidad, ubicacion)
VALUES 
('LAB-TEM','Laboratorio tecnologico', 50, 'Torre A'),
('LAB-IA','Laboratorio de inteligencia artificial', 30, 'Torre A'),
('LAB-REDES', 'Laboratorio de redes', 40, 'Torre A');

INSERT INTO gestiones_academicas (nombre, tipo, fecha_inicio, fecha_fin, descripcion)
VALUES 
('2025-I', 'Semestral', '01/01/2025', '31/07/2025', 'Gestion academica 2025');






SELECT *
FROM estudiantes e 
INNER JOIN usuarios u ON e.usuario_id = u.id;

SELECT * FROM roles;

SELECT u.nombre,u.apellido, u.email, u.password_hash, u.foto_perfil, upper(r.nombre) AS rol FROM 
usuarios u
INNER JOIN roles r ON u.rol_id = r.id
WHERE u.rol_id = 3;

SELECT * FROM usuarios;

UPDATE usuarios SET rol_id = 3 WHERE id = 3;

SELECT * FROM materias;
SELECT * FROM aulas;
SELECT * FROM gestiones_academicas;

ALTER TABLE paralelos ALTER COLUMN nombre TYPE CHAR(1);

INSERT INTO paralelos (nombre, gestion_id, materia_id, cupos)
VALUES 
('A', 1, 1, 30),
('B', 1, 2, 30),
('C', 1, 3, 30),
('D', 1, 4, 30);

SELECT * FROM paralelos;
SELECT * FROM horarios;

SELECT p.id, p.nombre AS paralelo,p.cupos, m.nombre AS materia, m.nivel_id
FROM paralelos p
INNER JOIN materias m ON m.id = p.materia_id;


SELECT u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion from usuarios u;

SELECT * FROM estudiantes;

SELECT e.id, e.codigo, e.nivel_id,e.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email,n.nombre as nivel, u.foto_perfil, u.fecha_creacion 
        FROM estudiantes e
        INNER JOIN usuarios u ON u.id = e.usuario_id
        INNER JOIN niveles n ON n.id = u.rol_id;
    
SELECT * FROM paralelos;

SELECT * FROM materias;

SELECT d.id, d.profesion, d.especialidad, d.fecha_contratacion, d.observaciones,d.usuario_id, u.nombre, u.apellido,u.fecha_nacimiento, u.cedula, u.genero, u.direccion, u.telefono, u.email, u.foto_perfil, u.fecha_creacion 
        FROM docentes d
        INNER JOIN usuarios u ON u.id = d.usuario_id;

SELECT DISTINCT m.id, m.nombre, m.descripcion
        FROM materias m
        JOIN paralelos p ON p.materia_id = m.id
        LEFT JOIN inscripciones i ON i.paralelo_id = p.id AND i.estudiante_id = 6
        WHERE m.nivel_id = (
            SELECT nivel_id FROM estudiantes WHERE id = 6
        ) AND i.id IS NULL;

SELECT 
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
LEFT JOIN inscripciones i ON i.paralelo_id = p.id AND i.estudiante_id = $1
WHERE m.nivel_id = (
    SELECT nivel_id FROM estudiantes WHERE id = $1
)
AND i.id IS NULL
ORDER BY m.nombre, p.nombre, h.dia_semana, h.hora_inicio;
