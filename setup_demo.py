#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para configurar dados de demonstração automaticamente
Executa quando o app é iniciado no Streamlit Cloud
"""

import os
from database import DatabaseManager
from models import Produto, Cliente, Pet, Categoria

def setup_demo_data():
    """Configura dados de demonstração se não existirem"""
    
    # Verificar se já existe dados
    db = DatabaseManager()
    
    try:
        # Verificar se já tem produtos
        produtos = db.execute_query("SELECT COUNT(*) FROM produtos")
        if produtos and produtos[0][0] > 0:
            return  # Já tem dados, não precisa criar
        
        print("🔧 Configurando dados de demonstração...")
        
        # Inicializar managers
        produto_manager = Produto(db)
        cliente_manager = Cliente(db)
        pet_manager = Pet(db)
        categoria_manager = Categoria(db)
        
        # Buscar IDs das categorias
        categorias = categoria_manager.listar_todas()
        cat_ids = {cat[1]: cat[0] for cat in categorias}
        
        # Produtos de demonstração
        produtos_demo = [
            # Rações
            ("Ração Premium Cães Adultos 15kg", cat_ids.get('Ração e Alimentos', 1), 89.90, 25, 5, "7891000001234", "Ração super premium para cães adultos", "Royal Canin", 15.0, "kg"),
            ("Ração Gatos Filhotes 3kg", cat_ids.get('Ração e Alimentos', 1), 45.50, 18, 3, "7891000001235", "Ração especial para gatos filhotes", "Whiskas", 3.0, "kg"),
            ("Petisco Natural Cães 500g", cat_ids.get('Ração e Alimentos', 1), 24.90, 30, 8, "7891000001237", "Petisco natural sem conservantes", "Bassar", 0.5, "kg"),
            
            # Medicamentos  
            ("Vermífugo Cães e Gatos", cat_ids.get('Medicamentos', 2), 35.00, 12, 3, "7891000002234", "Vermífugo de amplo espectro", "Bayer", 0.1, "un"),
            ("Antipulgas Spot On", cat_ids.get('Medicamentos', 2), 28.50, 20, 5, "7891000002235", "Antipulgas e carrapatos", "Frontline", 0.05, "un"),
            
            # Acessórios
            ("Coleira Ajustável M", cat_ids.get('Acessórios', 3), 19.90, 15, 5, "7891000003234", "Coleira de nylon ajustável", "Furacão Pet", 0.1, "un"),
            ("Brinquedo Corda", cat_ids.get('Acessórios', 3), 15.50, 25, 8, "7891000003236", "Brinquedo de corda natural", "Jambo", 0.2, "un"),
            ("Comedouro Inox Duplo", cat_ids.get('Acessórios', 3), 32.90, 12, 3, "7891000003237", "Comedouro inox duplo", "Chalesco", 0.5, "un"),
            
            # Higiene
            ("Shampoo Cães Pelos Longos", cat_ids.get('Higiene', 4), 18.90, 20, 5, "7891000004234", "Shampoo para pelos longos", "Sanol", 0.5, "un"),
            ("Escova de Dentes Pet", cat_ids.get('Higiene', 4), 12.50, 15, 5, "7891000004235", "Escova de dentes para pets", "Kelco", 0.05, "un"),
            
            # Camas
            ("Cama Pet Macia M", cat_ids.get('Camas e Casinhas', 5), 78.00, 6, 2, "7891000005234", "Cama macia e confortável", "Furacão Pet", 1.2, "un"),
        ]
        
        for produto_data in produtos_demo:
            produto_manager.adicionar(*produto_data)
        
        # Clientes de demonstração
        clientes_demo = [
            ("Maria Silva Santos", "123.456.789-01", "(11) 99999-1111", "maria.silva@email.com", "Rua das Flores, 123", "São Paulo", "01234-567"),
            ("João Pedro Oliveira", "987.654.321-02", "(11) 88888-2222", "joao.pedro@email.com", "Av. Principal, 456", "São Paulo", "01234-568"), 
            ("Ana Carolina Lima", "456.789.123-03", "(11) 77777-3333", "ana.lima@email.com", "Rua do Parque, 789", "São Paulo", "01234-569"),
            ("Carlos Eduardo Costa", "321.654.987-04", "(11) 66666-4444", "carlos.costa@email.com", "Rua das Palmeiras, 321", "São Paulo", "01234-570"),
            ("Fernanda Alves Rocha", "789.123.456-05", "(11) 55555-5555", "fernanda.rocha@email.com", "Av. Central, 654", "São Paulo", "01234-571"),
        ]
        
        cliente_ids = []
        for cliente_data in clientes_demo:
            cliente_id = cliente_manager.adicionar(*cliente_data)
            cliente_ids.append(cliente_id)
        
        # Pets de demonstração
        pets_demo = [
            ("Rex", cliente_ids[0], "Cão", "Golden Retriever", 3, 28.5, "Dourado", "Muito dócil e brincalhão"),
            ("Mimi", cliente_ids[0], "Gato", "Persa", 2, 4.2, "Branco", "Gosta de ficar no sol"),
            ("Bolt", cliente_ids[1], "Cão", "Border Collie", 5, 22.0, "Preto e branco", "Muito inteligente"),
            ("Luna", cliente_ids[2], "Gato", "Siamês", 1, 3.8, "Cinza", "Ainda filhote, muito ativa"),
            ("Thor", cliente_ids[2], "Cão", "Rottweiler", 4, 45.0, "Preto", "Grande e protetor"),
            ("Princesa", cliente_ids[3], "Cão", "Poodle", 6, 8.5, "Branco", "Muito carinhosa"),
            ("Simba", cliente_ids[4], "Gato", "Maine Coon", 3, 6.8, "Laranja", "Muito grande para um gato"),
            ("Mel", cliente_ids[4], "Cão", "Beagle", 2, 15.2, "Tricolor", "Adora comer"),
        ]
        
        for pet_data in pets_demo:
            pet_manager.adicionar(*pet_data)
        
        # Criar algumas vendas de exemplo para demonstrar relatórios
        from models import Venda
        import random
        from datetime import datetime, timedelta
        
        venda_manager = Venda(db)
        
        # Criar 10 vendas dos últimos 30 dias
        for i in range(10):
            # Data aleatória dos últimos 30 dias
            data_venda = datetime.now() - timedelta(days=random.randint(0, 30))
            
            # Cliente aleatório (alguns sem cliente)
            cliente_id = random.choice(cliente_ids + [None, None])  # 30% sem cliente
            
            # Forma de pagamento aleatória
            forma_pagamento = random.choice(['Dinheiro', 'Cartão de Débito', 'Cartão de Crédito', 'PIX'])
            
            # Desconto aleatório
            desconto = random.choice([0, 0, 0, 5.00, 10.00, 15.00])  # Maioria sem desconto
            
            # Criar venda
            venda_id = venda_manager.criar_venda(cliente_id, desconto, forma_pagamento)
            
            # Adicionar 1-4 itens aleatórios
            num_itens = random.randint(1, 4)
            produtos_disponiveis = produto_manager.listar_todos()
            
            for _ in range(num_itens):
                produto = random.choice(produtos_disponiveis)
                if produto[4] > 0:  # Se tem estoque
                    quantidade = random.randint(1, min(3, produto[4]))
                    venda_manager.adicionar_item(venda_id, produto[0], quantidade)
            
            # Finalizar venda
            venda_manager.finalizar_venda(venda_id)
            
            # Atualizar data da venda manualmente
            db.execute_update(
                "UPDATE vendas SET data_venda = ? WHERE id = ?",
                (data_venda.strftime('%Y-%m-%d %H:%M:%S'), venda_id)
            )
        
        print("✅ Dados de demonstração configurados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao configurar dados de demonstração: {e}")

if __name__ == "__main__":
    setup_demo_data() 