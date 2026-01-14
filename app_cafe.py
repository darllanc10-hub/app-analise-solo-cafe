import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")
c1, c2, c3 = st.columns(3)
produtor = c1.text_input("Produtor")
propriedade = c2.text_input("Propriedade")
municipio = c3.text_input("Município")

# =====================================================
# DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")
c1, c2, c3, c4 = st.columns(4)
area = c1.number_input("Área (ha)", min_value=0.0)
plantas_ha = c2.number_input("Plantas por ha", min_value=0)
variedade = c3.text_input("Variedade")
idade = c4.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3, c4 = st.columns(4)
ph = c1.number_input("pH", step=0.1)
v_percent = c2.number_input("V% (Saturação por bases)", step=1.0)
m_percent = c3.number_input("m% (Alumínio)", step=1.0)
T = c4.number_input("CTC T (cmolc/dm³)", step=0.1)

st.subheader("Macronutrientes (cmolc/dm³ ou mg/dm³)")
c1, c2, c3, c4, c5 = st.columns(5)
ca = c1.number_input("Ca", step=0.1)
mg = c2.number_input("Mg", step=0.1)
k = c3.number_input("K", step=0.1)
p = c4.number_input("P", step=0.1)
s = c5.number_input("S", step=0.1)

st.subheader("Micronutrientes (mg/dm³)")
c1, c2, c3, c4, c5 = st.columns(5)
b = c1.number_input("B", step=0.01)
zn = c2.number_input("Zn", step=0.1)
cu = c3.number_input("Cu", step=0.1)
mn = c4.number_input("Mn", step=0.1)
fe = c5.number_input("Fe", step=0.1)

mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# CORREÇÃO DO SOLO – CÁLCULO CORRETO
# =====================================================
st.header("🧪 Resultado da Correção do Solo")

PRNT = 90  # fixo
V_ALVO = 70

if v_percent < V_ALVO and T > 0:
    calcario_g_planta = (
        (V_ALVO - v_percent) * T / PRNT / 10000 * 1000 * 2
    )
else:
    calcario_g_planta = 0.0

# gesso provisório (20% do calcário)
gesso_g_planta = calcario_g_planta * 0.2

st.success(f"🪨 Calcário: **{calcario_g_planta:.1f} g/planta**")
st.success(f"🧂 Gesso agrícola: **{gesso_g_planta:.1f} g/planta**")

# =====================================================
# MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")
modalidade = st.selectbox("Escolha a modalidade", ["Fertirrigação", "Manual"])

# =====================================================
# TABELA (SEM AUTO-DISTRIBUIR AINDA)
# =====================================================
st.header("📅 Distribuição Anual de Adubação (editável)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "MAP (g/planta)": [""] * 12,
        "KCl (g/planta)": [""] * 12,
        "Ca (g/planta)": [""] * 12,
        "Mg (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""] * 12,
        "20-10-05 (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)
st.data_editor(df, use_container_width=True, num_rows="fixed")
