import streamlit as st
import pandas as pd

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="centered"
)

st.title("🌱 Análise de Solo – Café")

# ===============================
# DADOS DA ÁREA / PRODUTOR
# ===============================
st.header("📋 Identificação")

produtor = st.text_input("Produtor")
area = st.text_input("Área / Talhão")
cultura = st.selectbox("Cultura", ["Café Conilon", "Café Arábica"])
plantas_ha = st.number_input("Plantas por hectare", value=3000, step=100)

# ===============================
# PARÂMETROS QUÍMICOS
# ===============================
st.header("🧪 Parâmetros Químicos do Solo")

ph = st.number_input("pH", value=5.0, step=0.1)
v_atual = st.number_input("Saturação por Bases (V%)", value=40.0, step=1.0)
v_desejado = 60.0

ca = st.number_input("Cálcio (Ca)", value=1.5, step=0.1)
mg = st.number_input("Magnésio (Mg)", value=0.5, step=0.1)
k = st.number_input("Potássio (K)", value=80.0, step=5.0)
p = st.number_input("Fósforo (P)", value=8.0, step=1.0)

st.subheader("Micronutrientes")
zn = st.number_input("Zinco (Zn)", value=1.2, step=0.1)
b = st.number_input("Boro (B)", value=0.2, step=0.05)
cu = st.number_input("Cobre (Cu)", value=0.8, step=0.1)
mn = st.number_input("Manganês (Mn)", value=20.0, step=1.0)
fe = st.number_input("Ferro (Fe)", value=120.0, step=5.0)

st.header("🌾 Matéria Orgânica")
mo = st.number_input("Matéria Orgânica (%)", value=1.8, step=0.1)

# ===============================
# MODALIDADE DE APLICAÇÃO
# ===============================
st.header("🚜 Modalidade de Aplicação")
modalidade = st.selectbox("Escolha a modalidade", ["Manual", "Fertirrigação"])

# ===============================
# CÁLCULO DE CALAGEM E GESSAGEM
# ===============================
st.header("🧮 Cálculo de Calagem e Gessagem")

calcario_t_ha = max((v_desejado - v_atual) * 0.04, 0)
gesso_t_ha = calcario_t_ha * 0.3

calcario_g_planta = (calcario_t_ha * 1000) / plantas_ha
gesso_g_planta = (gesso_t_ha * 1000) / plantas_ha

# ===============================
# RESULTADO DA CORREÇÃO DO SOLO
# ===============================
st.header("📊 Resultado da Correção do Solo")

st.success(f"🪨 Calcário: {calcario_g_planta:.0f} g por planta")
st.warning(f"🟡 Gesso agrícola: {gesso_g_planta:.0f} g por planta")

# ===============================
# ADUBOS DISPONÍVEIS
# ===============================
st.header("🧾 Seleção e Ajuste de Adubos")

adubos = {
    "Ureia 46%": {
        "dose": 120,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Out", "Nov", "Jan"]
    },
    "MAP": {
        "dose": 80,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Set"]
    },
    "Cloreto de Potássio": {
        "dose": 100,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Dez", "Jan"]
    },
    "Caltimag": {
        "dose": 150,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Mar"]
    },
    "Multicafé Conilon": {
        "dose": 200,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Set", "Nov"]
    }
}

adubos_ativos = {}

for nome, info in adubos.items():
    if info["modalidade"] != modalidade:
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
            **info,
            "dose": dose_editada
        }

# ===============================
# TABELA DE DISTRIBUIÇÃO
# ===============================
st.header("📅 Tabela de Distribuição Anual (g por planta)")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

tabela = pd.DataFrame(index=meses)

for nome, info in adubos_ativos.items():
    tabela[nome] = [
        f"{info['dose']} {info['unidade']}" if mes in info["meses"] else ""
        for mes in meses
    ]

st.dataframe(tabela, use_container_width=True)

# ===============================
# UPLOAD DE FOTO (ETAPA C)
# ===============================
st.header("📷 Upload da Análise de Solo (em teste)")

st.file_uploader(
    "Envie uma foto da análise de solo (PDF ou imagem)",
    type=["png", "jpg", "jpeg", "pdf"]
)
