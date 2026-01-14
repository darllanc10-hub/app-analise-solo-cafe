import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# 1️⃣ CADASTRO
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
    plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c3:
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 3️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

st.subheader("Parâmetros gerais")
c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    m_percent = st.number_input("m% (Alumínio)", step=1.0)
with c4:
    T = st.number_input("CTC T (cmolc/dm³)", step=0.1)

st.subheader("Macronutrientes (cmolc/dm³ ou mg/dm³)")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    ca = st.number_input("Ca", step=0.1)
with c2:
    mg = st.number_input("Mg", step=0.1)
with c3:
    k = st.number_input("K", step=0.1)
with c4:
    p = st.number_input("P", step=0.1)
with c5:
    s = st.number_input("S", step=0.1)

st.subheader("Micronutrientes (mg/dm³)")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    b = st.number_input("B", step=0.1)
with c2:
    zn = st.number_input("Zn", step=0.1)
with c3:
    cu = st.number_input("Cu", step=0.1)
with c4:
    mn = st.number_input("Mn", step=0.1)
with c5:
    fe = st.number_input("Fe", step=0.1)

mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO – CALCÁRIO E GESSO
# =====================================================
st.header("🧪 Correção do Solo (automática)")

V_DESEJADO = 70
PRNT = 90

# cálculo SEM if visual
if T > 0:
    calcario_g_planta = (
        (V_DESEJADO - v_percent)
        * T
        / PRNT
        / 10000
        * 1000
        * 2
    )
else:
    calcario_g_planta = 0

if calcario_g_planta < 0:
    calcario_g_planta = 0

gesso_g_planta = calcario_g_planta * 0.30

st.subheader("📊 Resultado da Correção")

c1, c2 = st.columns(2)

with c1:
    if calcario_g_planta > 300:
        st.warning(
            f"Calcário total: {calcario_g_planta:.1f} g/planta "
            f"(parcelar em 2x de {calcario_g_planta/2:.1f} g)"
        )
    else:
        st.success(f"Calcário: {calcario_g_planta:.1f} g/planta")

with c2:
    if gesso_g_planta > 200:
        st.warning(
            f"Gesso total: {gesso_g_planta:.1f} g/planta "
            f"(parcelar em 2x de {gesso_g_planta/2:.1f} g)"
        )
    else:
        st.success(f"Gesso: {gesso_g_planta:.1f} g/planta")

# =====================================================
# 5️⃣ MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")
modalidade = st.selectbox("Escolha a modalidade", ["Fertirrigação", "Manual"])

# =====================================================
# 6️⃣ TABELA FINAL
# =====================================================
st.header("📅 Distribuição Anual de Adubação (editável)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""]*12,
        "MAP (g/planta)": [""]*12,
        "KCl (g/planta)": [""]*12,
        "Nitrato de Cálcio (g/planta)": [""]*12,
        "Sulfato de Magnésio (g/planta)": [""]*12,
        "Super S (ml/planta)": [""]*12,
        "Multicafé Conilon (ml/ha)": [""]*12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""]*12,
        "20-10-05 (g/planta)": [""]*12,
        "Caltimag (g/planta)": [""]*12,
        "Multicafé Conilon (ml/ha)": [""]*12,
    }

df = pd.DataFrame(dados, index=meses)
st.data_editor(df, use_container_width=True, num_rows="fixed")
