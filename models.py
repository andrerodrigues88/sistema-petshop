from database import DatabaseManager
from datetime import datetime, timedelta
import re

class Produto:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def adicionar(self, nome, categoria_id, preco, estoque_atual=0, estoque_minimo=5, 
                  codigo_barras=None, descricao=None, marca=None, peso=None, unidade_medida=None):
        """Adiciona um novo produto ao estoque"""
        query = '''
            INSERT INTO produtos (nome, categoria_id, preco, estoque_atual, estoque_minimo, 
                                codigo_barras, descricao, marca, peso, unidade_medida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        _, produto_id = self.db.execute_update(query, (nome, categoria_id, preco, estoque_atual, 
                                                      estoque_minimo, codigo_barras, descricao, 
                                                      marca, peso, unidade_medida))
        
        # Registrar movimentação de estoque se houver estoque inicial
        if estoque_atual > 0:
            self.registrar_movimentacao(produto_id, 'entrada', estoque_atual, 'Estoque inicial')
        
        return produto_id
    
    def listar_todos(self):
        """Lista todos os produtos com informações da categoria"""
        query = '''
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            ORDER BY p.nome
        '''
        return self.db.execute_query(query)
    
    def buscar_por_id(self, produto_id):
        """Busca um produto por ID"""
        query = '''
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            WHERE p.id = ?
        '''
        resultado = self.db.execute_query(query, (produto_id,))
        return resultado[0] if resultado else None
    
    def buscar_por_nome(self, nome):
        """Busca produtos por nome (busca parcial)"""
        query = '''
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            WHERE p.nome LIKE ?
            ORDER BY p.nome
        '''
        return self.db.execute_query(query, (f'%{nome}%',))
    
    def atualizar_estoque(self, produto_id, nova_quantidade, motivo='Ajuste manual'):
        """Atualiza o estoque de um produto"""
        # Buscar estoque atual
        produto = self.buscar_por_id(produto_id)
        if not produto:
            return False
        
        estoque_atual = produto[4]  # estoque_atual está na posição 4
        diferenca = nova_quantidade - estoque_atual
        
        # Atualizar estoque
        query = 'UPDATE produtos SET estoque_atual = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
        rows_affected, _ = self.db.execute_update(query, (nova_quantidade, produto_id))
        
        # Registrar movimentação
        if diferenca != 0:
            tipo_mov = 'entrada' if diferenca > 0 else 'saida'
            self.registrar_movimentacao(produto_id, tipo_mov, abs(diferenca), motivo)
        
        return rows_affected > 0
    
    def registrar_movimentacao(self, produto_id, tipo, quantidade, motivo):
        """Registra uma movimentação de estoque"""
        query = '''
            INSERT INTO movimentacoes_estoque (produto_id, tipo_movimentacao, quantidade, motivo)
            VALUES (?, ?, ?, ?)
        '''
        return self.db.execute_update(query, (produto_id, tipo, quantidade, motivo))
    
    def produtos_estoque_baixo(self):
        """Lista produtos com estoque abaixo do mínimo"""
        query = '''
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            WHERE p.estoque_atual <= p.estoque_minimo
            ORDER BY p.estoque_atual
        '''
        return self.db.execute_query(query)
    
    def excluir(self, produto_id):
        """Exclui um produto"""
        query = 'DELETE FROM produtos WHERE id = ?'
        rows_affected, _ = self.db.execute_update(query, (produto_id,))
        return rows_affected > 0

class Cliente:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def adicionar(self, nome, cpf=None, telefone=None, email=None, endereco=None, cidade=None, cep=None):
        """Adiciona um novo cliente"""
        query = '''
            INSERT INTO clientes (nome, cpf, telefone, email, endereco, cidade, cep)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        _, cliente_id = self.db.execute_update(query, (nome, cpf, telefone, email, endereco, cidade, cep))
        return cliente_id
    
    def listar_todos(self):
        """Lista todos os clientes"""
        query = 'SELECT * FROM clientes ORDER BY nome'
        return self.db.execute_query(query)
    
    def buscar_por_id(self, cliente_id):
        """Busca um cliente por ID"""
        query = 'SELECT * FROM clientes WHERE id = ?'
        resultado = self.db.execute_query(query, (cliente_id,))
        return resultado[0] if resultado else None
    
    def buscar_por_nome(self, nome):
        """Busca clientes por nome"""
        query = 'SELECT * FROM clientes WHERE nome LIKE ? ORDER BY nome'
        return self.db.execute_query(query, (f'%{nome}%',))
    
    def buscar_por_cpf(self, cpf):
        """Busca cliente por CPF"""
        query = 'SELECT * FROM clientes WHERE cpf = ?'
        resultado = self.db.execute_query(query, (cpf,))
        return resultado[0] if resultado else None
    
    def atualizar(self, cliente_id, nome, cpf=None, telefone=None, email=None, endereco=None, cidade=None, cep=None):
        """Atualiza dados de um cliente"""
        query = '''
            UPDATE clientes 
            SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ?, cidade = ?, cep = ?
            WHERE id = ?
        '''
        rows_affected, _ = self.db.execute_update(query, (nome, cpf, telefone, email, endereco, cidade, cep, cliente_id))
        return rows_affected > 0
    
    def excluir(self, cliente_id):
        """Exclui um cliente"""
        query = 'DELETE FROM clientes WHERE id = ?'
        rows_affected, _ = self.db.execute_update(query, (cliente_id,))
        return rows_affected > 0

