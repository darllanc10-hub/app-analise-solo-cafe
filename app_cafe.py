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
# CORREÇÃO AUTOMÁTICA DE SOLO
# =====================================================
st.header("🧮 Correção do Solo")

PRNT = 90
calcario_g = 0.0
gesso_g = 0.0

if T > 0 and plantas_ha > 0 and v < 70:
    # Cálculo em t/ha
    calcario_t_ha = (70 - v) * T / PRNT

    # Conversão para g/planta
    calcario_g = (calcario_t_ha * 1_000_000) / plantas_ha

    # Gesso = 30% do calcário
    if m >= 10 or v <= 30:
        gesso_g = calcario_g * 0.30

# =====================================================
# FUNÇÃO DE PARCELAMENTO (AJUSTADA)
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

st.info(
    "📌 Calcário calculado por saturação de bases (V alvo = 70%).\n"
    "📌 Gesso = 30% do calcário quando m ≥ 10% ou V ≤ 30%.\n"
    "📌 Parcelamento indica divisão da DOSE TOTAL anual, não reaplicação."
)

st.header("🌿 Nitrogênio (N)")

produtividade = st.number_input(
    "Produtividade esperada (sc/ha)",
    min_value=10,
    max_value=220,
    step=1
)

# Tabela 5ª aproximação – necessidade de N (kg/ha)
N_necessidade = 0

for faixa, valor in {
    (91,100):445, (101,110):470, (111,120):495,
    (121,130):520, (131,140):540, (141,150):560,
    (151,160):580, (161,170):595, (171,180):615,
    (181,190):635, (191,200):655, (201,220):675
}.items():
    if faixa[0] <= produtividade <= faixa[1]:
        N_necessidade = valor
        break

if N_necessidade > 0 and plantas_ha > 0:
    ureia_kg_ha = N_necessidade * 100 / 46
    ureia_g_planta_ano = (ureia_kg_ha * 1000) / plantas_ha

    st.metric(
        "Ureia 46% – Dose ANUAL",
        f"{ureia_g_planta_ano:.0f} g/planta/ano"
    )

    st.caption(
        f"N necessário: {N_necessidade} kg/ha | "
        f"Ureia: {ureia_kg_ha:.0f} kg/ha"
    )
# =====================================================
# TABELA (ETAPA SEGUINTE)
# =====================================================
st.header("📅 Distribuição Anual de Adubação")
st.info("🔧 A correção automática de NPK, macros e micros será integrada na próxima etapa.")
