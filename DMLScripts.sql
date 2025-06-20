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