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
# 3️⃣ ETAPA B – ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

st.markdown("### 📌 Parâmetros Químicos")

c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    m_percent = st.number_input("m% (Saturação por alumínio)", step=1.0)
with c4:
    T = st.number_input("CTC (T) cmolc/dm³", step=0.1)

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
# 4️⃣ CORREÇÃO DO SOLO – AUTOMÁTICA
# =====================================================
st.header("🧪 Correção do Solo (automática)")

PRNT = 90
V_desejado = 70

calcario_g_planta = 0
gesso_g_planta = 0

if T > 0 and plantas_ha > 0:
    calcario_g_planta = (
        (V_desejado - v_percent) * T / PRNT / 10000 * 1000 * 2
    )
    calcario_g_planta = max(calcario_g_planta, 0)

    gesso_g_planta = calcario_g_planta * 0.30

st.markdown("### 📊 Resultado da Correção")

c1, c2 = st.columns(2)

with c1:
    if calcario_g_planta > 300:
        st.warning(
            f"Calcário total: **{calcario_g_planta:.0f} g/planta** → aplicar em **2 vezes** de "
            f"{calcario_g_planta/2:.0f} g"
        )
    else:
        st.success(f"Calcário: **{calcario_g_planta:.0f} g/planta**")

with c2:
    if gesso_g_planta > 200:
        st.warning(
            f"Gesso total: **{gesso_g_planta:.0f} g/planta** → aplicar em **2 vezes** de "
            f"{gesso_g_planta/2:.0f} g"
        )
    else:
        st.success(f"Gesso: **{gesso_g_planta:.0f} g/planta**")

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

meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]

if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "MAP (g/planta)": [""] * 12,
        "Cloreto de Potássio (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Sulfato de Magnésio (g/planta)": [""] * 12,
        "Super S (ml/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""] * 12,
        "20-10-05 (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Super S (ml/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info("✏️ Edite as doses diretamente na tabela.")

st.data_editor(df, use_container_width=True, num_rows="fixed")
