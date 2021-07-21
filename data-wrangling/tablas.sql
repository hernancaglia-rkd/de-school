#Creo una base de datos que pueda usar
CREATE DATABASE PRACTICAS3;
CREATE USER usertest@'%' IDENTIFIED BY '12345678';
GRANT ALL PRIViLEGES ON PRACTICAS3.* TO usertest@'%';
;

USE practicas3;
SELECT * FROM tabla_demo LIMIT 10;

#DROP TABLE tabla_demo;