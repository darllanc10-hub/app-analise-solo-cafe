import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Correção de Solo – Café", layout="wide")
st.title("☕ Correção de Solo – Café")

# =====================================================
# CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")

c1, c2, c3 = st.columns(3)
with c1:
    produtor = st.text_input("Produtor")
with c2:
    propriedade = st.text_input("Propriedade")
with c3:
    municipio = st.text_input("Município")

# =====================================================
# DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")

c1, c2, c3, c4 = st.columns(4)
with c1:
    area = st.number_input("Área (ha)", min_value=0.0)
with c2:
    plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c3:
    produtividade = st.selectbox(
        "Produtividade esperada (sc/ha)",
        list(range(10, 221, 10))
    )
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v = st.number_input("V% (Saturação por bases)", min_value=0.0, max_value=100.0)
with c3:
    m = st.number_input("m% (Saturação por Alumínio)", min_value=0.0, max_value=100.0)
with c4:
    T = st.number_input("CTC a pH 7 (T) – cmolc/dm³", min_value=0.0)

# =====================================================
# CORREÇÃO AUTOMÁTICA DE SOLO (CALCÁRIO E GESSO)
# =====================================================
st.header("🧮 Correção do Solo")

PRNT = 90
calcario_g = 0.0
gesso_g = 0.0

if T > 0 and plantas_ha > 0 and v < 70:
    calcario_t_ha = (70 - v) * T / PRNT
    calcario_g = (calcario_t_ha * 1_000_000) / plantas_ha

    if m >= 10 or v <= 30:
        gesso_g = calcario_g * 0.30

def parcela(valor, limite):
    if valor > limite:
        return "Aplicar em 2 parcelas no ano (50% agora e 50% após 6 meses)"
    elif valor > 0:
        return "Aplicação única"
    else:
        return "-"

c1, c2 = st.columns(2)

with c1:
    st.metric("Calcário recomendado", f"{calcario_g:.0f} g/planta")
    st.caption(parcela(calcario_g, 300))

with c2:
    if gesso_g > 0:
        st.metric("Gesso agrícola recomendado", f"{gesso_g:.0f} g/planta")
        st.caption(parcela(gesso_g, 200))
    else:
        st.metric("Gesso agrícola", "Não recomendado")

# =====================================================
# NITROGÊNIO – BASEADO NA PRODUTIVIDADE (5ª APROX.)
# =====================================================
st.header("🌿 Correção de Nitrogênio")

# Tabela oficial (kg N / ha)
tabela_n = {
    10: 220, 20: 250, 30: 280, 40: 310, 50: 340,
    60: 370, 70: 395, 80: 420, 90: 445, 100: 470,
    110: 495, 120: 520, 130: 540, 140: 560, 150: 580,
    160: 595, 170: 615, 180: 635, 190: 655, 200: 675,
    210: 675, 220: 675
}

N_kg_ha = tabela_n.get(produtividade, 0)

# Conversão para Ureia 46%
N_g_planta = 0
if plantas_ha > 0:
    N_g_planta = (N_kg_ha * 100 / 46) / plantas_ha * 1000

st.metric(
    "Nitrogênio recomendado (Ureia 46%)",
    f"{N_g_planta:.1f} g/planta/ano"
)

st.info(
    "📌 Nitrogênio calculado exclusivamente pela produtividade.\n"
    "📌 Conversão feita para Ureia 46%.\n"
    "📌 Dose total ANUAL por planta."
)

# =====================================================
# PRÓXIMA ETAPA
# =====================================================
st.header("📅 Distribuição Anual de Adubação")
st.info("🔧 A distribuição mensal e os cálculos de P, K, micros e MO serão adicionados na próxima etapa.")
