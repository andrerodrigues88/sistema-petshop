#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, date, timedelta
from database import DatabaseManager
from models import Produto, Cliente, Pet, Venda, Agendamento, Categoria

class PetShopSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.produto_manager = Produto(self.db)
        self.cliente_manager = Cliente(self.db)
        self.pet_manager = Pet(self.db)
        self.venda_manager = Venda(self.db)
        self.agendamento_manager = Agendamento(self.db)
        self.categoria_manager = Categoria(self.db)
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa e aguarda o usuário pressionar Enter"""
        input("\nPressione Enter para continuar...")
    
    def exibir_header(self, titulo):
        """Exibe cabeçalho formatado"""
        print("=" * 60)
        print(f"🐾 SISTEMA PETSHOP - {titulo.upper()} 🐾")
        print("=" * 60)
    
    def menu_principal(self):
        """Exibe o menu principal do sistema"""
        while True:
            self.limpar_tela()
            self.exibir_header("MENU PRINCIPAL")
            print("1. 📦 Gestão de Estoque")
            print("2. 👥 Gestão de Clientes")
            print("3. 🐕 Gestão de Pets")
            print("4. 🛒 Vendas")
            print("5. 📅 Agendamentos e Serviços")
            print("6. 📊 Relatórios")
            print("0. ❌ Sair")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.menu_estoque()
            elif opcao == "2":
                self.menu_clientes()
            elif opcao == "3":
                self.menu_pets()
            elif opcao == "4":
                self.menu_vendas()
            elif opcao == "5":
                self.menu_agendamentos()
            elif opcao == "6":
                self.menu_relatorios()
            elif opcao == "0":
                print("\n👋 Obrigado por usar o Sistema PetShop!")
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def menu_estoque(self):
        """Menu de gestão de estoque"""
        while True:
            self.limpar_tela()
            self.exibir_header("GESTÃO DE ESTOQUE")
            print("1. ➕ Adicionar Produto")
            print("2. 📋 Listar Produtos")
            print("3. 🔍 Buscar Produto")
            print("4. ⚠️  Produtos com Estoque Baixo")
            print("5. 📈 Atualizar Estoque")
            print("6. 🏷️  Gerenciar Categorias")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.adicionar_produto()
            elif opcao == "2":
                self.listar_produtos()
            elif opcao == "3":
                self.buscar_produto()
            elif opcao == "4":
                self.produtos_estoque_baixo()
            elif opcao == "5":
                self.atualizar_estoque()
            elif opcao == "6":
                self.gerenciar_categorias()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def adicionar_produto(self):
        """Adiciona um novo produto"""
        self.limpar_tela()
        self.exibir_header("ADICIONAR PRODUTO")
        
        try:
            nome = input("Nome do produto: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                self.pausar()
                return
            
            # Listar categorias
            categorias = self.categoria_manager.listar_todas()
            print("\nCategorias disponíveis:")
            for cat in categorias:
                print(f"{cat[0]}. {cat[1]}")
            
            categoria_id = int(input("\nID da categoria: "))
            preco = float(input("Preço (R$): "))
            estoque_atual = int(input("Estoque inicial (padrão 0): ") or "0")
            estoque_minimo = int(input("Estoque mínimo (padrão 5): ") or "5")
            codigo_barras = input("Código de barras (opcional): ").strip() or None
            descricao = input("Descrição (opcional): ").strip() or None
            marca = input("Marca (opcional): ").strip() or None
            peso = input("Peso em kg (opcional): ").strip()
            peso = float(peso) if peso else None
            unidade_medida = input("Unidade de medida (un, kg, ml, etc.): ").strip() or None
            
            produto_id = self.produto_manager.adicionar(
                nome, categoria_id, preco, estoque_atual, estoque_minimo,
                codigo_barras, descricao, marca, peso, unidade_medida
            )
            
            print(f"✅ Produto '{nome}' adicionado com sucesso! ID: {produto_id}")
            
        except ValueError:
            print("❌ Erro nos valores inseridos!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        self.limpar_tela()
        self.exibir_header("LISTA DE PRODUTOS")
        
        produtos = self.produto_manager.listar_todos()
        
        if not produtos:
            print("❌ Nenhum produto cadastrado!")
        else:
            print(f"{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Preço':<10} {'Estoque':<10}")
            print("-" * 75)
            for produto in produtos:
                categoria = produto[12] if produto[12] else "Sem categoria"
                print(f"{produto[0]:<5} {produto[1][:29]:<30} {categoria[:19]:<20} R${produto[3]:<9.2f} {produto[4]:<10}")
        
        self.pausar()
    
    def buscar_produto(self):
        """Busca produto por nome"""
        self.limpar_tela()
        self.exibir_header("BUSCAR PRODUTO")
        
        nome = input("Digite parte do nome do produto: ").strip()
        if not nome:
            print("❌ Nome é obrigatório!")
            self.pausar()
            return
        
        produtos = self.produto_manager.buscar_por_nome(nome)
        
        if not produtos:
            print("❌ Nenhum produto encontrado!")
        else:
            print(f"{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Preço':<10} {'Estoque':<10}")
            print("-" * 75)
            for produto in produtos:
                categoria = produto[12] if produto[12] else "Sem categoria"
                print(f"{produto[0]:<5} {produto[1][:29]:<30} {categoria[:19]:<20} R${produto[3]:<9.2f} {produto[4]:<10}")
        
        self.pausar()
    
    def produtos_estoque_baixo(self):
        """Lista produtos com estoque baixo"""
        self.limpar_tela()
        self.exibir_header("PRODUTOS COM ESTOQUE BAIXO")
        
        produtos = self.produto_manager.produtos_estoque_baixo()
        
        if not produtos:
            print("✅ Todos os produtos estão com estoque adequado!")
        else:
            print(f"{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Atual':<8} {'Mínimo':<8}")
            print("-" * 73)
            for produto in produtos:
                categoria = produto[12] if produto[12] else "Sem categoria"
                print(f"{produto[0]:<5} {produto[1][:29]:<30} {categoria[:19]:<20} {produto[4]:<8} {produto[5]:<8}")
        
        self.pausar()
    
    def atualizar_estoque(self):
        """Atualiza estoque de um produto"""
        self.limpar_tela()
        self.exibir_header("ATUALIZAR ESTOQUE")
        
        try:
            produto_id = int(input("ID do produto: "))
            produto = self.produto_manager.buscar_por_id(produto_id)
            
            if not produto:
                print("❌ Produto não encontrado!")
                self.pausar()
                return
            
            print(f"\nProduto: {produto[1]}")
            print(f"Estoque atual: {produto[4]}")
            
            nova_quantidade = int(input("Nova quantidade: "))
            motivo = input("Motivo da alteração: ").strip() or "Ajuste manual"
            
            if self.produto_manager.atualizar_estoque(produto_id, nova_quantidade, motivo):
                print("✅ Estoque atualizado com sucesso!")
            else:
                print("❌ Erro ao atualizar estoque!")
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def gerenciar_categorias(self):
        """Gerencia categorias de produtos"""
        while True:
            self.limpar_tela()
            self.exibir_header("GERENCIAR CATEGORIAS")
            print("1. 📋 Listar Categorias")
            print("2. ➕ Adicionar Categoria")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_categorias()
            elif opcao == "2":
                self.adicionar_categoria()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def listar_categorias(self):
        """Lista todas as categorias"""
        self.limpar_tela()
        self.exibir_header("LISTA DE CATEGORIAS")
        
        categorias = self.categoria_manager.listar_todas()
        
        if not categorias:
            print("❌ Nenhuma categoria cadastrada!")
        else:
            print(f"{'ID':<5} {'Nome':<25} {'Descrição':<40}")
            print("-" * 70)
            for categoria in categorias:
                descricao = categoria[2] if categoria[2] else ""
                print(f"{categoria[0]:<5} {categoria[1]:<25} {descricao[:39]:<40}")
        
        self.pausar()
    
    def adicionar_categoria(self):
        """Adiciona uma nova categoria"""
        self.limpar_tela()
        self.exibir_header("ADICIONAR CATEGORIA")
        
        try:
            nome = input("Nome da categoria: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                self.pausar()
                return
            
            descricao = input("Descrição (opcional): ").strip() or None
            
            categoria_id = self.categoria_manager.adicionar(nome, descricao)
            print(f"✅ Categoria '{nome}' adicionada com sucesso! ID: {categoria_id}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def menu_clientes(self):
        """Menu de gestão de clientes"""
        while True:
            self.limpar_tela()
            self.exibir_header("GESTÃO DE CLIENTES")
            print("1. ➕ Adicionar Cliente")
            print("2. 📋 Listar Clientes")
            print("3. 🔍 Buscar Cliente")
            print("4. ✏️  Editar Cliente")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.adicionar_cliente()
            elif opcao == "2":
                self.listar_clientes()
            elif opcao == "3":
                self.buscar_cliente()
            elif opcao == "4":
                self.editar_cliente()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        self.limpar_tela()
        self.exibir_header("ADICIONAR CLIENTE")
        
        try:
            nome = input("Nome completo: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                self.pausar()
                return
            
            cpf = input("CPF (opcional): ").strip() or None
            telefone = input("Telefone: ").strip() or None
            email = input("Email (opcional): ").strip() or None
            endereco = input("Endereço (opcional): ").strip() or None
            cidade = input("Cidade (opcional): ").strip() or None
            cep = input("CEP (opcional): ").strip() or None
            
            cliente_id = self.cliente_manager.adicionar(nome, cpf, telefone, email, endereco, cidade, cep)
            print(f"✅ Cliente '{nome}' adicionado com sucesso! ID: {cliente_id}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        self.limpar_tela()
        self.exibir_header("LISTA DE CLIENTES")
        
        clientes = self.cliente_manager.listar_todos()
        
        if not clientes:
            print("❌ Nenhum cliente cadastrado!")
        else:
            print(f"{'ID':<5} {'Nome':<30} {'Telefone':<15} {'Email':<25}")
            print("-" * 75)
            for cliente in clientes:
                telefone = cliente[3] if cliente[3] else ""
                email = cliente[4] if cliente[4] else ""
                print(f"{cliente[0]:<5} {cliente[1][:29]:<30} {telefone:<15} {email[:24]:<25}")
        
        self.pausar()
    
    def buscar_cliente(self):
        """Busca cliente por nome"""
        self.limpar_tela()
        self.exibir_header("BUSCAR CLIENTE")
        
        nome = input("Digite parte do nome do cliente: ").strip()
        if not nome:
            print("❌ Nome é obrigatório!")
            self.pausar()
            return
        
        clientes = self.cliente_manager.buscar_por_nome(nome)
        
        if not clientes:
            print("❌ Nenhum cliente encontrado!")
        else:
            print(f"{'ID':<5} {'Nome':<30} {'Telefone':<15} {'Email':<25}")
            print("-" * 75)
            for cliente in clientes:
                telefone = cliente[3] if cliente[3] else ""
                email = cliente[4] if cliente[4] else ""
                print(f"{cliente[0]:<5} {cliente[1][:29]:<30} {telefone:<15} {email[:24]:<25}")
        
        self.pausar()
    
    def editar_cliente(self):
        """Edita dados de um cliente"""
        self.limpar_tela()
        self.exibir_header("EDITAR CLIENTE")
        
        try:
            cliente_id = int(input("ID do cliente: "))
            cliente = self.cliente_manager.buscar_por_id(cliente_id)
            
            if not cliente:
                print("❌ Cliente não encontrado!")
                self.pausar()
                return
            
            print(f"\nDados atuais do cliente:")
            print(f"Nome: {cliente[1]}")
            print(f"CPF: {cliente[2] if cliente[2] else 'Não informado'}")
            print(f"Telefone: {cliente[3] if cliente[3] else 'Não informado'}")
            print(f"Email: {cliente[4] if cliente[4] else 'Não informado'}")
            print(f"Endereço: {cliente[5] if cliente[5] else 'Não informado'}")
            print(f"Cidade: {cliente[6] if cliente[6] else 'Não informado'}")
            print(f"CEP: {cliente[7] if cliente[7] else 'Não informado'}")
            
            print("\nDigite os novos dados (pressione Enter para manter o atual):")
            
            nome = input(f"Nome [{cliente[1]}]: ").strip() or cliente[1]
            cpf = input(f"CPF [{cliente[2] if cliente[2] else ''}]: ").strip() or cliente[2]
            telefone = input(f"Telefone [{cliente[3] if cliente[3] else ''}]: ").strip() or cliente[3]
            email = input(f"Email [{cliente[4] if cliente[4] else ''}]: ").strip() or cliente[4]
            endereco = input(f"Endereço [{cliente[5] if cliente[5] else ''}]: ").strip() or cliente[5]
            cidade = input(f"Cidade [{cliente[6] if cliente[6] else ''}]: ").strip() or cliente[6]
            cep = input(f"CEP [{cliente[7] if cliente[7] else ''}]: ").strip() or cliente[7]
            
            if self.cliente_manager.atualizar(cliente_id, nome, cpf, telefone, email, endereco, cidade, cep):
                print("✅ Cliente atualizado com sucesso!")
            else:
                print("❌ Erro ao atualizar cliente!")
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def menu_pets(self):
        """Menu de gestão de pets"""
        while True:
            self.limpar_tela()
            self.exibir_header("GESTÃO DE PETS")
            print("1. ➕ Adicionar Pet")
            print("2. 📋 Listar Pets")
            print("3. 🔍 Buscar Pet")
            print("4. 📋 Pets por Cliente")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.adicionar_pet()
            elif opcao == "2":
                self.listar_pets()
            elif opcao == "3":
                self.buscar_pet()
            elif opcao == "4":
                self.pets_por_cliente()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def adicionar_pet(self):
        """Adiciona um novo pet"""
        self.limpar_tela()
        self.exibir_header("ADICIONAR PET")
        
        try:
            # Primeiro, mostrar clientes para seleção
            clientes = self.cliente_manager.listar_todos()
            if not clientes:
                print("❌ É necessário cadastrar um cliente antes de adicionar um pet!")
                self.pausar()
                return
            
            print("Clientes cadastrados:")
            for cliente in clientes[:10]:  # Mostrar apenas os primeiros 10
                print(f"{cliente[0]}. {cliente[1]} - {cliente[3] if cliente[3] else 'Sem telefone'}")
            
            if len(clientes) > 10:
                print("... (digite o ID do cliente desejado)")
            
            cliente_id = int(input("\nID do cliente: "))
            
            # Verificar se cliente existe
            cliente = self.cliente_manager.buscar_por_id(cliente_id)
            if not cliente:
                print("❌ Cliente não encontrado!")
                self.pausar()
                return
            
            nome = input("Nome do pet: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                self.pausar()
                return
            
            especie = input("Espécie (cão, gato, etc.): ").strip()
            if not especie:
                print("❌ Espécie é obrigatória!")
                self.pausar()
                return
            
            raca = input("Raça (opcional): ").strip() or None
            idade = input("Idade em anos (opcional): ").strip()
            idade = int(idade) if idade else None
            peso = input("Peso em kg (opcional): ").strip()
            peso = float(peso) if peso else None
            cor = input("Cor (opcional): ").strip() or None
            observacoes = input("Observações (opcional): ").strip() or None
            
            pet_id = self.pet_manager.adicionar(nome, cliente_id, especie, raca, idade, peso, cor, observacoes)
            print(f"✅ Pet '{nome}' adicionado com sucesso! ID: {pet_id}")
            
        except ValueError:
            print("❌ Erro nos valores inseridos!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_pets(self):
        """Lista todos os pets"""
        self.limpar_tela()
        self.exibir_header("LISTA DE PETS")
        
        pets = self.pet_manager.listar_todos()
        
        if not pets:
            print("❌ Nenhum pet cadastrado!")
        else:
            print(f"{'ID':<5} {'Nome':<20} {'Espécie':<15} {'Raça':<15} {'Cliente':<25}")
            print("-" * 80)
            for pet in pets:
                raca = pet[4] if pet[4] else "Não informada"
                cliente_nome = pet[9]  # cliente_nome vem da query JOIN
                print(f"{pet[0]:<5} {pet[1][:19]:<20} {pet[3][:14]:<15} {raca[:14]:<15} {cliente_nome[:24]:<25}")
        
        self.pausar()
    
    def buscar_pet(self):
        """Busca pet por nome"""
        self.limpar_tela()
        self.exibir_header("BUSCAR PET")
        
        nome = input("Digite parte do nome do pet: ").strip()
        if not nome:
            print("❌ Nome é obrigatório!")
            self.pausar()
            return
        
        pets = self.pet_manager.buscar_por_nome(nome)
        
        if not pets:
            print("❌ Nenhum pet encontrado!")
        else:
            print(f"{'ID':<5} {'Nome':<20} {'Espécie':<15} {'Raça':<15} {'Cliente':<25}")
            print("-" * 80)
            for pet in pets:
                raca = pet[4] if pet[4] else "Não informada"
                cliente_nome = pet[9]  # cliente_nome vem da query JOIN
                print(f"{pet[0]:<5} {pet[1][:19]:<20} {pet[3][:14]:<15} {raca[:14]:<15} {cliente_nome[:24]:<25}")
        
        self.pausar()
    
    def pets_por_cliente(self):
        """Lista pets de um cliente específico"""
        self.limpar_tela()
        self.exibir_header("PETS POR CLIENTE")
        
        try:
            cliente_id = int(input("ID do cliente: "))
            cliente = self.cliente_manager.buscar_por_id(cliente_id)
            
            if not cliente:
                print("❌ Cliente não encontrado!")
                self.pausar()
                return
            
            pets = self.pet_manager.listar_por_cliente(cliente_id)
            
            print(f"\nPets do cliente: {cliente[1]}")
            print("-" * 60)
            
            if not pets:
                print("❌ Este cliente não possui pets cadastrados!")
            else:
                print(f"{'ID':<5} {'Nome':<20} {'Espécie':<15} {'Raça':<15}")
                print("-" * 55)
                for pet in pets:
                    raca = pet[4] if pet[4] else "Não informada"
                    print(f"{pet[0]:<5} {pet[1][:19]:<20} {pet[3][:14]:<15} {raca[:14]:<15}")
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def menu_vendas(self):
        """Menu de vendas"""
        while True:
            self.limpar_tela()
            self.exibir_header("SISTEMA DE VENDAS")
            print("1. 🛒 Nova Venda")
            print("2. 📋 Listar Vendas")
            print("3. 🔍 Buscar Venda")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.nova_venda()
            elif opcao == "2":
                self.listar_vendas()
            elif opcao == "3":
                self.buscar_venda()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def nova_venda(self):
        """Realiza uma nova venda"""
        self.limpar_tela()
        self.exibir_header("NOVA VENDA")
        
        try:
            # Cliente (opcional)
            resposta = input("Deseja vincular a um cliente? (s/n): ").strip().lower()
            cliente_id = None
            
            if resposta == 's':
                cliente_nome = input("Digite parte do nome do cliente: ").strip()
                if cliente_nome:
                    clientes = self.cliente_manager.buscar_por_nome(cliente_nome)
                    if clientes:
                        print("\nClientes encontrados:")
                        for cliente in clientes[:5]:
                            print(f"{cliente[0]}. {cliente[1]} - {cliente[3] if cliente[3] else 'Sem telefone'}")
                        
                        cliente_id = int(input("ID do cliente (0 para venda sem cliente): "))
                        if cliente_id == 0:
                            cliente_id = None
                    else:
                        print("❌ Cliente não encontrado. Venda será sem cliente.")
            
            # Criar venda
            forma_pagamento = input("Forma de pagamento (Dinheiro/Cartão/PIX): ").strip() or "Dinheiro"
            desconto = float(input("Desconto em R$ (0 para sem desconto): ") or "0")
            
            venda_id = self.venda_manager.criar_venda(cliente_id, desconto, forma_pagamento)
            print(f"\n✅ Venda #{venda_id} criada!")
            
            # Adicionar itens
            while True:
                print(f"\n--- VENDA #{venda_id} ---")
                produto_nome = input("Nome do produto (ou 'fim' para finalizar): ").strip()
                
                if produto_nome.lower() == 'fim':
                    break
                
                produtos = self.produto_manager.buscar_por_nome(produto_nome)
                if not produtos:
                    print("❌ Produto não encontrado!")
                    continue
                
                print("\nProdutos encontrados:")
                for produto in produtos[:5]:
                    print(f"{produto[0]}. {produto[1]} - R${produto[3]:.2f} (Estoque: {produto[4]})")
                
                produto_id = int(input("ID do produto: "))
                produto = self.produto_manager.buscar_por_id(produto_id)
                
                if not produto:
                    print("❌ Produto não encontrado!")
                    continue
                
                if produto[4] <= 0:  # estoque_atual
                    print("❌ Produto sem estoque!")
                    continue
                
                quantidade = int(input(f"Quantidade (máx {produto[4]}): "))
                
                if quantidade > produto[4]:
                    print(f"❌ Estoque insuficiente! Disponível: {produto[4]}")
                    continue
                
                if self.venda_manager.adicionar_item(venda_id, produto_id, quantidade):
                    print(f"✅ {quantidade}x {produto[1]} adicionado à venda!")
                else:
                    print("❌ Erro ao adicionar item!")
            
            # Finalizar venda
            venda_info = self.venda_manager.buscar_venda(venda_id)
            if venda_info and venda_info['itens']:
                print(f"\n--- RESUMO DA VENDA #{venda_id} ---")
                print(f"Cliente: {venda_info['venda'][7] if venda_info['venda'][7] else 'Não informado'}")
                print(f"Forma de pagamento: {venda_info['venda'][4]}")
                
                print("\nItens:")
                for item in venda_info['itens']:
                    print(f"- {item[3]}x {item[6]} - R${item[5]:.2f}")
                
                print(f"\nDesconto: R${venda_info['venda'][2]:.2f}")
                print(f"TOTAL: R${venda_info['venda'][1]:.2f}")
                
                confirma = input("\nConfirmar venda? (s/n): ").strip().lower()
                if confirma == 's':
                    self.venda_manager.finalizar_venda(venda_id)
                    print("✅ Venda finalizada com sucesso!")
                else:
                    print("❌ Venda cancelada!")
            else:
                print("❌ Nenhum item foi adicionado à venda!")
            
        except ValueError:
            print("❌ Erro nos valores inseridos!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_vendas(self):
        """Lista as vendas recentes"""
        self.limpar_tela()
        self.exibir_header("VENDAS RECENTES")
        
        vendas = self.venda_manager.listar_vendas(30)
        
        if not vendas:
            print("❌ Nenhuma venda registrada!")
        else:
            print(f"{'ID':<5} {'Data':<12} {'Cliente':<25} {'Total':<12} {'Pagamento':<12}")
            print("-" * 66)
            for venda in vendas:
                data = venda[5][:10] if venda[5] else ""  # Só a data, sem hora
                cliente = venda[6] if venda[6] else "Não informado"
                print(f"{venda[0]:<5} {data:<12} {cliente[:24]:<25} R${venda[1]:<11.2f} {venda[4][:11]:<12}")
        
        self.pausar()
    
    def buscar_venda(self):
        """Busca uma venda específica"""
        self.limpar_tela()
        self.exibir_header("BUSCAR VENDA")
        
        try:
            venda_id = int(input("ID da venda: "))
            venda_info = self.venda_manager.buscar_venda(venda_id)
            
            if not venda_info:
                print("❌ Venda não encontrada!")
            else:
                venda = venda_info['venda']
                itens = venda_info['itens']
                
                print(f"\n--- VENDA #{venda[0]} ---")
                print(f"Data: {venda[5]}")
                print(f"Cliente: {venda[7] if venda[7] else 'Não informado'}")
                print(f"Forma de pagamento: {venda[4]}")
                
                if itens:
                    print("\nItens:")
                    for item in itens:
                        print(f"- {item[3]}x {item[6]} - R${item[4]:.2f} cada = R${item[5]:.2f}")
                
                print(f"\nDesconto: R${venda[2]:.2f}")
                print(f"TOTAL: R${venda[1]:.2f}")
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def menu_agendamentos(self):
        """Menu de agendamentos e serviços"""
        while True:
            self.limpar_tela()
            self.exibir_header("AGENDAMENTOS E SERVIÇOS")
            print("1. 📅 Novo Agendamento")
            print("2. 📋 Listar Agendamentos")
            print("3. ✅ Atualizar Status")
            print("4. 🛠️  Tipos de Serviços")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.novo_agendamento()
            elif opcao == "2":
                self.listar_agendamentos()
            elif opcao == "3":
                self.atualizar_status_agendamento()
            elif opcao == "4":
                self.listar_tipos_servicos()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def novo_agendamento(self):
        """Cria um novo agendamento"""
        self.limpar_tela()
        self.exibir_header("NOVO AGENDAMENTO")
        
        try:
            # Selecionar cliente
            cliente_nome = input("Digite parte do nome do cliente: ").strip()
            if not cliente_nome:
                print("❌ Nome é obrigatório!")
                self.pausar()
                return
            
            clientes = self.cliente_manager.buscar_por_nome(cliente_nome)
            if not clientes:
                print("❌ Cliente não encontrado!")
                self.pausar()
                return
            
            print("\nClientes encontrados:")
            for cliente in clientes[:5]:
                print(f"{cliente[0]}. {cliente[1]} - {cliente[3] if cliente[3] else 'Sem telefone'}")
            
            cliente_id = int(input("ID do cliente: "))
            cliente = self.cliente_manager.buscar_por_id(cliente_id)
            if not cliente:
                print("❌ Cliente não encontrado!")
                self.pausar()
                return
            
            # Selecionar pet
            pets = self.pet_manager.listar_por_cliente(cliente_id)
            if not pets:
                print("❌ Este cliente não possui pets cadastrados!")
                self.pausar()
                return
            
            print(f"\nPets de {cliente[1]}:")
            for pet in pets:
                print(f"{pet[0]}. {pet[1]} ({pet[3]})")
            
            pet_id = int(input("ID do pet: "))
            pet = self.pet_manager.buscar_por_id(pet_id)
            if not pet:
                print("❌ Pet não encontrado!")
                self.pausar()
                return
            
            # Selecionar serviço
            servicos = self.agendamento_manager.listar_tipos_servicos()
            print("\nServiços disponíveis:")
            for servico in servicos:
                duracao = f"{servico[3]}min" if servico[3] else "N/A"
                print(f"{servico[0]}. {servico[1]} - R${servico[2]:.2f} ({duracao})")
            
            tipo_servico_id = int(input("ID do serviço: "))
            
            # Data e hora
            print("\nData do agendamento (formato: DD/MM/AAAA HH:MM):")
            data_str = input("Data e hora: ").strip()
            
            try:
                data_agendamento = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            except ValueError:
                print("❌ Formato de data inválido!")
                self.pausar()
                return
            
            observacoes = input("Observações (opcional): ").strip() or None
            
            agendamento_id = self.agendamento_manager.criar_agendamento(
                cliente_id, pet_id, tipo_servico_id, data_agendamento, observacoes
            )
            
            print(f"✅ Agendamento #{agendamento_id} criado com sucesso!")
            print(f"Cliente: {cliente[1]}")
            print(f"Pet: {pet[1]}")
            print(f"Data: {data_agendamento.strftime('%d/%m/%Y às %H:%M')}")
            
        except ValueError:
            print("❌ Erro nos valores inseridos!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_agendamentos(self):
        """Lista agendamentos por período"""
        self.limpar_tela()
        self.exibir_header("LISTAR AGENDAMENTOS")
        
        print("1. Agendamentos de hoje")
        print("2. Próximos 7 dias")
        print("3. Todos os agendamentos")
        print("4. Período personalizado")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        data_inicio = None
        data_fim = None
        
        if opcao == "1":
            data_inicio = date.today().strftime("%Y-%m-%d")
            data_fim = data_inicio
        elif opcao == "2":
            data_inicio = date.today().strftime("%Y-%m-%d")
            data_fim = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        elif opcao == "3":
            pass  # Listar todos
        elif opcao == "4":
            try:
                data_inicio = input("Data início (DD/MM/AAAA): ").strip()
                data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
                data_fim = input("Data fim (DD/MM/AAAA): ").strip()
                data_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                print("❌ Formato de data inválido!")
                self.pausar()
                return
        else:
            print("❌ Opção inválida!")
            self.pausar()
            return
        
        agendamentos = self.agendamento_manager.listar_agendamentos(data_inicio, data_fim)
        
        if not agendamentos:
            print("❌ Nenhum agendamento encontrado!")
        else:
            print(f"\n{'ID':<5} {'Data/Hora':<17} {'Cliente':<20} {'Pet':<15} {'Serviço':<20} {'Status':<12}")
            print("-" * 89)
            for agendamento in agendamentos:
                data_hora = agendamento[4][:16] if agendamento[4] else ""  # YYYY-MM-DD HH:MM
                # Converter para formato brasileiro
                if data_hora:
                    try:
                        dt = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
                        data_hora = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        pass
                
                cliente_nome = agendamento[8][:19] if agendamento[8] else ""
                pet_nome = agendamento[9][:14] if agendamento[9] else ""
                servico_nome = agendamento[10][:19] if agendamento[10] else ""
                status = agendamento[5][:11] if agendamento[5] else ""
                
                print(f"{agendamento[0]:<5} {data_hora:<17} {cliente_nome:<20} {pet_nome:<15} {servico_nome:<20} {status:<12}")
        
        self.pausar()
    
    def atualizar_status_agendamento(self):
        """Atualiza status de um agendamento"""
        self.limpar_tela()
        self.exibir_header("ATUALIZAR STATUS DO AGENDAMENTO")
        
        try:
            agendamento_id = int(input("ID do agendamento: "))
            
            print("\nStatus disponíveis:")
            print("1. agendado")
            print("2. confirmado")
            print("3. em_andamento")
            print("4. concluido")
            print("5. cancelado")
            print("6. nao_compareceu")
            
            opcao = input("Escolha o novo status: ").strip()
            
            status_map = {
                "1": "agendado",
                "2": "confirmado", 
                "3": "em_andamento",
                "4": "concluido",
                "5": "cancelado",
                "6": "nao_compareceu"
            }
            
            if opcao not in status_map:
                print("❌ Opção inválida!")
                self.pausar()
                return
            
            novo_status = status_map[opcao]
            
            if self.agendamento_manager.atualizar_status(agendamento_id, novo_status):
                print(f"✅ Status atualizado para '{novo_status}'!")
            else:
                print("❌ Erro ao atualizar status!")
            
        except ValueError:
            print("❌ ID deve ser um número!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def listar_tipos_servicos(self):
        """Lista tipos de serviços disponíveis"""
        self.limpar_tela()
        self.exibir_header("TIPOS DE SERVIÇOS")
        
        servicos = self.agendamento_manager.listar_tipos_servicos()
        
        if not servicos:
            print("❌ Nenhum serviço cadastrado!")
        else:
            print(f"{'ID':<5} {'Nome':<25} {'Preço':<12} {'Duração':<15} {'Descrição':<30}")
            print("-" * 87)
            for servico in servicos:
                duracao = f"{servico[3]} min" if servico[3] else "N/A"
                descricao = servico[4][:29] if servico[4] else ""
                print(f"{servico[0]:<5} {servico[1][:24]:<25} R${servico[2]:<11.2f} {duracao:<15} {descricao:<30}")
        
        self.pausar()
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        while True:
            self.limpar_tela()
            self.exibir_header("RELATÓRIOS")
            print("1. 📊 Resumo Geral")
            print("2. 💰 Vendas por Período")
            print("3. 📦 Estoque Atual")
            print("4. 👥 Clientes Cadastrados")
            print("5. 🐕 Pets por Espécie")
            print("6. 📅 Agendamentos do Dia")
            print("0. ⬅️  Voltar")
            print("-" * 60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.relatorio_resumo_geral()
            elif opcao == "2":
                self.relatorio_vendas_periodo()
            elif opcao == "3":
                self.relatorio_estoque()
            elif opcao == "4":
                self.relatorio_clientes()
            elif opcao == "5":
                self.relatorio_pets_especie()
            elif opcao == "6":
                self.relatorio_agendamentos_dia()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
                self.pausar()
    
    def relatorio_resumo_geral(self):
        """Relatório resumo geral do sistema"""
        self.limpar_tela()
        self.exibir_header("RESUMO GERAL")
        
        try:
            # Contar registros
            total_produtos = len(self.produto_manager.listar_todos())
            total_clientes = len(self.cliente_manager.listar_todos())
            total_pets = len(self.pet_manager.listar_todos())
            
            # Vendas do mês atual
            vendas_mes = self.db.execute_query('''
                SELECT COUNT(*), COALESCE(SUM(total), 0)
                FROM vendas 
                WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
            ''')
            
            total_vendas_mes = vendas_mes[0][0] if vendas_mes else 0
            valor_vendas_mes = vendas_mes[0][1] if vendas_mes else 0
            
            # Agendamentos hoje
            agendamentos_hoje = self.db.execute_query('''
                SELECT COUNT(*)
                FROM agendamentos 
                WHERE DATE(data_agendamento) = DATE('now')
            ''')
            
            total_agendamentos_hoje = agendamentos_hoje[0][0] if agendamentos_hoje else 0
            
            # Produtos com estoque baixo
            produtos_estoque_baixo = len(self.produto_manager.produtos_estoque_baixo())
            
            print("📊 ESTATÍSTICAS GERAIS")
            print("-" * 40)
            print(f"Total de Produtos: {total_produtos}")
            print(f"Total de Clientes: {total_clientes}")
            print(f"Total de Pets: {total_pets}")
            print()
            print("📅 ESTE MÊS")
            print("-" * 40)
            print(f"Vendas realizadas: {total_vendas_mes}")
            print(f"Faturamento: R${valor_vendas_mes:.2f}")
            print()
            print("🚨 ALERTAS")
            print("-" * 40)
            print(f"Agendamentos hoje: {total_agendamentos_hoje}")
            print(f"Produtos com estoque baixo: {produtos_estoque_baixo}")
            
            if produtos_estoque_baixo > 0:
                print("\n⚠️  ATENÇÃO: Existem produtos com estoque baixo!")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
        
        self.pausar()
    
    def relatorio_vendas_periodo(self):
        """Relatório de vendas por período"""
        self.limpar_tela()
        self.exibir_header("VENDAS POR PERÍODO")
        
        try:
            data_inicio = input("Data início (DD/MM/AAAA): ").strip()
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_fim = input("Data fim (DD/MM/AAAA): ").strip()
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            vendas = self.db.execute_query('''
                SELECT DATE(data_venda) as data, COUNT(*) as qtd_vendas, SUM(total) as total_vendas
                FROM vendas 
                WHERE DATE(data_venda) BETWEEN ? AND ?
                GROUP BY DATE(data_venda)
                ORDER BY data
            ''', (data_inicio, data_fim))
            
            if not vendas:
                print("❌ Nenhuma venda encontrada no período!")
            else:
                print(f"\n{'Data':<12} {'Qtd Vendas':<12} {'Total (R$)':<15}")
                print("-" * 39)
                
                total_geral = 0
                qtd_geral = 0
                
                for venda in vendas:
                    # Converter data para formato brasileiro
                    data_br = datetime.strptime(venda[0], "%Y-%m-%d").strftime("%d/%m/%Y")
                    print(f"{data_br:<12} {venda[1]:<12} R${venda[2]:<14.2f}")
                    total_geral += venda[2]
                    qtd_geral += venda[1]
                
                print("-" * 39)
                print(f"{'TOTAL':<12} {qtd_geral:<12} R${total_geral:<14.2f}")
            
        except ValueError:
            print("❌ Formato de data inválido!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def relatorio_estoque(self):
        """Relatório de estoque atual"""
        self.limpar_tela()
        self.exibir_header("RELATÓRIO DE ESTOQUE")
        
        produtos = self.produto_manager.listar_todos()
        
        if not produtos:
            print("❌ Nenhum produto cadastrado!")
        else:
            print(f"{'Nome':<30} {'Categoria':<20} {'Estoque':<10} {'Valor Total':<15}")
            print("-" * 75)
            
            valor_total_estoque = 0
            
            for produto in produtos:
                categoria = produto[12] if produto[12] else "Sem categoria"
                valor_total_produto = produto[3] * produto[4]  # preço * estoque
                valor_total_estoque += valor_total_produto
                
                print(f"{produto[1][:29]:<30} {categoria[:19]:<20} {produto[4]:<10} R${valor_total_produto:<14.2f}")
            
            print("-" * 75)
            print(f"{'VALOR TOTAL DO ESTOQUE':<60} R${valor_total_estoque:<14.2f}")
        
        self.pausar()
    
    def relatorio_clientes(self):
        """Relatório de clientes cadastrados"""
        self.limpar_tela()
        self.exibir_header("CLIENTES CADASTRADOS")
        
        clientes = self.cliente_manager.listar_todos()
        
        if not clientes:
            print("❌ Nenhum cliente cadastrado!")
        else:
            print(f"Total de clientes: {len(clientes)}")
            print(f"\n{'Nome':<30} {'Telefone':<15} {'Email':<25} {'Cidade':<20}")
            print("-" * 90)
            
            for cliente in clientes:
                telefone = cliente[3] if cliente[3] else ""
                email = cliente[4] if cliente[4] else ""
                cidade = cliente[6] if cliente[6] else ""
                print(f"{cliente[1][:29]:<30} {telefone:<15} {email[:24]:<25} {cidade[:19]:<20}")
        
        self.pausar()
    
    def relatorio_pets_especie(self):
        """Relatório de pets por espécie"""
        self.limpar_tela()
        self.exibir_header("PETS POR ESPÉCIE")
        
        try:
            pets_por_especie = self.db.execute_query('''
                SELECT especie, COUNT(*) as quantidade
                FROM pets 
                GROUP BY LOWER(especie)
                ORDER BY quantidade DESC
            ''')
            
            if not pets_por_especie:
                print("❌ Nenhum pet cadastrado!")
            else:
                print(f"{'Espécie':<20} {'Quantidade':<12}")
                print("-" * 32)
                
                for item in pets_por_especie:
                    print(f"{item[0].title():<20} {item[1]:<12}")
                
                total_pets = sum(item[1] for item in pets_por_especie)
                print("-" * 32)
                print(f"{'TOTAL':<20} {total_pets:<12}")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        self.pausar()
    
    def relatorio_agendamentos_dia(self):
        """Relatório de agendamentos do dia"""
        self.limpar_tela()
        self.exibir_header("AGENDAMENTOS DE HOJE")
        
        hoje = date.today().strftime("%Y-%m-%d")
        agendamentos = self.agendamento_manager.listar_agendamentos(hoje, hoje)
        
        if not agendamentos:
            print("❌ Nenhum agendamento para hoje!")
        else:
            print(f"Total de agendamentos hoje: {len(agendamentos)}")
            print(f"\n{'Hora':<8} {'Cliente':<25} {'Pet':<15} {'Serviço':<20} {'Status':<12}")
            print("-" * 80)
            
            for agendamento in agendamentos:
                # Extrair hora
                hora = agendamento[4][11:16] if len(agendamento[4]) > 16 else agendamento[4][-5:]
                cliente_nome = agendamento[8][:24] if agendamento[8] else ""
                pet_nome = agendamento[9][:14] if agendamento[9] else ""
                servico_nome = agendamento[10][:19] if agendamento[10] else ""
                status = agendamento[5][:11] if agendamento[5] else ""
                
                print(f"{hora:<8} {cliente_nome:<25} {pet_nome:<15} {servico_nome:<20} {status:<12}")
        
        self.pausar()

def main():
    """Função principal"""
    try:
        sistema = PetShopSystem()
        sistema.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print("Por favor, contate o suporte técnico.")

if __name__ == "__main__":
    main() 