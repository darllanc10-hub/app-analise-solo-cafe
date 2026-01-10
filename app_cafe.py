import streamlit as st
import pandas as pd

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="centered"
)

st.title("🌱 Análise e Planejamento de Adubação – Café")

# =========================
# DADOS FIXOS DO SISTEMA
# =========================

# Adubos cadastrados

import streamlit as st
import pandas as pd
st.title("🌱 Interpretação de Análise de Solo – Café")

st.markdown("### 🔧 Tipo de Aplicação")
tipo_aplicacao = st.radio(
    "Selecione a modalidade de adubação:",
    ["Fertirrigação", "Manual"]
)

st.divider()
st.markdown("### 🧪 Dados da Análise de Solo")

col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input("pH", value=5.5)
    v = st.number_input("V (%)", value=60.0)
    m = st.number_input("m (%)", value=5.0)
    mo = st.number_input("Matéria Orgânica (%)", value=2.5)

with col2:
    ca = st.number_input("Cálcio (cmolc/dm³)", value=2.0)
    mg = st.number_input("Magnésio (cmolc/dm³)", value=0.8)
    k = st.number_input("Potássio (cmolc/dm³)", value=0.25)
    s = st.number_input("Enxofre (mg/dm³)", value=10.0)

with col3:
    p = st.number_input("Fósforo (mg/dm³)", value=8.0)
    b = st.number_input("Boro (mg/dm³)", value=0.3)
    zn = st.number_input("Zinco (mg/dm³)", value=1.0)
    cu = st.number_input("Cobre (mg/dm³)", value=0.5)
    mn = st.number_input("Manganês (mg/dm³)", value=20.0)
st.set_page_config(layout="centered")

st.title("☕ Interpretação de Análise de Solo – Café")

st.markdown("### 📌 Dados do Produtor")

nome = st.text_input("Nome do produtor")
talhao = st.text_input("Talhão")

st.markdown("### 🌱 Espaçamento e Produção")

col1, col2 = st.columns(2)
with col1:
    espac_linha = st.number_input("Espaçamento entre linhas (m)", value=3.0)
with col2:
    espac_planta = st.number_input("Espaçamento entre plantas (m)", value=1.0)

produtividade = st.number_input("Produtividade (sc/ha)", value=60)

plantas_ha = 10000 / (espac_linha * espac_planta)

st.markdown("---")

st.markdown("### 🧪 Saturação de Bases")

V_atual = st.number_input("V atual (%)", value=45)
V_desejado = 70
PRNT = 90

if V_atual < V_desejado:
    dose_calcario = ((V_desejado - V_atual) / V_desejado) * 2
    dose_calcario = min(dose_calcario, 3)
else:
    dose_calcario = 0

calcario_planta = (dose_calcario * 1_000_000) / plantas_ha
dose_gesso = dose_calcario * 0.30
gesso_planta = (dose_gesso * 1_000_000) / plantas_ha

st.markdown("### 🟤 Calagem e Gessagem")

st.success(f"Calcário: {calcario_planta:.0f} g por planta")
st.warning(f"Gesso agrícola: {gesso_planta:.0f} g por planta")

st.markdown("---")
# ==============================
# CADASTRO DE ADUBOS (PADRÃO)
# ==============================

