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
# CÁLCULO DE CALCÁRIO E GESSO
# =====================================================
st.header("🧮 Correção do Solo")

PRNT = 90
calcario = 0.0
gesso = 0.0

if T > 0 and v < 70:
    # Fórmula conforme você descreveu
    calcario = ((70 - v) * T / PRNT / 10000 * 1000 * 2)
    
    # Gesso = 30% do calcário quando m >=10 ou V <= 30
    if m >= 10 or v <= 30:
        gesso = calcario * 0.30

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
c1, c2 = st.columns(2)

with c1:
    st.metric("Calcário recomendado", f"{calcario*1000:.0f} g/planta")
    st.caption(parcela(calcario*1000, 300))

with c2:
    if gesso > 0:
        st.metric("Gesso agrícola recomendado", f"{gesso*1000:.0f} g/planta")
        st.caption(parcela(gesso*1000, 200))
    else:
        st.metric("Gesso agrícola", "Não recomendado")

st.info(
    "📌 Calcário calculado para elevar V% até 70%.\n"
    "📌 Gesso = 30% do calcário quando m ≥ 10% ou V ≤ 30%.\n"
    "📌 Parcelamento indica divisão da dose total anual."
)

# =====================================================
# TABELA FUTURA
# =====================================================
st.header("📅 Distribuição Anual de Adubação")
st.info("🔧 A correção automática de NPK, macros e micros será integrada na próxima etapa.")
