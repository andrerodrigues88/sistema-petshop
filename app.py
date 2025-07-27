#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sqlite3

# Importar nossos modelos
from database import DatabaseManager
from models import Produto, Cliente, Pet, Venda, Agendamento, Categoria

# Configuração da página
st.set_page_config(
    page_title="🐾 Sistema PetShop",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar o visual
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        padding: 0.5rem;
        border-radius: 0.25rem;
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    .error-message {
        padding: 0.5rem;
        border-radius: 0.25rem;
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar managers
@st.cache_resource
def init_database():
    db = DatabaseManager()
    
    # Configurar dados de demonstração automaticamente
    try:
        from setup_demo import setup_demo_data
        setup_demo_data()
    except Exception as e:
        print(f"Aviso: Não foi possível configurar dados de demonstração: {e}")
    
    return {
        'db': db,
        'produto_manager': Produto(db),
        'cliente_manager': Cliente(db),
        'pet_manager': Pet(db),
        'venda_manager': Venda(db),
        'agendamento_manager': Agendamento(db),
        'categoria_manager': Categoria(db)
    }

managers = init_database()

def main():
    # Aviso de demonstração
    st.info("🎯 **DEMONSTRAÇÃO GRATUITA** - Este é um sistema completo funcionando com dados de exemplo. Entre em contato para adquirir sua licença!", icon="ℹ️")
    
    # Header principal
    st.markdown('<h1 class="main-header">🐾 Sistema PetShop Profissional</h1>', unsafe_allow_html=True)
    
    # Sidebar para navegação
    st.sidebar.title("📋 Menu Principal")
    
    # Opções do menu
    opcoes_menu = {
        "🏠 Dashboard": "dashboard",
        "📦 Gestão de Estoque": "estoque", 
        "👥 Gestão de Clientes": "clientes",
        "🐕 Gestão de Pets": "pets",
        "🛒 Sistema de Vendas": "vendas",
        "📅 Agendamentos": "agendamentos",
        "📊 Relatórios": "relatorios"
    }
    
    opcao_selecionada = st.sidebar.selectbox(
        "Escolha uma opção:",
        list(opcoes_menu.keys()),
        index=0
    )
    
    # Roteamento de páginas
    pagina = opcoes_menu[opcao_selecionada]
    
    if pagina == "dashboard":
        mostrar_dashboard()
    elif pagina == "estoque":
        mostrar_gestao_estoque()
    elif pagina == "clientes":
        mostrar_gestao_clientes()
    elif pagina == "pets":
        mostrar_gestao_pets()
    elif pagina == "vendas":
        mostrar_sistema_vendas()
    elif pagina == "agendamentos":
        mostrar_agendamentos()
    elif pagina == "relatorios":
        mostrar_relatorios()

def mostrar_dashboard():
    """Dashboard principal com estatísticas"""
    st.header("🏠 Dashboard - Visão Geral")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Buscar dados para métricas
        produtos = managers['produto_manager'].listar_todos()
        clientes = managers['cliente_manager'].listar_todos()
        pets = managers['pet_manager'].listar_todos()
        
        # Vendas do mês
        vendas_mes = managers['db'].execute_query('''
            SELECT COUNT(*), COALESCE(SUM(total), 0)
            FROM vendas 
            WHERE strftime('%Y-%m', data_venda) = strftime('%Y-%m', 'now')
        ''')
        
        total_vendas_mes = vendas_mes[0][0] if vendas_mes else 0
        valor_vendas_mes = vendas_mes[0][1] if vendas_mes else 0
        
        # Produtos com estoque baixo
        produtos_estoque_baixo = len(managers['produto_manager'].produtos_estoque_baixo())
        
        with col1:
            st.metric("📦 Total de Produtos", len(produtos))
        
        with col2:
            st.metric("👥 Total de Clientes", len(clientes))
        
        with col3:
            st.metric("🐕 Total de Pets", len(pets))
        
        with col4:
            st.metric("💰 Vendas do Mês", f"R$ {valor_vendas_mes:.2f}")
        
        # Segunda linha de métricas
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric("🛒 Vendas Realizadas", total_vendas_mes)
        
        with col6:
            if produtos_estoque_baixo > 0:
                st.metric("⚠️ Estoque Baixo", produtos_estoque_baixo, delta=f"-{produtos_estoque_baixo}")
            else:
                st.metric("✅ Estoque OK", "0")
        
        with col7:
            # Agendamentos hoje
            hoje = date.today().strftime("%Y-%m-%d")
            agendamentos_hoje = managers['agendamento_manager'].listar_agendamentos(hoje, hoje)
            st.metric("📅 Agendamentos Hoje", len(agendamentos_hoje))
        
        with col8:
            # Valor total do estoque
            valor_estoque = sum(p[3] * p[4] for p in produtos)  # preço * estoque
            st.metric("💎 Valor do Estoque", f"R$ {valor_estoque:.2f}")
        
        # Gráficos
        st.markdown("---")
        
        # Gráfico de vendas dos últimos 30 dias
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.subheader("📈 Vendas dos Últimos 30 Dias")
            
            vendas_30_dias = managers['db'].execute_query('''
                SELECT DATE(data_venda) as data, COUNT(*) as qtd, SUM(total) as total
                FROM vendas 
                WHERE data_venda >= date('now', '-30 days')
                GROUP BY DATE(data_venda)
                ORDER BY data
            ''')
            
            if vendas_30_dias:
                df_vendas = pd.DataFrame(vendas_30_dias, columns=['Data', 'Quantidade', 'Total'])
                df_vendas['Data'] = pd.to_datetime(df_vendas['Data'])
                
                fig = px.line(df_vendas, x='Data', y='Total', 
                             title='Faturamento Diário',
                             labels={'Total': 'Valor (R$)', 'Data': 'Data'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma venda nos últimos 30 dias")
        
        with col_graf2:
            st.subheader("🐕 Pets por Espécie")
            
            pets_especies = managers['db'].execute_query('''
                SELECT especie, COUNT(*) as quantidade
                FROM pets 
                GROUP BY LOWER(especie)
                ORDER BY quantidade DESC
            ''')
            
            if pets_especies:
                df_especies = pd.DataFrame(pets_especies, columns=['Espécie', 'Quantidade'])
                
                fig = px.pie(df_especies, values='Quantidade', names='Espécie',
                           title='Distribuição de Pets por Espécie')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum pet cadastrado")
        
        # Alertas importantes
        st.markdown("---")
        st.subheader("🚨 Alertas Importantes")
        
        if produtos_estoque_baixo > 0:
            st.warning(f"⚠️ {produtos_estoque_baixo} produto(s) com estoque baixo!")
            
            # Mostrar produtos com estoque baixo
            produtos_baixo = managers['produto_manager'].produtos_estoque_baixo()
            df_baixo = pd.DataFrame(produtos_baixo, columns=[
                'ID', 'Nome', 'Categoria_ID', 'Preço', 'Estoque Atual', 
                'Estoque Mínimo', 'Código', 'Descrição', 'Marca', 'Peso', 
                'Unidade', 'Created', 'Updated', 'Categoria'
            ])
            st.dataframe(df_baixo[['Nome', 'Estoque Atual', 'Estoque Mínimo', 'Categoria']], 
                        use_container_width=True)
        else:
            st.success("✅ Todos os produtos estão com estoque adequado!")
        
        # Agendamentos de hoje
        if agendamentos_hoje:
            st.info(f"📅 Você tem {len(agendamentos_hoje)} agendamento(s) para hoje!")
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")

def mostrar_gestao_estoque():
    """Página de gestão de estoque"""
    st.header("📦 Gestão de Estoque")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar Produtos", "➕ Adicionar Produto", "📈 Atualizar Estoque", "🏷️ Categorias"])
    
    with tab1:
        st.subheader("Lista de Produtos")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_nome = st.text_input("🔍 Filtrar por nome:")
        with col2:
            categorias = managers['categoria_manager'].listar_todas()
            categoria_opcoes = ["Todas"] + [cat[1] for cat in categorias]
            filtro_categoria = st.selectbox("🏷️ Filtrar por categoria:", categoria_opcoes)
        
        # Buscar produtos
        if filtro_nome:
            produtos = managers['produto_manager'].buscar_por_nome(filtro_nome)
        else:
            produtos = managers['produto_manager'].listar_todos()
        
        if produtos:
            # Converter para DataFrame
            df = pd.DataFrame(produtos, columns=[
                'ID', 'Nome', 'Categoria_ID', 'Preço', 'Estoque Atual', 
                'Estoque Mínimo', 'Código', 'Descrição', 'Marca', 'Peso', 
                'Unidade', 'Created', 'Updated', 'Categoria'
            ])
            
            # Filtrar por categoria se selecionada
            if filtro_categoria != "Todas":
                df = df[df['Categoria'] == filtro_categoria]
            
            # Destacar produtos com estoque baixo
            def highlight_estoque_baixo(row):
                if row['Estoque Atual'] <= row['Estoque Mínimo']:
                    return ['background-color: #ffebee'] * len(row)
                return [''] * len(row)
            
            # Mostrar tabela
            st.dataframe(
                df[['ID', 'Nome', 'Categoria', 'Preço', 'Estoque Atual', 'Estoque Mínimo']].style.apply(highlight_estoque_baixo, axis=1),
                use_container_width=True
            )
        else:
            st.info("Nenhum produto encontrado")
    
    with tab2:
        st.subheader("Adicionar Novo Produto")
        
        with st.form("form_produto"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome do Produto *", placeholder="Ex: Ração Premium Cães")
                
                categorias = managers['categoria_manager'].listar_todas()
                categoria_opcoes = {cat[1]: cat[0] for cat in categorias}
                categoria_selecionada = st.selectbox("Categoria *", list(categoria_opcoes.keys()))
                
                preco = st.number_input("Preço (R$) *", min_value=0.01, step=0.01, format="%.2f")
                estoque_atual = st.number_input("Estoque Inicial", min_value=0, value=0)
                estoque_minimo = st.number_input("Estoque Mínimo", min_value=0, value=5)
            
            with col2:
                codigo_barras = st.text_input("Código de Barras", placeholder="Opcional")
                marca = st.text_input("Marca", placeholder="Ex: Royal Canin")
                peso = st.number_input("Peso/Volume", min_value=0.0, step=0.1, format="%.1f")
                unidade_medida = st.selectbox("Unidade", ["un", "kg", "g", "ml", "l"])
                descricao = st.text_area("Descrição", placeholder="Descrição detalhada do produto")
            
            submitted = st.form_submit_button("✅ Adicionar Produto", type="primary")
            
            if submitted:
                if nome and categoria_selecionada and preco > 0:
                    try:
                        categoria_id = categoria_opcoes[categoria_selecionada]
                        codigo = codigo_barras if codigo_barras else None
                        
                        produto_id = managers['produto_manager'].adicionar(
                            nome, categoria_id, preco, estoque_atual, estoque_minimo,
                            codigo, descricao, marca, peso if peso > 0 else None, unidade_medida
                        )
                        
                        st.success(f"✅ Produto '{nome}' adicionado com sucesso! ID: {produto_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar produto: {e}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios!")
    
    with tab3:
        st.subheader("Atualizar Estoque")
        
        # Buscar produto
        produtos = managers['produto_manager'].listar_todos()
        if produtos:
            produto_opcoes = {f"{p[0]} - {p[1]}": p[0] for p in produtos}
            produto_selecionado = st.selectbox("Selecione o produto:", list(produto_opcoes.keys()))
            
            if produto_selecionado:
                produto_id = produto_opcoes[produto_selecionado]
                produto = managers['produto_manager'].buscar_por_id(produto_id)
                
                if produto:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"**Produto:** {produto[1]}")
                        st.info(f"**Estoque Atual:** {produto[4]}")
                    
                    with col2:
                        nova_quantidade = st.number_input("Nova Quantidade:", min_value=0, value=produto[4])
                        motivo = st.text_input("Motivo da Alteração:", value="Ajuste manual")
                    
                    if st.button("🔄 Atualizar Estoque", type="primary"):
                        try:
                            if managers['produto_manager'].atualizar_estoque(produto_id, nova_quantidade, motivo):
                                st.success("✅ Estoque atualizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao atualizar estoque!")
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
        else:
            st.info("Nenhum produto cadastrado")
    
    with tab4:
        st.subheader("Gerenciar Categorias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Categorias Existentes:**")
            categorias = managers['categoria_manager'].listar_todas()
            
            if categorias:
                df_cat = pd.DataFrame(categorias, columns=['ID', 'Nome', 'Descrição', 'Criado em'])
                st.dataframe(df_cat[['ID', 'Nome', 'Descrição']], use_container_width=True)
            else:
                st.info("Nenhuma categoria cadastrada")
        
        with col2:
            st.write("**Adicionar Nova Categoria:**")
            
            with st.form("form_categoria"):
                nome_cat = st.text_input("Nome da Categoria *")
                desc_cat = st.text_area("Descrição")
                
                if st.form_submit_button("➕ Adicionar Categoria"):
                    if nome_cat:
                        try:
                            cat_id = managers['categoria_manager'].adicionar(nome_cat, desc_cat)
                            st.success(f"✅ Categoria '{nome_cat}' adicionada! ID: {cat_id}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao adicionar categoria: {e}")
                    else:
                        st.error("❌ Nome da categoria é obrigatório!")

def mostrar_gestao_clientes():
    """Página de gestão de clientes"""
    st.header("👥 Gestão de Clientes")
    
    tab1, tab2, tab3 = st.tabs(["📋 Listar Clientes", "➕ Adicionar Cliente", "✏️ Editar Cliente"])
    
    with tab1:
        st.subheader("Lista de Clientes")
        
        # Filtro
        filtro_nome = st.text_input("🔍 Filtrar por nome:")
        
        # Buscar clientes
        if filtro_nome:
            clientes = managers['cliente_manager'].buscar_por_nome(filtro_nome)
        else:
            clientes = managers['cliente_manager'].listar_todos()
        
        if clientes:
            df = pd.DataFrame(clientes, columns=[
                'ID', 'Nome', 'CPF', 'Telefone', 'Email', 'Endereço', 'Cidade', 'CEP', 'Criado em'
            ])
            
            st.dataframe(
                df[['ID', 'Nome', 'Telefone', 'Email', 'Cidade']],
                use_container_width=True
            )
            
            # Estatísticas
            st.metric("Total de Clientes", len(clientes))
        else:
            st.info("Nenhum cliente encontrado")
    
    with tab2:
        st.subheader("Adicionar Novo Cliente")
        
        with st.form("form_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Ex: João Silva Santos")
                cpf = st.text_input("CPF", placeholder="000.000.000-00")
                telefone = st.text_input("Telefone *", placeholder="(11) 99999-9999")
                email = st.text_input("Email", placeholder="cliente@email.com")
            
            with col2:
                endereco = st.text_input("Endereço", placeholder="Rua, número")
                cidade = st.text_input("Cidade", placeholder="São Paulo")
                cep = st.text_input("CEP", placeholder="00000-000")
            
            submitted = st.form_submit_button("✅ Adicionar Cliente", type="primary")
            
            if submitted:
                if nome:
                    try:
                        cliente_id = managers['cliente_manager'].adicionar(
                            nome, cpf if cpf else None, telefone if telefone else None,
                            email if email else None, endereco if endereco else None,
                            cidade if cidade else None, cep if cep else None
                        )
                        
                        st.success(f"✅ Cliente '{nome}' adicionado com sucesso! ID: {cliente_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar cliente: {e}")
                else:
                    st.error("❌ Nome é obrigatório!")
    
    with tab3:
        st.subheader("Editar Cliente")
        
        clientes = managers['cliente_manager'].listar_todos()
        if clientes:
            cliente_opcoes = {f"{c[0]} - {c[1]}": c[0] for c in clientes}
            cliente_selecionado = st.selectbox("Selecione o cliente:", list(cliente_opcoes.keys()))
            
            if cliente_selecionado:
                cliente_id = cliente_opcoes[cliente_selecionado]
                cliente = managers['cliente_manager'].buscar_por_id(cliente_id)
                
                if cliente:
                    with st.form("form_editar_cliente"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nome = st.text_input("Nome Completo *", value=cliente[1])
                            cpf = st.text_input("CPF", value=cliente[2] if cliente[2] else "")
                            telefone = st.text_input("Telefone", value=cliente[3] if cliente[3] else "")
                            email = st.text_input("Email", value=cliente[4] if cliente[4] else "")
                        
                        with col2:
                            endereco = st.text_input("Endereço", value=cliente[5] if cliente[5] else "")
                            cidade = st.text_input("Cidade", value=cliente[6] if cliente[6] else "")
                            cep = st.text_input("CEP", value=cliente[7] if cliente[7] else "")
                        
                        if st.form_submit_button("💾 Salvar Alterações", type="primary"):
                            if nome:
                                try:
                                    if managers['cliente_manager'].atualizar(
                                        cliente_id, nome, cpf if cpf else None,
                                        telefone if telefone else None, email if email else None,
                                        endereco if endereco else None, cidade if cidade else None,
                                        cep if cep else None
                                    ):
                                        st.success("✅ Cliente atualizado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao atualizar cliente!")
                                except Exception as e:
                                    st.error(f"❌ Erro: {e}")
                            else:
                                st.error("❌ Nome é obrigatório!")
        else:
            st.info("Nenhum cliente cadastrado")

def mostrar_gestao_pets():
    """Página de gestão de pets"""
    st.header("🐕 Gestão de Pets")
    
    tab1, tab2 = st.tabs(["📋 Listar Pets", "➕ Adicionar Pet"])
    
    with tab1:
        st.subheader("Lista de Pets")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_nome = st.text_input("🔍 Filtrar por nome do pet:")
        with col2:
            especies = managers['db'].execute_query('SELECT DISTINCT especie FROM pets ORDER BY especie')
            especie_opcoes = ["Todas"] + [e[0] for e in especies] if especies else ["Todas"]
            filtro_especie = st.selectbox("🐕 Filtrar por espécie:", especie_opcoes)
        
        # Buscar pets
        if filtro_nome:
            pets = managers['pet_manager'].buscar_por_nome(filtro_nome)
        else:
            pets = managers['pet_manager'].listar_todos()
        
        if pets:
            df = pd.DataFrame(pets, columns=[
                'ID', 'Nome', 'Cliente_ID', 'Espécie', 'Raça', 'Idade', 
                'Peso', 'Cor', 'Observações', 'Criado em', 'Cliente Nome', 'Cliente Telefone'
            ])
            
            # Filtrar por espécie
            if filtro_especie != "Todas":
                df = df[df['Espécie'].str.lower() == filtro_especie.lower()]
            
            st.dataframe(
                df[['ID', 'Nome', 'Espécie', 'Raça', 'Idade', 'Peso', 'Cliente Nome']],
                use_container_width=True
            )
            
            # Estatísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Pets", len(df))
            with col2:
                idade_media = df['Idade'].dropna().mean()
                st.metric("Idade Média", f"{idade_media:.1f} anos" if not pd.isna(idade_media) else "N/A")
            with col3:
                peso_medio = df['Peso'].dropna().mean()
                st.metric("Peso Médio", f"{peso_medio:.1f} kg" if not pd.isna(peso_medio) else "N/A")
        else:
            st.info("Nenhum pet encontrado")
    
    with tab2:
        st.subheader("Adicionar Novo Pet")
        
        # Primeiro, selecionar cliente
        clientes = managers['cliente_manager'].listar_todos()
        if not clientes:
            st.warning("⚠️ É necessário cadastrar um cliente antes de adicionar um pet!")
            return
        
        with st.form("form_pet"):
            # Seleção de cliente
            cliente_opcoes = {f"{c[1]} - {c[3] if c[3] else 'Sem telefone'}": c[0] for c in clientes}
            cliente_selecionado = st.selectbox("Cliente *", list(cliente_opcoes.keys()))
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome do Pet *", placeholder="Ex: Rex")
                especie = st.selectbox("Espécie *", ["Cão", "Gato", "Pássaro", "Peixe", "Hamster", "Coelho", "Outro"])
                raca = st.text_input("Raça", placeholder="Ex: Golden Retriever")
                idade = st.number_input("Idade (anos)", min_value=0, max_value=30, value=0)
            
            with col2:
                peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.1f")
                cor = st.text_input("Cor", placeholder="Ex: Dourado")
                observacoes = st.text_area("Observações", placeholder="Informações importantes sobre o pet")
            
            submitted = st.form_submit_button("✅ Adicionar Pet", type="primary")
            
            if submitted:
                if nome and especie and cliente_selecionado:
                    try:
                        cliente_id = cliente_opcoes[cliente_selecionado]
                        
                        pet_id = managers['pet_manager'].adicionar(
                            nome, cliente_id, especie, raca if raca else None,
                            idade if idade > 0 else None, peso if peso > 0 else None,
                            cor if cor else None, observacoes if observacoes else None
                        )
                        
                        st.success(f"✅ Pet '{nome}' adicionado com sucesso! ID: {pet_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar pet: {e}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios!")

def mostrar_sistema_vendas():
    """Sistema de vendas web"""
    st.header("🛒 Sistema de Vendas")
    
    tab1, tab2, tab3 = st.tabs(["🛒 Nova Venda", "📋 Histórico de Vendas", "🔍 Buscar Venda"])
    
    with tab1:
        nova_venda_web()
    
    with tab2:
        historico_vendas_web()
    
    with tab3:
        buscar_venda_web()

def nova_venda_web():
    """Interface para nova venda"""
    st.subheader("🛒 Nova Venda")
    
    # Inicializar session state para carrinho
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []
    if 'venda_atual' not in st.session_state:
        st.session_state.venda_atual = None
    
    # Seleção de cliente (opcional)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        clientes = managers['cliente_manager'].listar_todos()
        cliente_opcoes = {"Venda sem cliente": None}
        cliente_opcoes.update({f"{c[1]} - {c[3] if c[3] else 'Sem telefone'}": c[0] for c in clientes})
        
        cliente_selecionado = st.selectbox("👤 Cliente:", list(cliente_opcoes.keys()))
        cliente_id = cliente_opcoes[cliente_selecionado]
    
    with col2:
        forma_pagamento = st.selectbox("💳 Forma de Pagamento:", 
                                     ["Dinheiro", "Cartão de Débito", "Cartão de Crédito", "PIX"])
    
    # Adicionar produtos ao carrinho
    st.markdown("---")
    st.subheader("📦 Adicionar Produtos")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        produtos = managers['produto_manager'].listar_todos()
        if produtos:
            produto_opcoes = {f"{p[1]} - R${p[3]:.2f} (Estoque: {p[4]})": p for p in produtos if p[4] > 0}
            
            if produto_opcoes:
                produto_selecionado = st.selectbox("Produto:", list(produto_opcoes.keys()))
                produto_dados = produto_opcoes[produto_selecionado]
            else:
                st.warning("⚠️ Nenhum produto com estoque disponível!")
                return
        else:
            st.warning("⚠️ Nenhum produto cadastrado!")
            return
    
    with col2:
        quantidade = st.number_input("Qtd:", min_value=1, max_value=produto_dados[4], value=1)
    
    with col3:
        preco_unitario = st.number_input("Preço Unit.:", value=float(produto_dados[3]), step=0.01, format="%.2f")
    
    with col4:
        if st.button("➕ Adicionar", type="primary"):
            if quantidade <= produto_dados[4]:
                item = {
                    'produto_id': produto_dados[0],
                    'nome': produto_dados[1],
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario,
                    'subtotal': quantidade * preco_unitario
                }
                st.session_state.carrinho.append(item)
                st.success(f"✅ {quantidade}x {produto_dados[1]} adicionado ao carrinho!")
                st.rerun()
            else:
                st.error(f"❌ Estoque insuficiente! Disponível: {produto_dados[4]}")
    
    # Mostrar carrinho
    if st.session_state.carrinho:
        st.markdown("---")
        st.subheader("🛒 Carrinho de Compras")
        
        total_carrinho = 0
        for i, item in enumerate(st.session_state.carrinho):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(item['nome'])
            with col2:
                st.write(f"{item['quantidade']}x")
            with col3:
                st.write(f"R${item['preco_unitario']:.2f}")
            with col4:
                st.write(f"R${item['subtotal']:.2f}")
            with col5:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.carrinho.pop(i)
                    st.rerun()
            
            total_carrinho += item['subtotal']
        
        # Totais e desconto
        col1, col2, col3 = st.columns(3)
        
        with col1:
            desconto = st.number_input("💰 Desconto (R$):", min_value=0.0, step=0.01, format="%.2f")
        
        with col2:
            st.metric("🛒 Subtotal:", f"R$ {total_carrinho:.2f}")
        
        with col3:
            total_final = total_carrinho - desconto
            st.metric("💰 Total Final:", f"R$ {total_final:.2f}")
        
        # Finalizar venda
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Finalizar Venda", type="primary", use_container_width=True):
                try:
                    # Criar venda
                    venda_id = managers['venda_manager'].criar_venda(
                        cliente_id, desconto, forma_pagamento
                    )
                    
                    # Adicionar itens
                    for item in st.session_state.carrinho:
                        managers['venda_manager'].adicionar_item(
                            venda_id, item['produto_id'], item['quantidade'], item['preco_unitario']
                        )
                    
                    # Finalizar e atualizar estoque
                    managers['venda_manager'].finalizar_venda(venda_id)
                    
                    st.success(f"🎉 Venda #{venda_id} finalizada com sucesso!")
                    st.session_state.carrinho = []
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao finalizar venda: {e}")
        
        with col2:
            if st.button("🗑️ Limpar Carrinho", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()

def historico_vendas_web():
    """Histórico de vendas"""
    st.subheader("📋 Histórico de Vendas")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_inicio = st.date_input("Data Início:", value=date.today() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("Data Fim:", value=date.today())
    
    with col3:
        limite = st.number_input("Limite de registros:", min_value=10, max_value=500, value=50)
    
    # Buscar vendas
    vendas = managers['db'].execute_query('''
        SELECT v.*, c.nome as cliente_nome
        FROM vendas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        WHERE DATE(v.data_venda) BETWEEN ? AND ?
        ORDER BY v.data_venda DESC
        LIMIT ?
    ''', (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d'), limite))
    
    if vendas:
        df = pd.DataFrame(vendas, columns=[
            'ID', 'Cliente_ID', 'Total', 'Desconto', 'Forma_Pagamento', 
            'Data_Venda', 'Observações', 'Cliente_Nome'
        ])
        
        # Formatar data
        df['Data'] = pd.to_datetime(df['Data_Venda']).dt.strftime('%d/%m/%Y %H:%M')
        df['Cliente'] = df['Cliente_Nome'].fillna('Sem cliente')
        
        # Mostrar tabela
        st.dataframe(
            df[['ID', 'Data', 'Cliente', 'Total', 'Forma_Pagamento']],
            use_container_width=True
        )
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Vendas", len(df))
        
        with col2:
            total_faturamento = df['Total'].sum()
            st.metric("Faturamento Total", f"R$ {total_faturamento:.2f}")
        
        with col3:
            ticket_medio = df['Total'].mean()
            st.metric("Ticket Médio", f"R$ {ticket_medio:.2f}")
        
        with col4:
            total_desconto = df['Desconto'].sum()
            st.metric("Total Descontos", f"R$ {total_desconto:.2f}")
    else:
        st.info("Nenhuma venda encontrada no período selecionado")

def buscar_venda_web():
    """Buscar venda específica"""
    st.subheader("🔍 Buscar Venda")
    
    venda_id = st.number_input("ID da Venda:", min_value=1, step=1)
    
    if st.button("🔍 Buscar"):
        venda_info = managers['venda_manager'].buscar_venda(venda_id)
        
        if venda_info:
            venda = venda_info['venda']
            itens = venda_info['itens']
            
            # Informações da venda
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**Venda #{venda[0]}**")
                st.write(f"**Data:** {venda[5]}")
                st.write(f"**Cliente:** {venda[7] if venda[7] else 'Sem cliente'}")
                st.write(f"**Forma de Pagamento:** {venda[4]}")
            
            with col2:
                st.write(f"**Desconto:** R$ {venda[2]:.2f}")
                st.write(f"**Total:** R$ {venda[1]:.2f}")
            
            # Itens da venda
            if itens:
                st.subheader("Itens da Venda")
                
                df_itens = pd.DataFrame(itens, columns=[
                    'ID', 'Venda_ID', 'Produto_ID', 'Quantidade', 
                    'Preço_Unitário', 'Subtotal', 'Produto_Nome'
                ])
                
                st.dataframe(
                    df_itens[['Produto_Nome', 'Quantidade', 'Preço_Unitário', 'Subtotal']],
                    use_container_width=True
                )
        else:
            st.error("❌ Venda não encontrada!")

def mostrar_agendamentos():
    """Página de agendamentos"""
    st.header("📅 Agendamentos e Serviços")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Novo Agendamento", "📋 Lista de Agendamentos", "✅ Atualizar Status", "🛠️ Tipos de Serviços"])
    
    with tab1:
        novo_agendamento_web()
    
    with tab2:
        lista_agendamentos_web()
    
    with tab3:
        atualizar_status_web()
    
    with tab4:
        tipos_servicos_web()

def novo_agendamento_web():
    """Interface para novo agendamento"""
    st.subheader("📅 Novo Agendamento")
    
    # Verificar se há clientes e pets
    clientes = managers['cliente_manager'].listar_todos()
    if not clientes:
        st.warning("⚠️ É necessário cadastrar clientes antes de criar agendamentos!")
        return
    
    with st.form("form_agendamento"):
        # Seleção de cliente
        cliente_opcoes = {f"{c[1]} - {c[3] if c[3] else 'Sem telefone'}": c[0] for c in clientes}
        cliente_selecionado = st.selectbox("👤 Cliente *", list(cliente_opcoes.keys()))
        cliente_id = cliente_opcoes[cliente_selecionado]
        
        # Buscar pets do cliente
        pets_cliente = managers['pet_manager'].listar_por_cliente(cliente_id)
        
        if not pets_cliente:
            st.warning(f"⚠️ Este cliente não possui pets cadastrados!")
            st.form_submit_button("❌ Cancelar")
            return
        
        # Seleção de pet
        pet_opcoes = {f"{p[1]} ({p[3]})": p[0] for p in pets_cliente}
        pet_selecionado = st.selectbox("🐕 Pet *", list(pet_opcoes.keys()))
        pet_id = pet_opcoes[pet_selecionado]
        
        # Seleção de serviço
        servicos = managers['agendamento_manager'].listar_tipos_servicos()
        servico_opcoes = {f"{s[1]} - R${s[2]:.2f}": s[0] for s in servicos}
        servico_selecionado = st.selectbox("🛠️ Serviço *", list(servico_opcoes.keys()))
        tipo_servico_id = servico_opcoes[servico_selecionado]
        
        # Data e hora
        col1, col2 = st.columns(2)
        
        with col1:
            data_agendamento = st.date_input("📅 Data *", min_value=date.today())
        
        with col2:
            hora_agendamento = st.time_input("🕐 Hora *", value=datetime.now().time())
        
        # Observações
        observacoes = st.text_area("📝 Observações", placeholder="Observações sobre o agendamento")
        
        submitted = st.form_submit_button("✅ Criar Agendamento", type="primary")
        
        if submitted:
            try:
                # Combinar data e hora
                data_hora = datetime.combine(data_agendamento, hora_agendamento)
                
                agendamento_id = managers['agendamento_manager'].criar_agendamento(
                    cliente_id, pet_id, tipo_servico_id, data_hora, observacoes if observacoes else None
                )
                
                st.success(f"✅ Agendamento #{agendamento_id} criado com sucesso!")
                st.success(f"📅 Data: {data_hora.strftime('%d/%m/%Y às %H:%M')}")
                
            except Exception as e:
                st.error(f"❌ Erro ao criar agendamento: {e}")

def lista_agendamentos_web():
    """Lista de agendamentos"""
    st.subheader("📋 Lista de Agendamentos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        opcoes_periodo = {
            "Hoje": (date.today(), date.today()),
            "Próximos 7 dias": (date.today(), date.today() + timedelta(days=7)),
            "Próximos 30 dias": (date.today(), date.today() + timedelta(days=30)),
            "Todos": (None, None)
        }
        periodo_selecionado = st.selectbox("📅 Período:", list(opcoes_periodo.keys()))
        data_inicio, data_fim = opcoes_periodo[periodo_selecionado]
    
    with col2:
        status_opcoes = ["Todos", "agendado", "confirmado", "em_andamento", "concluido", "cancelado", "nao_compareceu"]
        status_filtro = st.selectbox("📊 Status:", status_opcoes)
    
    with col3:
        if st.button("🔄 Atualizar"):
            st.rerun()
    
    # Buscar agendamentos
    if data_inicio and data_fim:
        agendamentos = managers['agendamento_manager'].listar_agendamentos(
            data_inicio.strftime('%Y-%m-%d'),
            data_fim.strftime('%Y-%m-%d')
        )
    else:
        agendamentos = managers['agendamento_manager'].listar_agendamentos()
    
    if agendamentos:
        df = pd.DataFrame(agendamentos, columns=[
            'ID', 'Cliente_ID', 'Pet_ID', 'Tipo_Servico_ID', 'Data_Agendamento',
            'Status', 'Preço', 'Observações', 'Criado_em', 'Cliente_Nome', 'Pet_Nome', 'Servico_Nome'
        ])
        
        # Filtrar por status
        if status_filtro != "Todos":
            df = df[df['Status'] == status_filtro]
        
        # Formatar data
        df['Data_Hora'] = pd.to_datetime(df['Data_Agendamento']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Função para colorir status
        def color_status(val):
            colors = {
                'agendado': 'background-color: #e3f2fd',
                'confirmado': 'background-color: #e8f5e8', 
                'em_andamento': 'background-color: #fff3e0',
                'concluido': 'background-color: #e8f5e8',
                'cancelado': 'background-color: #ffebee',
                'nao_compareceu': 'background-color: #fce4ec'
            }
            return colors.get(val, '')
        
        # Mostrar tabela
        st.dataframe(
            df[['ID', 'Data_Hora', 'Cliente_Nome', 'Pet_Nome', 'Servico_Nome', 'Status', 'Preço']].style.applymap(
                color_status, subset=['Status']
            ),
            use_container_width=True
        )
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Agendamentos", len(df))
        
        with col2:
            agendados_hoje = len(df[df['Data_Agendamento'].str.contains(date.today().strftime('%Y-%m-%d'))])
            st.metric("Agendamentos Hoje", agendados_hoje)
        
        with col3:
            receita_total = df['Preço'].sum()
            st.metric("Receita Total", f"R$ {receita_total:.2f}")
        
        with col4:
            concluidos = len(df[df['Status'] == 'concluido'])
            st.metric("Concluídos", concluidos)
    else:
        st.info("Nenhum agendamento encontrado")

def atualizar_status_web():
    """Atualizar status de agendamento"""
    st.subheader("✅ Atualizar Status do Agendamento")
    
    # Buscar agendamentos pendentes
    agendamentos = managers['db'].execute_query('''
        SELECT a.id, a.data_agendamento, a.status, c.nome as cliente_nome, 
               p.nome as pet_nome, ts.nome as servico_nome
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN pets p ON a.pet_id = p.id
        JOIN tipos_servicos ts ON a.tipo_servico_id = ts.id
        WHERE a.status != 'concluido' AND a.status != 'cancelado'
        ORDER BY a.data_agendamento
    ''')
    
    if agendamentos:
        # Seleção de agendamento
        agendamento_opcoes = {
            f"#{a[0]} - {a[3]} - {a[4]} - {a[1][:16]}": a[0] 
            for a in agendamentos
        }
        
        agendamento_selecionado = st.selectbox(
            "Selecione o agendamento:",
            list(agendamento_opcoes.keys())
        )
        
        agendamento_id = agendamento_opcoes[agendamento_selecionado]
        
        # Buscar dados do agendamento
        agendamento_atual = next(a for a in agendamentos if a[0] == agendamento_id)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Status Atual:** {agendamento_atual[2]}")
            st.write(f"**Cliente:** {agendamento_atual[3]}")
            st.write(f"**Pet:** {agendamento_atual[4]}")
            st.write(f"**Serviço:** {agendamento_atual[5]}")
        
        with col2:
            status_opcoes = {
                "agendado": "📅 Agendado",
                "confirmado": "✅ Confirmado",
                "em_andamento": "🔄 Em Andamento", 
                "concluido": "✅ Concluído",
                "cancelado": "❌ Cancelado",
                "nao_compareceu": "❌ Não Compareceu"
            }
            
            novo_status = st.selectbox(
                "Novo Status:",
                list(status_opcoes.keys()),
                format_func=lambda x: status_opcoes[x],
                index=list(status_opcoes.keys()).index(agendamento_atual[2])
            )
        
        if st.button("💾 Atualizar Status", type="primary"):
            try:
                if managers['agendamento_manager'].atualizar_status(agendamento_id, novo_status):
                    st.success(f"✅ Status atualizado para '{status_opcoes[novo_status]}'!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar status!")
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    else:
        st.info("Nenhum agendamento pendente encontrado")

def tipos_servicos_web():
    """Lista de tipos de serviços"""
    st.subheader("🛠️ Tipos de Serviços")
    
    servicos = managers['agendamento_manager'].listar_tipos_servicos()
    
    if servicos:
        df = pd.DataFrame(servicos, columns=[
            'ID', 'Nome', 'Preço_Base', 'Duração_Minutos', 'Descrição', 'Criado_em'
        ])
        
        # Formatar duração
        df['Duração'] = df['Duração_Minutos'].apply(
            lambda x: f"{x//60}h {x%60}min" if x >= 60 else f"{x}min" if x else "N/A"
        )
        
        st.dataframe(
            df[['ID', 'Nome', 'Preço_Base', 'Duração', 'Descrição']],
            use_container_width=True
        )
    else:
        st.info("Nenhum tipo de serviço cadastrado")

def mostrar_relatorios():
    """Página de relatórios com gráficos"""
    st.header("📊 Relatórios e Análises")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Vendas", "📦 Estoque", "👥 Clientes", "🐕 Pets"])
    
    with tab1:
        relatorios_vendas()
    
    with tab2:
        relatorios_estoque()
    
    with tab3:
        relatorios_clientes()
    
    with tab4:
        relatorios_pets()

def relatorios_vendas():
    """Relatórios de vendas"""
    st.subheader("📈 Análise de Vendas")
    
    # Filtros de período
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("Data Início:", value=date.today() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("Data Fim:", value=date.today())
    
    # Vendas por dia
    vendas_periodo = managers['db'].execute_query('''
        SELECT DATE(data_venda) as data, COUNT(*) as qtd_vendas, SUM(total) as total_vendas
        FROM vendas 
        WHERE DATE(data_venda) BETWEEN ? AND ?
        GROUP BY DATE(data_venda)
        ORDER BY data
    ''', (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
    
    if vendas_periodo:
        df_vendas = pd.DataFrame(vendas_periodo, columns=['Data', 'Qtd_Vendas', 'Total_Vendas'])
        df_vendas['Data'] = pd.to_datetime(df_vendas['Data'])
        
        # Gráfico de faturamento
        col1, col2 = st.columns(2)
        
        with col1:
            fig_faturamento = px.line(
                df_vendas, x='Data', y='Total_Vendas',
                title='Faturamento por Dia',
                labels={'Total_Vendas': 'Faturamento (R$)', 'Data': 'Data'}
            )
            st.plotly_chart(fig_faturamento, use_container_width=True)
        
        with col2:
            fig_quantidade = px.bar(
                df_vendas, x='Data', y='Qtd_Vendas',
                title='Quantidade de Vendas por Dia',
                labels={'Qtd_Vendas': 'Número de Vendas', 'Data': 'Data'}
            )
            st.plotly_chart(fig_quantidade, use_container_width=True)
        
        # Métricas do período
        col1, col2, col3, col4 = st.columns(4)
        
        total_vendas = df_vendas['Qtd_Vendas'].sum()
        total_faturamento = df_vendas['Total_Vendas'].sum()
        ticket_medio = total_faturamento / total_vendas if total_vendas > 0 else 0
        
        with col1:
            st.metric("Total de Vendas", total_vendas)
        
        with col2:
            st.metric("Faturamento Total", f"R$ {total_faturamento:.2f}")
        
        with col3:
            st.metric("Ticket Médio", f"R$ {ticket_medio:.2f}")
        
        with col4:
            vendas_por_dia = total_vendas / len(df_vendas) if len(df_vendas) > 0 else 0
            st.metric("Vendas/Dia (Média)", f"{vendas_por_dia:.1f}")
        
        # Produtos mais vendidos
        st.subheader("🏆 Produtos Mais Vendidos")
        
        produtos_vendidos = managers['db'].execute_query('''
            SELECT p.nome, SUM(iv.quantidade) as qtd_vendida, SUM(iv.subtotal) as receita
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            JOIN vendas v ON iv.venda_id = v.id
            WHERE DATE(v.data_venda) BETWEEN ? AND ?
            GROUP BY p.id, p.nome
            ORDER BY qtd_vendida DESC
            LIMIT 10
        ''', (data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        
        if produtos_vendidos:
            df_produtos = pd.DataFrame(produtos_vendidos, columns=['Produto', 'Quantidade', 'Receita'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_produtos_qtd = px.bar(
                    df_produtos.head(10), x='Quantidade', y='Produto',
                    title='Top 10 - Quantidade Vendida',
                    orientation='h'
                )
                st.plotly_chart(fig_produtos_qtd, use_container_width=True)
            
            with col2:
                fig_produtos_receita = px.bar(
                    df_produtos.head(10), x='Receita', y='Produto',
                    title='Top 10 - Receita Gerada',
                    orientation='h'
                )
                st.plotly_chart(fig_produtos_receita, use_container_width=True)
    else:
        st.info("Nenhuma venda encontrada no período selecionado")

def relatorios_estoque():
    """Relatórios de estoque"""
    st.subheader("📦 Análise de Estoque")
    
    produtos = managers['produto_manager'].listar_todos()
    
    if produtos:
        df = pd.DataFrame(produtos, columns=[
            'ID', 'Nome', 'Categoria_ID', 'Preço', 'Estoque_Atual', 
            'Estoque_Mínimo', 'Código', 'Descrição', 'Marca', 'Peso', 
            'Unidade', 'Created', 'Updated', 'Categoria'
        ])
        
        # Valor do estoque
        df['Valor_Estoque'] = df['Preço'] * df['Estoque_Atual']
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Produtos", len(df))
        
        with col2:
            valor_total = df['Valor_Estoque'].sum()
            st.metric("Valor Total do Estoque", f"R$ {valor_total:.2f}")
        
        with col3:
            produtos_baixo = len(df[df['Estoque_Atual'] <= df['Estoque_Mínimo']])
            st.metric("Produtos com Estoque Baixo", produtos_baixo)
        
        with col4:
            sem_estoque = len(df[df['Estoque_Atual'] == 0])
            st.metric("Produtos Sem Estoque", sem_estoque)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Estoque por categoria
            estoque_categoria = df.groupby('Categoria')['Estoque_Atual'].sum().reset_index()
            
            fig_categoria = px.pie(
                estoque_categoria, values='Estoque_Atual', names='Categoria',
                title='Distribuição do Estoque por Categoria'
            )
            st.plotly_chart(fig_categoria, use_container_width=True)
        
        with col2:
            # Valor por categoria
            valor_categoria = df.groupby('Categoria')['Valor_Estoque'].sum().reset_index()
            
            fig_valor = px.bar(
                valor_categoria, x='Categoria', y='Valor_Estoque',
                title='Valor do Estoque por Categoria'
            )
            st.plotly_chart(fig_valor, use_container_width=True)
        
        # Produtos que precisam reposição
        if produtos_baixo > 0:
            st.subheader("⚠️ Produtos que Precisam de Reposição")
            
            df_baixo = df[df['Estoque_Atual'] <= df['Estoque_Mínimo']]
            
            st.dataframe(
                df_baixo[['Nome', 'Categoria', 'Estoque_Atual', 'Estoque_Mínimo', 'Valor_Estoque']],
                use_container_width=True
            )
        
        # Top produtos por valor
        st.subheader("💎 Top Produtos por Valor em Estoque")
        
        top_valor = df.nlargest(10, 'Valor_Estoque')
        
        fig_top_valor = px.bar(
            top_valor, x='Valor_Estoque', y='Nome',
            title='Top 10 - Maior Valor em Estoque',
            orientation='h'
        )
        st.plotly_chart(fig_top_valor, use_container_width=True)
    else:
        st.info("Nenhum produto cadastrado")

def relatorios_clientes():
    """Relatórios de clientes"""
    st.subheader("👥 Análise de Clientes")
    
    clientes = managers['cliente_manager'].listar_todos()
    pets = managers['pet_manager'].listar_todos()
    
    if clientes:
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Clientes", len(clientes))
        
        with col2:
            st.metric("Total de Pets", len(pets))
        
        with col3:
            pets_por_cliente = len(pets) / len(clientes) if len(clientes) > 0 else 0
            st.metric("Pets por Cliente (Média)", f"{pets_por_cliente:.1f}")
        
        with col4:
            # Clientes com mais de 1 pet
            clientes_multiplos_pets = managers['db'].execute_query('''
                SELECT COUNT(DISTINCT cliente_id) 
                FROM pets 
                WHERE cliente_id IN (
                    SELECT cliente_id FROM pets GROUP BY cliente_id HAVING COUNT(*) > 1
                )
            ''')
            multiplos = clientes_multiplos_pets[0][0] if clientes_multiplos_pets else 0
            st.metric("Clientes com Múltiplos Pets", multiplos)
        
        # Distribuição por cidade
        df_clientes = pd.DataFrame(clientes, columns=[
            'ID', 'Nome', 'CPF', 'Telefone', 'Email', 'Endereço', 'Cidade', 'CEP', 'Criado_em'
        ])
        
        # Clientes por cidade
        cidades = df_clientes['Cidade'].value_counts().reset_index()
        cidades.columns = ['Cidade', 'Quantidade']
        
        if len(cidades) > 0 and not cidades['Cidade'].isna().all():
            fig_cidades = px.bar(
                cidades.head(10), x='Cidade', y='Quantidade',
                title='Clientes por Cidade'
            )
            st.plotly_chart(fig_cidades, use_container_width=True)
        
        # Clientes mais ativos (com mais compras)
        clientes_vendas = managers['db'].execute_query('''
            SELECT c.nome, COUNT(v.id) as qtd_compras, SUM(v.total) as total_gasto
            FROM clientes c
            LEFT JOIN vendas v ON c.id = v.cliente_id
            GROUP BY c.id, c.nome
            HAVING qtd_compras > 0
            ORDER BY qtd_compras DESC
            LIMIT 10
        ''')
        
        if clientes_vendas:
            st.subheader("🏆 Clientes Mais Ativos")
            
            df_ativos = pd.DataFrame(clientes_vendas, columns=['Cliente', 'Qtd_Compras', 'Total_Gasto'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_compras = px.bar(
                    df_ativos, x='Qtd_Compras', y='Cliente',
                    title='Quantidade de Compras',
                    orientation='h'
                )
                st.plotly_chart(fig_compras, use_container_width=True)
            
            with col2:
                fig_gasto = px.bar(
                    df_ativos, x='Total_Gasto', y='Cliente',
                    title='Total Gasto (R$)',
                    orientation='h'
                )
                st.plotly_chart(fig_gasto, use_container_width=True)
    else:
        st.info("Nenhum cliente cadastrado")

def relatorios_pets():
    """Relatórios de pets"""
    st.subheader("🐕 Análise de Pets")
    
    pets = managers['pet_manager'].listar_todos()
    
    if pets:
        df = pd.DataFrame(pets, columns=[
            'ID', 'Nome', 'Cliente_ID', 'Espécie', 'Raça', 'Idade', 
            'Peso', 'Cor', 'Observações', 'Criado_em', 'Cliente_Nome', 'Cliente_Telefone'
        ])
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Pets", len(df))
        
        with col2:
            idade_media = df['Idade'].dropna().mean()
            st.metric("Idade Média", f"{idade_media:.1f} anos" if not pd.isna(idade_media) else "N/A")
        
        with col3:
            peso_medio = df['Peso'].dropna().mean()
            st.metric("Peso Médio", f"{peso_medio:.1f} kg" if not pd.isna(peso_medio) else "N/A")
        
        with col4:
            especies_unicas = df['Espécie'].nunique()
            st.metric("Tipos de Espécies", especies_unicas)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por espécie
            especies = df['Espécie'].value_counts().reset_index()
            especies.columns = ['Espécie', 'Quantidade']
            
            fig_especies = px.pie(
                especies, values='Quantidade', names='Espécie',
                title='Distribuição por Espécie'
            )
            st.plotly_chart(fig_especies, use_container_width=True)
        
        with col2:
            # Distribuição por idade
            idades_validas = df[df['Idade'].notna() & (df['Idade'] > 0)]
            
            if len(idades_validas) > 0:
                fig_idades = px.histogram(
                    idades_validas, x='Idade',
                    title='Distribuição por Idade',
                    nbins=10
                )
                st.plotly_chart(fig_idades, use_container_width=True)
            else:
                st.info("Dados de idade insuficientes")
        
        # Raças mais comuns por espécie
        st.subheader("🏆 Raças Mais Comuns")
        
        for especie in df['Espécie'].unique():
            pets_especie = df[df['Espécie'] == especie]
            racas = pets_especie['Raça'].value_counts().head(5)
            
            if len(racas) > 0 and not racas.index.isna().all():
                st.write(f"**{especie}:**")
                
                for raca, count in racas.items():
                    if pd.notna(raca):
                        st.write(f"- {raca}: {count} pet(s)")
                
                st.write("")
        
        # Pets por peso (para cães)
        caes = df[(df['Espécie'].str.lower() == 'cão') & df['Peso'].notna()]
        
        if len(caes) > 0:
            st.subheader("🐕 Distribuição de Peso dos Cães")
            
            # Categorizar por porte
            def categorizar_porte(peso):
                if peso < 10:
                    return "Pequeno"
                elif peso < 25:
                    return "Médio"
                else:
                    return "Grande"
            
            caes['Porte'] = caes['Peso'].apply(categorizar_porte)
            porte_dist = caes['Porte'].value_counts().reset_index()
            porte_dist.columns = ['Porte', 'Quantidade']
            
            fig_porte = px.bar(
                porte_dist, x='Porte', y='Quantidade',
                title='Distribuição por Porte (Cães)'
            )
            st.plotly_chart(fig_porte, use_container_width=True)
    else:
        st.info("Nenhum pet cadastrado")

if __name__ == "__main__":
    main() 