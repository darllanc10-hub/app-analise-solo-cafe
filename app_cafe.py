import streamlit as st
import pandas as pd

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
# CORREÇÃO DE SOLO
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

# =====================================================
# NITROGÊNIO (UREIA 46%)
# =====================================================

tabela_n = {
20: 220, 30: 250, 40: 280, 50: 310, 60: 340, 70: 370, 80: 395,
90: 420, 100: 445, 110: 470, 120: 495, 130: 520, 140: 540,
150: 560, 160: 580, 170: 595, 180: 615, 190: 635, 200: 655, 220: 675
}

def necessidade_n(prod):
    for limite, valor in tabela_n.items():
        if prod <= limite:
            return valor
    return 675

n_kg_ha = necessidade_n(produtividade)

# Fórmula que você passou:
# Necessidade x 100 ÷ %N ÷ plantas/ha x 1000 = g/planta/ano
ureia_g_planta = (n_kg_ha * 100 / 46 / plantas_ha) * 1000

# =====================================================
# FUNÇÃO DE PARCELAMENTO
# =====================================================
def parcela(valor, limite):
    if valor > limite:
        return "Aplicar em 2 parcelas no ano (50% agora e 50% após 6 meses)"
    elif valor > 0:
        return "Aplicação única"
    else:
        return "-"

# =====================================================
# RESULTADOS
# =====================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Calcário recomendado", f"{calcario_g:.0f} g/planta")
    st.caption(parcela(calcario_g, 300))

with c2:
    if gesso_g > 0:
        st.metric("Gesso agrícola recomendado", f"{gesso_g:.0f} g/planta")
        st.caption(parcela(gesso_g, 200))
    else:
        st.metric("Gesso agrícola", "Não recomendado")

with c3:
    st.metric("Nitrogênio recomendado (Uréia 46%)", f"{ureia_g_planta:.0f} g/planta/ano")

st.info(
    "📌 Calcário calculado por saturação de bases (V alvo = 70%).\n"
    "📌 Gesso = 30% do calcário quando m ≥ 10% ou V ≤ 30%.\n"
    "📌 Nitrogênio calculado pela produtividade e convertido para Uréia 46%."
)

# =====================================================
# TABELA
# =====================================================
st.header("📅 Distribuição Anual de Adubação")
st.info("🔧 A correção automática de P, K, Ca, Mg e micros será integrada na próxima etapa.")
