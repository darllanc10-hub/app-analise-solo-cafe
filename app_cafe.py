import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO GERAL
# =====================================================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="wide"
)

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

c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    m_percent = st.number_input("m% (Saturação por alumínio)", step=1.0)

c1, c2, c3, c4 = st.columns(4)
with c1:
    ca = st.number_input("Cálcio (Ca)", step=0.1)
with c2:
    mg = st.number_input("Magnésio (Mg)", step=0.1)
with c3:
    k = st.number_input("Potássio (K)", step=0.1)
with c4:
    p = st.number_input("Fósforo (P)", step=0.1)

mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO (INPUT)
# =====================================================
st.header("🧪 Correção do Solo")

c1, c2 = st.columns(2)
with c1:
    calcario = st.number_input("Calcário (g/planta)", min_value=0.0)
with c2:
    gesso = st.number_input("Gesso agrícola (g/planta)", min_value=0.0)
# =====================================================
# RESULTADO – CALCÁRIO E GESSO (AUTOMÁTICO)
# =====================================================
st.subheader("📊 Resultado da Correção do Solo")

# Parâmetros técnicos
V_alvo = 70
PRNT = 0.90
limite_calcario_t_ha = 3

# Cálculo do calcário (t/ha)
if v_percent < V_alvo:
    calcario_t_ha = ((V_alvo - v_percent) / V_alvo) * limite_calcario_t_ha
    calcario_t_ha = min(calcario_t_ha, limite_calcario_t_ha)
else:
    calcario_t_ha = 0

# Conversão para g/planta
calcario_g_planta_calc = (
    (calcario_t_ha * 1000 * 1000) / plantas_ha
    if plantas_ha > 0 else 0
)

# Gesso: 30% do calcário, com regra técnica
if v_percent <= 30 or m_percent >= 10:
    gesso_t_ha = calcario_t_ha * 0.30
else:
    gesso_t_ha = 0

gesso_g_planta_calc = (
    (gesso_t_ha * 1000 * 1000) / plantas_ha
    if plantas_ha > 0 else 0
)

# Exibição
st.write(f"🪨 **Calcário:** {calcario_g_planta_calc:.0f} g por planta")
st.write(f"🧱 **Gesso agrícola:** {gesso_g_planta_calc:.0f} g por planta")
# =====================================================
# 5️⃣ ENXOFRE – SUPER S
# =====================================================
st.header("🧪 Enxofre (Super S)")

super_s_l_ha = 5
super_s_ml_planta = (super_s_l_ha * 1000) / plantas_ha if plantas_ha > 0 else 0

st.write(f"➡ **Super S:** {super_s_l_ha} L/ha")
st.write(f"➡ **{super_s_ml_planta:.2f} ml por planta**")

# =====================================================
# 6️⃣ MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")

modalidade = st.selectbox(
    "Escolha a modalidade",
    ["Fertirrigação", "Manual"]
)

# =====================================================
# 7️⃣ DOSES INTERNAS – MANUAL (g/planta)
# =====================================================
dose_190419 = 100
dose_201005 = 100
dose_caltimag = 100

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

manual_190419 = [0, dose_190419, 0, dose_190419, 0, 0, 0, 0, 0, dose_190419, 0, dose_190419]
manual_201005 = [dose_201005, 0, dose_201005, 0, dose_201005, 0, dose_201005, 0, dose_201005, 0, dose_201005, 0]
manual_caltimag = [dose_caltimag, 0, 0, 0, 0, 0, dose_caltimag, 0, 0, 0, 0, 0]

# =====================================================
# 8️⃣ TABELA FINAL – EDITÁVEL
# =====================================================
st.header("📅 Distribuição Anual de Adubação (editável)")

if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "MAP (g/planta)": [""] * 12,
        "Cloreto de Potássio (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Sulfato de Magnésio (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": manual_190419,
        "20-10-05 (g/planta)": manual_201005,
        "Caltimag (g/planta)": manual_caltimag,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info("✏️ A tabela já vem preenchida e pode ser editada livremente.")

st.data_editor(df, use_container_width=True, num_rows="fixed")
