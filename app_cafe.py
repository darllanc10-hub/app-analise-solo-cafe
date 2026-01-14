import streamlit as st

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Correção de Solo – Café", layout="wide")
st.title("☕ Correção de Solo – Café")

# =====================================================
# 1️⃣ CADASTRO DO PRODUTOR
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
# 2️⃣ DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")

c1, c2, c3 = st.columns(3)
with c1:
    area = st.number_input("Área (ha)", min_value=0.0)
with c2:
    variedade = st.text_input("Variedade")
with c3:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 3️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3 = st.columns(3)
with c1:
    v_percent = st.number_input(
        "V% (Saturação por bases)",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )
with c2:
    m_percent = st.number_input(
        "m% (Saturação por Alumínio)",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )
with c3:
    T = st.number_input(
        "CTC a pH 7,0 (T) – cmolc/dm³",
        min_value=0.0,
        step=0.1
    )

# =====================================================
# 4️⃣ CÁLCULO DE CALCÁRIO E GESSO
# =====================================================
st.header("🧮 Resultado da Correção")

calcario_g_planta = 0.0
gesso_g_planta = 0.0

if T > 0 and v_percent < 70:
    calcario_g_planta = ((70 - v_percent) * T / 90 / 10000) * 1000 * 2

    # Gesso: 30% do calcário
    if m_percent >= 10 or v_percent <= 30:
        gesso_g_planta = calcario_g_planta * 0.30

# =====================================================
# 5️⃣ APRESENTAÇÃO DOS RESULTADOS
# =====================================================
c1, c2 = st.columns(2)

with c1:
    st.metric(
        label="Calcário recomendado",
        value=f"{calcario_g_planta:.0f} g/planta"
    )

with c2:
    if gesso_g_planta > 0:
        st.metric(
            label="Gesso agrícola recomendado",
            value=f"{gesso_g_planta:.0f} g/planta"
        )
    else:
        st.metric(
            label="Gesso agrícola",
            value="Não recomendado"
        )

st.info(
    "📌 O cálculo do calcário considera V alvo = 70%, PRNT = 90.\n"
    "📌 O gesso é recomendado quando m ≥ 10% ou V ≤ 30%, na dose de 30% do calcário."
)
