#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para inserir dados de exemplo no sistema PetShop
Execute este script após executar o main.py pela primeira vez
"""

from database import DatabaseManager
from models import Produto, Cliente, Pet, Categoria
from datetime import datetime, timedelta

def inserir_dados_exemplo():
    """Insere dados de exemplo no sistema"""
    
    print("🐾 Inserindo dados de exemplo no Sistema PetShop...")
    
    # Inicializar managers
    db = DatabaseManager()
    produto_manager = Produto(db)
    cliente_manager = Cliente(db)
    pet_manager = Pet(db)
    categoria_manager = Categoria(db)
    
    try:
        # Buscar IDs das categorias existentes
        categorias = categoria_manager.listar_todas()
        cat_racao_id = None
        cat_medicamento_id = None
        cat_acessorio_id = None
        cat_higiene_id = None
        cat_cama_id = None
        
        for cat in categorias:
            if 'Ração' in cat[1]:
                cat_racao_id = cat[0]
            elif 'Medicamento' in cat[1]:
                cat_medicamento_id = cat[0]
            elif 'Acessório' in cat[1]:
                cat_acessorio_id = cat[0]
            elif 'Higiene' in cat[1]:
                cat_higiene_id = cat[0]
            elif 'Cama' in cat[1]:
                cat_cama_id = cat[0]
        
        # 1. PRODUTOS DE EXEMPLO
        print("📦 Adicionando produtos...")
        
        produtos_exemplo = [
            # Rações
            ("Ração Premium Cães Adultos 15kg", cat_racao_id, 89.90, 25, 5, "7891000001234", "Ração super premium para cães adultos", "Royal Canin", 15.0, "kg"),
            ("Ração Gatos Filhotes 3kg", cat_racao_id, 45.50, 18, 3, "7891000001235", "Ração especial para gatos filhotes", "Whiskas", 3.0, "kg"),
            ("Ração Cães Pequeno Porte 7.5kg", cat_racao_id, 67.80, 15, 5, "7891000001236", "Ração para cães de pequeno porte", "Pedigree", 7.5, "kg"),
            ("Petisco Natural Cães 500g", cat_racao_id, 24.90, 30, 8, "7891000001237", "Petisco natural sem conservantes", "Bassar", 0.5, "kg"),
            
            # Medicamentos
            ("Vermífugo Cães e Gatos", cat_medicamento_id, 35.00, 12, 3, "7891000002234", "Vermífugo de amplo espectro", "Bayer", 0.1, "un"),
            ("Antipulgas Spot On Cães", cat_medicamento_id, 28.50, 20, 5, "7891000002235", "Antipulgas e carrapatos", "Frontline", 0.05, "un"),
            ("Vitamina para Pets", cat_medicamento_id, 42.00, 8, 2, "7891000002236", "Complexo vitamínico", "Vetnil", 0.15, "un"),
            
            # Acessórios
            ("Coleira Ajustável M", cat_acessorio_id, 19.90, 15, 5, "7891000003234", "Coleira de nylon ajustável", "Furacão Pet", 0.1, "un"),
            ("Guia Retrátil 5m", cat_acessorio_id, 45.00, 8, 2, "7891000003235", "Guia retrátil para cães médios", "Flexi", 0.3, "un"),
            ("Brinquedo Corda Cães", cat_acessorio_id, 15.50, 25, 8, "7891000003236", "Brinquedo de corda natural", "Jambo", 0.2, "un"),
            ("Comedouro Inox Duplo", cat_acessorio_id, 32.90, 12, 3, "7891000003237", "Comedouro de inox com dois compartimentos", "Chalesco", 0.5, "un"),
            
            # Higiene
            ("Shampoo Cães Pelos Longos", cat_higiene_id, 18.90, 20, 5, "7891000004234", "Shampoo específico para pelos longos", "Sanol", 0.5, "un"),
            ("Escova de Dentes Pet", cat_higiene_id, 12.50, 15, 5, "7891000004235", "Escova de dentes para pets", "Kelco", 0.05, "un"),
            ("Lenços Umedecidos Pet", cat_higiene_id, 8.90, 30, 10, "7891000004236", "Lenços para limpeza rápida", "Petix", 0.1, "un"),
            
            # Camas e Casinhas
            ("Cama Pet Macia M", cat_cama_id, 78.00, 6, 2, "7891000005234", "Cama macia e confortável", "Furacão Pet", 1.2, "un"),
            ("Casinha Plástica G", cat_cama_id, 156.00, 4, 1, "7891000005235", "Casinha resistente para externos", "Igloo", 3.5, "un"),
        ]
        
        for produto_data in produtos_exemplo:
            produto_manager.adicionar(*produto_data)
        
        # 2. CLIENTES DE EXEMPLO
        print("👥 Adicionando clientes...")
        
        clientes_exemplo = [
            ("Maria Silva Santos", "123.456.789-01", "(11) 99999-1111", "maria.silva@email.com", "Rua das Flores, 123", "São Paulo", "01234-567"),
            ("João Pedro Oliveira", "987.654.321-02", "(11) 88888-2222", "joao.pedro@email.com", "Av. Principal, 456", "São Paulo", "01234-568"),
            ("Ana Carolina Lima", "456.789.123-03", "(11) 77777-3333", "ana.lima@email.com", "Rua do Parque, 789", "São Paulo", "01234-569"),
            ("Carlos Eduardo Costa", "321.654.987-04", "(11) 66666-4444", "carlos.costa@email.com", "Rua das Palmeiras, 321", "São Paulo", "01234-570"),
            ("Fernanda Alves Rocha", "789.123.456-05", "(11) 55555-5555", "fernanda.rocha@email.com", "Av. Central, 654", "São Paulo", "01234-571"),
            ("Ricardo Mendes Silva", "147.258.369-06", "(11) 44444-6666", "ricardo.mendes@email.com", "Rua do Sol, 987", "São Paulo", "01234-572"),
            ("Juliana Santos Costa", "258.369.147-07", "(11) 33333-7777", "juliana.santos@email.com", "Rua da Lua, 159", "São Paulo", "01234-573"),
            ("Bruno Ferreira Lima", "369.147.258-08", "(11) 22222-8888", "bruno.ferreira@email.com", "Av. das Estrelas, 753", "São Paulo", "01234-574"),
        ]
        
        cliente_ids = []
        for cliente_data in clientes_exemplo:
            cliente_id = cliente_manager.adicionar(*cliente_data)
            cliente_ids.append(cliente_id)
        
        # 3. PETS DE EXEMPLO
        print("🐕 Adicionando pets...")
        
        pets_exemplo = [
            # Pets da Maria Silva
            ("Rex", cliente_ids[0], "Cão", "Golden Retriever", 3, 28.5, "Dourado", "Muito dócil e brincalhão"),
            ("Mimi", cliente_ids[0], "Gato", "Persa", 2, 4.2, "Branco", "Gosta de ficar no sol"),
            
            # Pets do João Pedro
            ("Bolt", cliente_ids[1], "Cão", "Border Collie", 5, 22.0, "Preto e branco", "Muito inteligente"),
            
            # Pets da Ana Carolina
            ("Luna", cliente_ids[2], "Gato", "Siamês", 1, 3.8, "Cinza", "Ainda filhote, muito ativa"),
            ("Thor", cliente_ids[2], "Cão", "Rottweiler", 4, 45.0, "Preto", "Grande e protetor"),
            
            # Pets do Carlos Eduardo
            ("Princesa", cliente_ids[3], "Cão", "Poodle", 6, 8.5, "Branco", "Muito carinhosa"),
            
            # Pets da Fernanda Alves
            ("Simba", cliente_ids[4], "Gato", "Maine Coon", 3, 6.8, "Laranja", "Muito grande para um gato"),
            ("Mel", cliente_ids[4], "Cão", "Beagle", 2, 15.2, "Tricolor", "Adora comer"),
            
            # Pets do Ricardo Mendes
            ("Zeus", cliente_ids[5], "Cão", "Pastor Alemão", 7, 35.0, "Preto e marrom", "Cão de guarda experiente"),
            
            # Pets da Juliana Santos
            ("Lola", cliente_ids[6], "Cão", "Shih Tzu", 4, 6.0, "Dourado e branco", "Muito vaidosa"),
            
            # Pets do Bruno Ferreira
            ("Garfield", cliente_ids[7], "Gato", "Persa", 5, 5.5, "Laranja", "Preguiçoso como o personagem"),
            ("Max", cliente_ids[7], "Cão", "Labrador", 1, 12.0, "Amarelo", "Ainda filhote, muito enérgico"),
        ]
        
        for pet_data in pets_exemplo:
            pet_manager.adicionar(*pet_data)
        
        print("✅ Dados de exemplo inseridos com sucesso!")
        print("\n📊 Resumo dos dados inseridos:")
        print(f"• {len(produtos_exemplo)} produtos adicionados")
        print(f"• {len(clientes_exemplo)} clientes cadastrados")
        print(f"• {len(pets_exemplo)} pets registrados")
        print("\n🎯 Agora você pode:")
        print("1. Testar o sistema de vendas")
        print("2. Criar agendamentos para os pets")
        print("3. Visualizar relatórios")
        print("4. Gerenciar o estoque")
        
        print("\n💡 Dica: Execute 'python main.py' para acessar o sistema!")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")

if __name__ == "__main__":
    inserir_dados_exemplo() 