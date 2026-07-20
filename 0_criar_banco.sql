-- CRIANDO O BANCO DE DADOS
CREATE DATABASE transparencia_viagens
    WITH OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

--CONECTANDO AO BANCO DE DADOS
\c transparencia_viagens;

-- Criar schema para organização
CREATE SCHEMA projeto_viagens AUTHORIZATION postgres;

-- RAW VIAGEM
CREATE TABLE projeto_viagens.raw_viagem (
    id_viagem VARCHAR(20),
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255),
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    cpf_viajante VARCHAR(20),
    funcao VARCHAR(255)
);

-- RAW PAGAMENTO
CREATE TABLE projeto_viagens.raw_pagamento (
    id_pagamento VARCHAR(20),
    id_viagem VARCHAR(20),
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50),
    valor VARCHAR(50)
);

-- RAW PASSAGEM
CREATE TABLE projeto_viagens.raw_passagem (
    id_passagem VARCHAR(20),
    id_viagem VARCHAR(20),
    data_inicio VARCHAR(20),
    data_fim VARCHAR(20),
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(50),
    valor_passagens VARCHAR(50),
    valor_devolucao VARCHAR(50),
    valor_outros_gastos VARCHAR(50)
);

-- RAW TRECHO
CREATE TABLE projeto_viagens.raw_trecho (
    id_trecho VARCHAR(20),
    id_viagem VARCHAR(20),
    sequencia_trecho VARCHAR(20),
    origem_data VARCHAR(20),
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data VARCHAR(20),
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias VARCHAR(50)
);

-- SILVER VIAGEM
CREATE TABLE projeto_viagens.silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY NOT NULL,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255)
);

-- SILVER PAGAMENTO
CREATE TABLE projeto_viagens.silver_pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) CHECK (valor >= 0),
    FOREIGN KEY (id_viagem) REFERENCES projeto_viagens.silver_viagem(id_viagem)
);

-- SILVER PASSAGEM
CREATE TABLE projeto_viagens.silver_passagem (
    id_passagem SERIAL PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2) CHECK (valor_diarias >= 0),
    valor_passagens DECIMAL(10,2) CHECK (valor_passagens >= 0),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,
    FOREIGN KEY (id_viagem) REFERENCES projeto_viagens.silver_viagem(id_viagem)
);

-- SILVER TRECHO
CREATE TABLE projeto_viagens.silver_trecho (
    id_trecho SERIAL PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    sequencia_trecho INT,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2) CHECK (numero_diarias >= 0),
    FOREIGN KEY (id_viagem) REFERENCES projeto_viagens.silver_viagem(id_viagem),
    CONSTRAINT unique_viagem_trecho UNIQUE (id_viagem, sequencia_trecho)
);
