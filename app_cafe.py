import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# CADASTRO
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
# ÁREA
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
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    m_percent = st.number_input("m% (Alumínio)", step=1.0)
with c4:
    T = st.number_input("CTC T (cmolc/dm³)", step=0.1)

# =====================================================
# CORREÇÃO DO SOLO – AGORA FUNCIONA
# =====================================================
st.header("🧪 Correção do Solo (automática)")

V_desejado = 70
PRNT = 90

calcario_g_planta = 0.0
gesso_g_planta = 0.0

if T > 0 and v_percent < V_desejado:
    calcario_g_planta = (
        (V_desejado - v_percent)
        * T
        / PRNT
        / 10000
        * 1000
        * 2
    )
    gesso_g_planta = calcario_g_planta * 0.30

st.subheader("📊 Resultado")

c1, c2 = st.columns(2)

with c1:
    if calcario_g_planta > 300:
        st.warning(
            f"Calcário total: {calcario_g_planta:.0f} g/planta "
            f"(2x de {calcario_g_planta/2:.0f} g)"
        )
    else:
        st.success(f"Calcário: {calcario_g_planta:.0f} g/planta")

with c2:
    if gesso_g_planta > 200:
        st.warning(
            f"Gesso total: {gesso_g_planta:.0f} g/planta "
            f"(2x de {gesso_g_planta/2:.0f} g)"
        )
    else:
        st.success(f"Gesso: {gesso_g_planta:.0f} g/planta")

# =====================================================
# MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")
modalidade = st.selectbox("Escolha a modalidade", ["Fertirrigação", "Manual"])

# =====================================================
# TABELA EDITÁVEL
# =====================================================
st.header("📅 Distribuição Anual de Adubação")

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
