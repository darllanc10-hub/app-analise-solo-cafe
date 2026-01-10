import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="Análise de Solo - Café",
    layout="wide"
)

st.title("☕ Análise de Solo – Café")

# =====================================================
# 📌 CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")

col1, col2, col3 = st.columns(3)

with col1:
    produtor = st.text_input("Nome do produtor")
with col2:
    propriedade = st.text_input("Propriedade")
with col3:
    municipio = st.text_input("Município")

# =====================================================
# 🌱 DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")

col1, col2, col3, col4 = st.columns(4)

with col1:
    area_ha = st.number_input("Área (ha)", min_value=0.0)
with col2:
    plantas_ha = st.number_input("Plantas por ha", min_value=0)
with col3:
    variedade = st.text_input("Variedade")
with col4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 🧪 CORREÇÃO DO SOLO
# =====================================================
st.header("🧪 Correção do Solo")

col1, col2 = st.columns(2)

with col1:
    calcario = st.number_input("Calcário (g por planta)", min_value=0.0)
    if calcario > 0:
        st.success(f"Calcário: {calcario:.0f} g por planta")

with col2:
    gesso = st.number_input("Gesso agrícola (g por planta)", min_value=0.0)
    if gesso > 0:
        st.warning(f"Gesso agrícola: {gesso:.0f} g por planta")

# =====================================================
# 🚜 MODALIDADE DE APLICAÇÃO
# =====================================================
st.header("🚜 Modalidade de Aplicação")

tipo_aplicacao = st.radio(
    "Escolha a modalidade:",
    ["Manual", "Fertirrigação"]
)

# =====================================================
# 🧂 ADUBOS CADASTRADOS
# =====================================================
adubos = {
    "Ureia 46%": {
        "dose": 120,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev", "Mar", "Abr"]
    },
    "MAP": {
        "dose": 80,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Set", "Out"]
    },
    "KCl": {
        "dose": 100,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Nov", "Dez"]
    },
    "Boro": {
        "dose": 2,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Jan"]
    },
    "Zinco": {
        "dose": 2,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Fev"]
    }
}

# =====================================================
# 📋 SELEÇÃO E AJUSTE
# =====================================================
st.header("📋 Seleção e Ajuste de Adubos")

adubos_ativos = {}

for nome, info in adubos.items():
    if info["modalidade"] != tipo_aplicacao:
        continue

    col1, col2 = st.columns([3, 2])

    with col1:
        ativo = st.checkbox(nome, value=True)

    with col2:
        dose_editada = st.number_input(
            f"Dose ({info['unidade']})",
            value=float(info["dose"]),
            step=1.0,
            key=f"dose_{nome}"
        )

    if ativo:
        adubos_ativos[nome] = {
            "dose": dose_editada,
            "unidade": info["unidade"],
            "meses": info["meses"]
        }

# =====================================================
# 📅 TABELA ANUAL
# =====================================================
st.header("📅 Tabela de Distribuição Anual (por planta)")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

tabela = pd.DataFrame(index=meses)

for nome, info in adubos_ativos.items():
    tabela[nome] = [
        f"{info['dose']} {info['unidade']}" if mes in info["meses"] else ""
        for mes in meses
    ]

st.dataframe(tabela, use_container_width=True)