adubos = {
    "Ureia 46% (fertirrigação)": {
        "dose": 22,
        "unidade": "g/planta",
        "meses": ["Set", "Out", "Nov", "Dez", "Jan", "Fev", "Mar"]
    },
    "Nitrato de Amônio": {
        "dose": 22,
        "unidade": "g/planta",
        "meses": ["Set", "Out", "Nov", "Dez", "Jan", "Fev", "Mar"]
    },
    "Ureia Sulfatada": {
        "dose": 37,
        "unidade": "g/planta",
        "meses": ["Set", "Out", "Nov", "Dez", "Jan", "Fev", "Mar"]
    },
    "26-00-26": {
        "dose": 45,
        "unidade": "g/planta",
        "meses": ["Out", "Dez", "Fev"]
    },
    "20-10-05 (florada)": {
        "dose": 100,
        "unidade": "g/planta",
        "meses": ["Jun", "Ago"]
    },
    "19-04-19 (granação)": {
        "dose": 100,
        "unidade": "g/planta",
        "meses": ["Out", "Dez", "Fev", "Abr"]
    },
    "Fertium Produção": {
        "dose": 150,
        "unidade": "g/planta",
        "meses": ["Out", "Dez", "Fev", "Abr"]
    },
    "MAP purificado": {
        "dose": 13,
        "unidade": "g/planta",
adubos = {
    "Ureia (46%)": {
        "dose": 10,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev", "Mar"]
    },
    "26-00-26": {
        "dose": 12,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev"]
    },
    "19-04-19": {
        "dose": 100,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Out", "Nov", "Dez"]
    },
    "Fertium Produção": {
        "dose": 150,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Out", "Dez", "Fev"]
    },
        "meses": ["Set", "Nov", "Jan"]
    },
    "Petrum (Vittia)": {
        "dose": 12,
        "unidade": "ml/planta",
        "meses": ["Set", "Nov", "Jan"]
    },
    "Cloreto de Potássio": {
        "dose": 20,
        "unidade": "g/planta",
        "meses": ["Out", "Dez", "Fev"]
    },
    "Sulfato de Magnésio": {
        "dose": 15,
        "unidade": "g/planta",
        "meses": ["Nov", "Jan"]
    },
    "Nitrato de Cálcio": {
        "dose": 20,
import streamlit as st
import pandas as pd

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="centered"
)

st.title("🌱 Análise e Planejamento de Adubação – Café")

# =========================
# DADOS FIXOS DO SISTEMA
# =========================

# Adubos cadastrados
adubos = {
    "Ureia (46%)": {
        "dose": 10,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev", "Mar"]
    },
    "26-00-26": {
        "dose": 12,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev"]
    },
    "19-04-19": {
        "dose": 100,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Out", "Nov", "Dez"]
    },
    "Fertium Produção": {
        "dose": 150,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Out", "Dez", "Fev"]
    },
    "Nitrato de Cálcio": {
        "dose": 13,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev"]
    },
    "Sulfato de Magnésio": {
        "dose": 6,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Abr", "Mai"]
    },
    "Boro": {
        "dose": 2,
        "unidade": "L/ha",
        "modalidade": "Fertirrigação",
        "meses": ["Jun"]
    },
    "Zinco": {
        "dose": 2,
        "unidade": "L/ha",
        "modalidade": "Fertirrigação",
        "meses": ["Nov"]
    },
    "Multicafé Conilon": {
        "dose": 15,
        "unidade": "L/ha",
        "modalidade": "Fertirrigação",
        "meses": ["Nov", "Jan", "Mar"]
    },
    "Biogrow Mol": {
        "dose": 20,
        "unidade": "L/ha",
        "modalidade": "Fertirrigação",
        "meses": ["Fora"]
    }
}

# =========================
# CALAGEM E GESSAGEM
# =========================
st.subheader("🪨 Correção do Solo")

calcario = st.number_input("Calcário (g por planta)", value=214.0)
gesso = st.number_input("Gesso agrícola (g por planta)", value=64.0)

st.success(f"Calcário: {calcario:.0f} g por planta")
st.warning(f"Gesso agrícola: {gesso:.0f} g por planta")

# =========================
# SELEÇÃO DE MODALIDADE
# =========================
st.subheader("🚜 Modalidade de Aplicação")

tipo_aplicacao = st.radio(
    "Escolha a modalidade:",
    ["Fertirrigação", "Manual"]
)

# =========================
# SELEÇÃO E EDIÇÃO DE ADUBOS
# =========================
st.subheader("🧪 Seleção e Ajuste de Adubos")

adubos_ativos = {}

for nome, info in adubos.items():
    if info["modalidade"] != tipo_aplicacao:
        continue

    col1, col2 = st.columns([3, 2])

    with col1:
        ativo = st.checkbox(nome, value=True)

    with col2:
        nova_dose = st.number_input(
            f"Dose ({info['unidade']})",
            value=float(info["dose"]),
            step=1.0,
            key=f"dose_{nome}"
        )

    if ativo:
        adubos_ativos[nome] = {
            "dose": nova_dose,
            "unidade": info["unidade"],
            "meses": info["meses"]
        }

# =========================
# TABELA DE DISTRIBUIÇÃO ANUAL
# =========================
st.subheader("📅 Tabela de Distribuição Anual")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

tabela = pd.DataFrame(index=meses)

for nome, info in adubos_ativos.items():
    tabela[nome] = [
        f"{info['dose']} {info['unidade']}" if mes in info["meses"] else ""
        for mes in meses
    ]

st.dataframe(tabela, use_container_width=True)

# =========================
# FINAL
# =========================
st.success("✅ Planejamento gerado com sucesso")
