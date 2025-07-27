import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='petshop.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Inicializa o banco de dados com todas as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Categorias de Produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Produtos/Estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria_id INTEGER,
                preco REAL NOT NULL,
                estoque_atual INTEGER DEFAULT 0,
                estoque_minimo INTEGER DEFAULT 5,
                codigo_barras TEXT UNIQUE,
                descricao TEXT,
                marca TEXT,
                peso REAL,
                unidade_medida TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        # Tabela de Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                cidade TEXT,
                cep TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Pets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cliente_id INTEGER NOT NULL,
                especie TEXT NOT NULL,
                raca TEXT,
                idade INTEGER,
                peso REAL,
                cor TEXT,
                observacoes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabela de Vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                total REAL NOT NULL,
                desconto REAL DEFAULT 0,
                forma_pagamento TEXT,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabela de Itens da Venda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        # Tabela de Tipos de Serviços
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                preco_base REAL NOT NULL,
                duracao_minutos INTEGER,
                descricao TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Agendamentos/Serviços
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                pet_id INTEGER NOT NULL,
                tipo_servico_id INTEGER NOT NULL,
                data_agendamento TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'agendado',
                preco REAL,
                observacoes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (pet_id) REFERENCES pets (id),
                FOREIGN KEY (tipo_servico_id) REFERENCES tipos_servicos (id)
            )
        ''')
        
        # Tabela de Movimentações de Estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo_movimentacao TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                motivo TEXT,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Inserir dados iniciais
        self.insert_initial_data()
    
    def insert_initial_data(self):
        """Insere dados iniciais no banco"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Categorias iniciais
        categorias_iniciais = [
            ('Ração e Alimentos', 'Rações, petiscos e alimentos para pets'),
            ('Medicamentos', 'Medicamentos e produtos veterinários'),
            ('Acessórios', 'Coleiras, guias, brinquedos e acessórios'),
            ('Higiene', 'Produtos de higiene e limpeza'),
            ('Camas e Casinhas', 'Camas, casinhas e produtos para descanso')
        ]
        
        for nome, descricao in categorias_iniciais:
            cursor.execute('''
                INSERT OR IGNORE INTO categorias (nome, descricao) 
                VALUES (?, ?)
            ''', (nome, descricao))
        
        # Tipos de serviços iniciais
        servicos_iniciais = [
            ('Banho Simples', 25.00, 60, 'Banho básico com shampoo neutro'),
            ('Banho e Tosa', 45.00, 120, 'Banho completo com tosa higiênica'),
            ('Tosa Completa', 60.00, 180, 'Tosa completa com acabamento'),
            ('Consulta Veterinária', 80.00, 30, 'Consulta clínica geral'),
            ('Vacinação', 35.00, 15, 'Aplicação de vacinas'),
            ('Hospedagem (diária)', 50.00, 1440, 'Hospedagem por dia')
        ]
        
        for nome, preco, duracao, descricao in servicos_iniciais:
            cursor.execute('''
                INSERT OR IGNORE INTO tipos_servicos (nome, preco_base, duracao_minutos, descricao) 
                VALUES (?, ?, ?, ?)
            ''', (nome, preco, duracao, descricao))
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def execute_update(self, query, params=None):
        """Executa uma query de atualização e retorna o número de linhas afetadas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows_affected = cursor.rowcount
        last_row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return rows_affected, last_row_id 