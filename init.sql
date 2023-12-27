CREATE DATABASE IF NOT EXISTS productos;

CREATE USER 'nico'@'localhost'IDENTIFIED BY 'naiki2353';

USE productos;

CREATE TABLE productos.lista_de_productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ean VARCHAR(13) UNIQUE NOT NULL,
    nameComplete VARCHAR(255),
    dimension VARCHAR(20),
    unidad_de_peso VARCHAR(20),
    precio FLOAT(10, 2)
);

GRANT SELECT, INSERT, DELETE, UPDATE, ALTER ON productos.lista_de_productos TO 'nico'@'localhost';
