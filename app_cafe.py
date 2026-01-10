import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="Análise de Solo - Café",
    layout="wide"
)

st.title("☕ Análise de Solo – Café")

# ---------------- SELEÇÃO DA MODALIDADE ----------------
tipo_aplicacao = st.radio(
    "Selecione a modalidade de aplicação:",
    ["Manual", "Fertirrigação"]
)

# ---------------- ADUBOS CADASTRADOS ----------------
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

st.divider()

# ---------------- SELEÇÃO E EDIÇÃO ----------------
st.subheader("📋 Seleção e ajuste de adubos")

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

st.divider()

# ---------------- TABELA DE DISTRIBUIÇÃO ----------------
st.subheader("📅 Tabela de Distribuição Anual (g por planta)")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

tabela = pd.DataFrame(index=meses)

for nome, info in adubos_ativos.items():
    tabela[nome] = [
        f"{info['dose']} {info['unidade']}" if mes in info["meses"] else ""
        for mes in meses
    ]

st.dataframe(tabela, use_container_width=True)
