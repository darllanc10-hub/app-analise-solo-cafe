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
# 3️⃣ ANÁLISE DE SOLO – PARÂMETROS GERAIS
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
    ctc_t = st.number_input("CTC T (cmolc/dm³)", step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO – CÁLCULO AUTOMÁTICO
# =====================================================
st.header("🧪 Correção do Solo")

PRNT = 90
V_DESEJADO = 70

calcario_g_planta = 0.0
gesso_g_planta = 0.0

if plantas_ha > 0 and ctc_t > 0:
    # Necessidade de calcário em t/ha (fórmula agronômica correta)
    nc_t_ha = (V_DESEJADO - v_percent) * ctc_t * 0.1 / PRNT

    if nc_t_ha < 0:
        nc_t_ha = 0

    # Converter para g/planta
    calcario_g_planta = (nc_t_ha * 1_000_000) / plantas_ha

    # Gesso = 30% do calcário
    gesso_g_planta = calcario_g_planta * 0.30

# Parcelamento automático
parcelas_calcario = 1
parcelas_gesso = 1

if calcario_g_planta > 300:
    parcelas_calcario = 2

if gesso_g_planta > 200:
    parcelas_gesso = 2

# =====================================================
# 5️⃣ RESULTADO DA CORREÇÃO
# =====================================================
st.subheader("📊 Resultado da Correção")

st.success(
    f"🪨 **Calcário:** {calcario_g_planta:.1f} g/planta "
    f"({parcelas_calcario} aplicação(ões) de {calcario_g_planta/parcelas_calcario:.1f} g)"
)

st.success(
    f"🧂 **Gesso agrícola:** {gesso_g_planta:.1f} g/planta "
    f"({parcelas_gesso} aplicação(ões) de {gesso_g_planta/parcelas_gesso:.1f} g)"
)

# =====================================================
# 6️⃣ MODALIDADE DE APLICAÇÃO
# =====================================================
st.header("🚜 Modalidade de Aplicação")

modalidade = st.selectbox(
    "Escolha a modalidade",
    ["Fertirrigação", "Manual"]
)

# =====================================================
# 7️⃣ TABELA EDITÁVEL – CRONOGRAMA (SEM ALTERAÇÕES)
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
        "KCl (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Sulfato de Magnésio (g/planta)": [""] * 12,
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

st.info("✏️ Edite as doses diretamente na tabela.")

st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)
