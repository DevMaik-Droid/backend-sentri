-- Insertar semestres de la carrera Ingenieria de sistemas
INSERT INTO niveles (nombre, descripcion) 
VALUES 
    ('Primer Semestre', 'Se lleva una introduccion a las materias basicas'),
    ('Segundo Semestre', 'Se busca desarrollar las habilidades basicas de programacion'),
    ('Tercer Semestre', 'Los estudiantes tienen que tener los conocimientos intermedios de programacion');



ALTER TABLE materias ADD COLUMN nivel_id INTEGER REFERENCES niveles(id);

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

ALTER TABLE cursos DROP COLUMN nivel_id;

SELECT *
FROM estudiantes e 
INNER JOIN usuarios u ON e.usuario_id = u.id;