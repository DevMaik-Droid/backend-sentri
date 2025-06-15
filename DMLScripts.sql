-- Insertar semestres de la carrera Ingenieria de sistemas
INSERT INTO niveles (nombre, descripcion) 
VALUES 
    ('Primer Semestre', 'Introduccion a la Programacion, calculo I, algebra I, etc'),
    ('Segundo Semestre', 'Programacion I, calulo II, algebra II, etc'),
    ('Tercer Semestre', 'Programacion II, calculo III, Estadiscas, etc');



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