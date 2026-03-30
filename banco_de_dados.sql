CREATE DATABASE sistema_estoque_avancado;
USE sistema_estoque_avancado;

CREATE TABLE usuarios (
    identificador INT AUTO_INCREMENT PRIMARY KEY,
    nome_acesso VARCHAR(50) NOT NULL UNIQUE,
    senha_criptografada VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(100) NOT NULL
);

CREATE TABLE categorias (
    identificador INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(50) NOT NULL
);

CREATE TABLE produtos (
    identificador INT AUTO_INCREMENT PRIMARY KEY,
    codigo_produto VARCHAR(50) UNIQUE NOT NULL,
    nome_produto VARCHAR(150) NOT NULL,
    identificador_categoria INT,
    quantidade_atual INT DEFAULT 0,
    estoque_minimo INT DEFAULT 5,
    preco_custo DECIMAL(10, 2) NOT NULL,
    preco_venda DECIMAL(10, 2) NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (identificador_categoria) REFERENCES categorias(identificador)
);

INSERT INTO categorias (nome_categoria) VALUES ('Hardware'), ('Periféricos'), ('Licenças de Software'), ('Redes');

INSERT INTO usuarios (nome_acesso, senha_criptografada, nome_completo) 
VALUES ('admin', 'scrypt:32768:8:1$h1aH8G9Y$8b3a5c...', 'Administrador Mestre');