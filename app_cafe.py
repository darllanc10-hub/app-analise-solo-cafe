import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

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

c1, c2, c3, c4 = st.columns(4)
with c1:
    area = st.number_input("Área (ha)", min_value=0.0)
with c2:
    plantas_ha = st.number_input("Plantas por ha", min_value=0)
with c3:
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 3️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

st.markdown("### 📌 Parâmetros Químicos")

c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", min_value=0.0, max_value=100.0, step=1.0)
with c3:
    m_percent = st.number_input("m% (Saturação por Alumínio)", min_value=0.0, max_value=100.0, step=1.0)
with c4:
    T = st.number_input("CTC a pH 7,0 (T) – cmolc/dm³", min_value=0.0, step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO – AUTOMÁTICA
# =====================================================
st.header("🧮 Correção do Solo")

calcario_g = 0.0
gesso_g = 0.0

if T > 0:
    if v_percent < 70:
        calcario_g = ((70 - v_percent) * T / 90 / 10000) * 1000 * 2

    if calcario_g > 0 and (m_percent >= 10 or v_percent <= 30):
        gesso_g = calcario_g * 0.30

# Parcelamento
def parcelamento(valor, limite):
    if valor > limite:
        return "Dividir em 2 aplicações"
    elif valor > 0:
        return "Aplicação única"
    else:
        return "-"

# RESULTADOS
c1, c2 = st.columns(2)

with c1:
    st.metric("Calcário recomendado", f"{calcario_g:.0f} g/planta")
    st.caption(parcelamento(calcario_g, 300))

with c2:
    if gesso_g > 0:
        st.metric("Gesso agrícola recomendado", f"{gesso_g:.0f} g/planta")
        st.caption(parcelamento(gesso_g, 200))
    else:
        st.metric("Gesso agrícola", "Não recomendado")

# =====================================================
# 5️⃣ TABELA (mantida para próxima etapa)
# =====================================================
st.header("📅 Distribuição Anual de Adubação")

st.info("🔧 A correção automática de NPK, macros e micros será ligada na próxima etapa.")
