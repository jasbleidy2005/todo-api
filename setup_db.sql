# Script para crear la base de datos PostgreSQL

-- Crear la base de datos
CREATE DATABASE tasks_management_db;

-- Conectarse a la base de datos
\c tasks_management_db;

-- Mensaje de confirmación
SELECT 'Base de datos tasks_management_db creada exitosamente' AS mensaje;
