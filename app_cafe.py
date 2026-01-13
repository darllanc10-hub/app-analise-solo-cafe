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
    plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c3:
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# PRODUTIVIDADE
# =====================================================
st.header("📈 Produtividade Esperada")

sc_ha = st.selectbox(
    "Produtividade (sacas por hectare)",
    list(range(10, 230, 10))
)

# =====================================================
# 3️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

st.markdown("### 📌 Parâmetros Químicos")

c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    m_percent = st.number_input("m% (Saturação por alumínio)", step=1.0)

st.markdown("### 🌱 Macronutrientes")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    ca = st.number_input("Cálcio (Ca)", step=0.1)
with c2:
    mg = st.number_input("Magnésio (Mg)", step=0.1)
with c3:
    k = st.number_input("Potássio (K)", step=0.1)
with c4:
    p = st.number_input("Fósforo (P)", step=0.1)
with c5:
    s = st.number_input("Enxofre (S)", step=0.1)

st.markdown("### 🧬 Micronutrientes")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    b = st.number_input("Boro (B)", step=0.1)
with c2:
    zn = st.number_input("Zinco (Zn)", step=0.1)
with c3:
    cu = st.number_input("Cobre (Cu)", step=0.1)
with c4:
    mn = st.number_input("Manganês (Mn)", step=0.1)
with c5:
    fe = st.number_input("Ferro (Fe)", step=0.1)

st.markdown("### 🌾 Matéria Orgânica")
mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO – CALCÁRIO E GESSO
# =====================================================
st.header("🧪 Correção do Solo")

def calcular_calcario_gesso(v_atual, m_atual, plantas_ha):
    v_desejado = 70
    limite_t_ha = 3

    if v_atual >= v_desejado:
        return 0, 0

    dose_t_ha = min((v_desejado - v_atual) * 0.1, limite_t_ha)
    calcario_kg_ha = dose_t_ha * 1000

    if v_atual <= 30 or m_atual >= 10:
        gesso_kg_ha = calcario_kg_ha * 0.30
    else:
        gesso_kg_ha = 0

    calcario_g_planta = (calcario_kg_ha * 1000) / plantas_ha
    gesso_g_planta = (gesso_kg_ha * 1000) / plantas_ha

    return round(calcario_g_planta, 1), round(gesso_g_planta, 1)

calcario_planta, gesso_planta = calcular_calcario_gesso(
    v_percent, m_percent, plantas_ha
)

if calcario_planta > 0:
    st.success(f"🪨 Calcário: {calcario_planta} g/planta")
else:
    st.info("🪨 Calcário: não necessário")

if gesso_planta > 0:
    st.success(f"🧂 Gesso agrícola: {gesso_planta} g/planta")
else:
    st.info("🧂 Gesso agrícola: não necessário")

# =====================================================
# TABELA BASE – 5ª APROXIMAÇÃO (INTERNA)
# =====================================================
tabela_5a = {
    10:  {"N": 20},
    20:  {"N": 40},
    30:  {"N": 60},
    40:  {"N": 80},
    50:  {"N": 100},
    60:  {"N": 120},
    70:  {"N": 140},
    80:  {"N": 160},
    90:  {"N": 180},
    100: {"N": 200},
    120: {"N": 240},
    140: {"N": 280},
    160: {"N": 320},
    180: {"N": 360},
    200: {"N": 400},
    220: {"N": 440},
}

# =====================================================
# CÁLCULO AUTOMÁTICO – NITROGÊNIO
# =====================================================
dose_n_planta = 0
if plantas_ha > 0:
    necessidade_n = tabela_5a.get(sc_ha, {}).get("N", 0)
    dose_n_planta = round((necessidade_n * 100) / 46 / plantas_ha * 1000, 1)

st.info(f"🔬 Nitrogênio calculado: {dose_n_planta} g/planta/ano")

# =====================================================
# 5️⃣ MODALIDADE DE APLICAÇÃO
# =====================================================
st.header("🚜 Modalidade de Aplicação")

modalidade = st.selectbox(
    "Escolha a modalidade",
    ["Fertirrigação", "Manual"]
)

# =====================================================
# 6️⃣ TABELA EDITÁVEL – CRONOGRAMA
# =====================================================
st.header("📅 Distribuição Anual de Adubação (editável)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "MAP (g/planta)": [""] * 12,
        "Cloreto de Potássio (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Sulfato de Magnésio (g/planta)": [""] * 12,
        "Super S (ml/planta)": [""] * 12,
        "Multicafé Conilon (ml/planta)": [""] * 12,
        "Matéria Orgânica (ml/planta)": [""] * 12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""] * 12,
        "20-10-05 (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Super S (ml/planta)": [""] * 12,
        "Multicafé Conilon (ml/planta)": [""] * 12,
        "Matéria Orgânica (ml/planta)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info("✏️ Edite as doses diretamente na tabela. Célula vazia = sem aplicação.")

st.data_editor(df, use_container_width=True, num_rows="fixed")
