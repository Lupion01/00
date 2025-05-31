
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === CONFIGURAÇÕES INICIAIS ===
st.set_page_config(page_title="Sistema de Estoque", layout="wide")

# === ESTILO CUSTOMIZADO ===
st.markdown("""
    <style>
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #4CAF50;
    }
    .sidebar-button {
        display: block;
        width: 100%;
        padding: 12px;
        margin-bottom: 10px;
        text-align: left;
        font-size: 16px;
        border-radius: 10px;
        background-color: #f1f3f4;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    .sidebar-button:hover {
        background-color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# === SIDEBAR COM BOTÕES ===
st.sidebar.markdown('<div class="sidebar-title">Navegação</div>', unsafe_allow_html=True)

abas = [
    "Resumo Geral", 
    "Refrigerante", 
    "Cerveja Lata", 
    "Cerveja Garrafa", 
    "Suco Prat's", 
    "Água", 
    "Adicionar Produto", 
    "Histórico"
]

aba_selecionada = None
for aba in abas:
    if st.sidebar.button(aba, key=aba):
        aba_selecionada = aba

if aba_selecionada is None:
    aba_selecionada = "Resumo Geral"

# === FUNÇÃO PARA CARREGAR DADOS ===
def carregar_dados():
    caminho = "estoque_bebidas_completo.xlsx"
    if not os.path.exists(caminho):
        st.error("Arquivo de dados não encontrado.")
        return None
    else:
        return pd.read_excel(caminho, sheet_name=None, engine='openpyxl')

# === FUNÇÃO PARA EXIBIR TABELA COM CORES ===
def exibir_tabela_categoria(df):
    def classificar_estoque(row):
        if row["Estoque Atual"] >= row["Estoque Ideal"]:
            return "🟩 Verde"
        elif row["Estoque Atual"] >= row["Estoque Médio"]:
            return "🟨 Amarelo"
        elif row["Estoque Atual"] <= row["Estoque Crítico"]:
            return "🟥 Vermelho"
        else:
            return "⬜️ Padrão"

    df["Situação"] = df.apply(classificar_estoque, axis=1)
    st.dataframe(df[["Produto", "Estoque Atual", "Situação"]], use_container_width=True)

# === CARREGANDO DADOS ===
dados = carregar_dados()

# === EXIBINDO CONTEÚDO COM BASE NA ABA SELECIONADA ===
if dados:
    if aba_selecionada in dados:
        st.title(aba_selecionada)
        exibir_tabela_categoria(dados[aba_selecionada])
    elif aba_selecionada == "Resumo Geral":
        st.title("Resumo Geral")
        st.info("Resumo dos produtos em estado crítico ou abaixo da média aparecerá aqui.")
    elif aba_selecionada == "Adicionar Produto":
        st.title("Adicionar Novo Produto")
        st.info("Formulário para adicionar novo produto será exibido aqui.")
    elif aba_selecionada == "Histórico":
        st.title("Histórico de Alterações")
        st.info("Log de alterações aparecerá aqui.")
