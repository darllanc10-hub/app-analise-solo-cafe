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
# =====================================================
# NPK – ETAPA A | NECESSIDADE ANUAL (5ª APROXIMAÇÃO)
# =====================================================
st.header("📊 NPK – Necessidade Anual (5ª Aproximação)")

# Produtividade
produtividade = st.selectbox(
    "Produtividade esperada (sc/ha)",
    options=list(range(10, 221, 10))
)

st.caption("Baseado na Tabela da 5ª Aproximação para café.")

# -------------------------------
# TABELA BASE (MODELO)
# Obs: valores exemplo – depois ajustamos exatamente à sua tabela
# -------------------------------
tabela_5_aprox = {
    10:  {"N": 60,  "P2O5": 20,  "K2O": 60},
    20:  {"N": 90,  "P2O5": 30,  "K2O": 90},
    30:  {"N": 120, "P2O5": 40,  "K2O": 120},
    40:  {"N": 150, "P2O5": 50,  "K2O": 150},
    50:  {"N": 180, "P2O5": 60,  "K2O": 180},
    60:  {"N": 210, "P2O5": 70,  "K2O": 210},
    80:  {"N": 260, "P2O5": 90,  "K2O": 260},
    100: {"N": 300, "P2O5": 110, "K2O": 300},
    120: {"N": 340, "P2O5": 130, "K2O": 340},
    150: {"N": 400, "P2O5": 160, "K2O": 400},
    180: {"N": 460, "P2O5": 190, "K2O": 460},
    200: {"N": 500, "P2O5": 210, "K2O": 500},
    220: {"N": 540, "P2O5": 230, "K2O": 540},
}

# Buscar necessidade
necessidade = tabela_5_aprox.get(produtividade)

if necessidade:
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Nitrogênio (N)", f"{necessidade['N']} kg/ha/ano")
    with c2:
        st.metric("Fósforo (P₂O₅)", f"{necessidade['P2O5']} kg/ha/ano")
    with c3:
        st.metric("Potássio (K₂O)", f"{necessidade['K2O']} kg/ha/ano")

    st.info(
        "📌 Estes valores representam a NECESSIDADE ANUAL.\n"
        "📌 A conversão para produto (g ou ml por planta) será feita na próxima etapa."
    )

    # Guardar no session_state para próximas etapas
    st.session_state["necessidade_npk"] = {
        "produtividade": produtividade,
        "N": necessidade["N"],
        "P2O5": necessidade["P2O5"],
        "K2O": necessidade["K2O"]
    }
else:
    st.warning("Produtividade não encontrada na tabela.")
# =====================================================
# TABELA (ETAPA SEGUINTE)
# =====================================================
st.header("📅 Distribuição Anual de Adubação")
st.info("🔧 A correção automática de NPK, macros e micros será integrada na próxima etapa.")