class Pet:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def adicionar(self, nome, cliente_id, especie, raca=None, idade=None, peso=None, cor=None, observacoes=None):
        """Adiciona um novo pet"""
        query = '''
            INSERT INTO pets (nome, cliente_id, especie, raca, idade, peso, cor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        _, pet_id = self.db.execute_update(query, (nome, cliente_id, especie, raca, idade, peso, cor, observacoes))
        return pet_id
    
    def listar_todos(self):
        """Lista todos os pets com informações do cliente"""
        query = '''
            SELECT p.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM pets p
            JOIN clientes c ON p.cliente_id = c.id
            ORDER BY p.nome
        '''
        return self.db.execute_query(query)
    
    def listar_por_cliente(self, cliente_id):
        """Lista pets de um cliente específico"""
        query = 'SELECT * FROM pets WHERE cliente_id = ? ORDER BY nome'
        return self.db.execute_query(query, (cliente_id,))
    
    def buscar_por_id(self, pet_id):
        """Busca um pet por ID"""
        query = '''
            SELECT p.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM pets p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.id = ?
        '''
        resultado = self.db.execute_query(query, (pet_id,))
        return resultado[0] if resultado else None
    
    def buscar_por_nome(self, nome):
        """Busca pets por nome"""
        query = '''
            SELECT p.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM pets p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.nome LIKE ?
            ORDER BY p.nome
        '''
        return self.db.execute_query(query, (f'%{nome}%',))
    
    def atualizar(self, pet_id, nome, especie, raca=None, idade=None, peso=None, cor=None, observacoes=None):
        """Atualiza dados de um pet"""
        query = '''
            UPDATE pets 
            SET nome = ?, especie = ?, raca = ?, idade = ?, peso = ?, cor = ?, observacoes = ?
            WHERE id = ?
        '''
        rows_affected, _ = self.db.execute_update(query, (nome, especie, raca, idade, peso, cor, observacoes, pet_id))
        return rows_affected > 0
    
    def excluir(self, pet_id):
        """Exclui um pet"""
        query = 'DELETE FROM pets WHERE id = ?'
        rows_affected, _ = self.db.execute_update(query, (pet_id,))
        return rows_affected > 0

class Venda:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def criar_venda(self, cliente_id=None, desconto=0, forma_pagamento='Dinheiro', observacoes=None):
        """Cria uma nova venda"""
        query = '''
            INSERT INTO vendas (cliente_id, total, desconto, forma_pagamento, observacoes)
            VALUES (?, ?, ?, ?, ?)
        '''
        _, venda_id = self.db.execute_update(query, (cliente_id, 0, desconto, forma_pagamento, observacoes))
        return venda_id
    
    def adicionar_item(self, venda_id, produto_id, quantidade, preco_unitario=None):
        """Adiciona um item à venda"""
        # Se não foi informado preço unitário, usar o preço atual do produto
        if preco_unitario is None:
            produto_query = 'SELECT preco FROM produtos WHERE id = ?'
            resultado = self.db.execute_query(produto_query, (produto_id,))
            if not resultado:
                return False
            preco_unitario = resultado[0][0]
        
        subtotal = quantidade * preco_unitario
        
        # Adicionar item
        query = '''
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        '''
        rows_affected, _ = self.db.execute_update(query, (venda_id, produto_id, quantidade, preco_unitario, subtotal))
        
        # Atualizar total da venda
        self.atualizar_total_venda(venda_id)
        
        return rows_affected > 0
    
    def atualizar_total_venda(self, venda_id):
        """Atualiza o total de uma venda baseado nos itens"""
        query = '''
            UPDATE vendas 
            SET total = (
                SELECT COALESCE(SUM(subtotal), 0) - desconto
                FROM itens_venda 
                WHERE venda_id = ?
            )
            WHERE id = ?
        '''
        return self.db.execute_update(query, (venda_id, venda_id))
    
    def finalizar_venda(self, venda_id):
        """Finaliza a venda e atualiza o estoque"""
        # Buscar itens da venda
        query = '''
            SELECT produto_id, quantidade 
            FROM itens_venda 
            WHERE venda_id = ?
        '''
        itens = self.db.execute_query(query, (venda_id,))
        
        produto_manager = Produto(self.db)
        
        # Reduzir estoque para cada item
        for produto_id, quantidade in itens:
            produto = produto_manager.buscar_por_id(produto_id)
            if produto:
                novo_estoque = produto[4] - quantidade  # estoque_atual está na posição 4
                produto_manager.atualizar_estoque(produto_id, novo_estoque, f'Venda #{venda_id}')
        
        return True
    
    def listar_vendas(self, limite=50):
        """Lista as vendas mais recentes"""
        query = '''
            SELECT v.*, c.nome as cliente_nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.data_venda DESC
            LIMIT ?
        '''
        return self.db.execute_query(query, (limite,))
    
    def buscar_venda(self, venda_id):
        """Busca uma venda específica com seus itens"""
        # Buscar venda
        query = '''
            SELECT v.*, c.nome as cliente_nome, c.telefone as cliente_telefone
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        '''
        venda = self.db.execute_query(query, (venda_id,))
        if not venda:
            return None
        
        # Buscar itens da venda
        query_itens = '''
            SELECT iv.*, p.nome as produto_nome
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        '''
        itens = self.db.execute_query(query_itens, (venda_id,))
        
        return {
            'venda': venda[0],
            'itens': itens
        }

class Agendamento:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def criar_agendamento(self, cliente_id, pet_id, tipo_servico_id, data_agendamento, observacoes=None):
        """Cria um novo agendamento"""
        # Buscar preço do serviço
        query_preco = 'SELECT preco_base FROM tipos_servicos WHERE id = ?'
        resultado = self.db.execute_query(query_preco, (tipo_servico_id,))
        preco = resultado[0][0] if resultado else 0
        
        query = '''
            INSERT INTO agendamentos (cliente_id, pet_id, tipo_servico_id, data_agendamento, preco, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        _, agendamento_id = self.db.execute_update(query, (cliente_id, pet_id, tipo_servico_id, data_agendamento, preco, observacoes))
        return agendamento_id
    
    def listar_agendamentos(self, data_inicio=None, data_fim=None):
        """Lista agendamentos por período"""
        if data_inicio and data_fim:
            query = '''
                SELECT a.*, c.nome as cliente_nome, p.nome as pet_nome, ts.nome as servico_nome
                FROM agendamentos a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN pets p ON a.pet_id = p.id
                JOIN tipos_servicos ts ON a.tipo_servico_id = ts.id
                WHERE DATE(a.data_agendamento) BETWEEN ? AND ?
                ORDER BY a.data_agendamento
            '''
            return self.db.execute_query(query, (data_inicio, data_fim))
        else:
            query = '''
                SELECT a.*, c.nome as cliente_nome, p.nome as pet_nome, ts.nome as servico_nome
                FROM agendamentos a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN pets p ON a.pet_id = p.id
                JOIN tipos_servicos ts ON a.tipo_servico_id = ts.id
                ORDER BY a.data_agendamento
            '''
            return self.db.execute_query(query)
    
    def atualizar_status(self, agendamento_id, novo_status):
        """Atualiza o status de um agendamento"""
        query = 'UPDATE agendamentos SET status = ? WHERE id = ?'
        rows_affected, _ = self.db.execute_update(query, (novo_status, agendamento_id))
        return rows_affected > 0
    
    def listar_tipos_servicos(self):
        """Lista todos os tipos de serviços disponíveis"""
        query = 'SELECT * FROM tipos_servicos ORDER BY nome'
        return self.db.execute_query(query)

class Categoria:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def listar_todas(self):
        """Lista todas as categorias"""
        query = 'SELECT * FROM categorias ORDER BY nome'
        return self.db.execute_query(query)
    
    def adicionar(self, nome, descricao=None):
        """Adiciona uma nova categoria"""
        query = 'INSERT INTO categorias (nome, descricao) VALUES (?, ?)'
        _, categoria_id = self.db.execute_update(query, (nome, descricao))
        return categoria_id 