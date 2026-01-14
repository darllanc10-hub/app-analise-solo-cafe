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
# 3️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v_percent = st.number_input("V% (Saturação por bases)", step=1.0)
with c3:
    t_ctc = st.number_input("CTC T (cmolc/dm³)", step=0.1)

# =====================================================
# 4️⃣ CORREÇÃO DO SOLO (CÁLCULO AUTOMÁTICO)
# =====================================================
st.header("🧪 Correção do Solo (automática)")

PRNT = 90  # %
V_DESEJADO = 70

calcario_g_planta = 0
gesso_g_planta = 0

if plantas_ha > 0 and t_ctc > 0:
    # ---- CÁLCULO DO CALCÁRIO ----
    # Resultado da fórmula = kg/planta
    calcario_kg_planta = ((V_DESEJADO - v_percent) * t_ctc / PRNT) / 10000 * 1000 * 2
    calcario_g_planta = max(calcario_kg_planta * 1000, 0)

    # ---- CÁLCULO DO GESSO (30% do calcário como referência técnica) ----
    gesso_g_planta = calcario_g_planta * 0.3

st.markdown("### 📌 Resultado da Correção")

c1, c2 = st.columns(2)

with c1:
    if calcario_g_planta > 300:
        st.success(
            f"Calcário: {calcario_g_planta:.0f} g/planta (dose anual)\n\n"
            f"➡ Aplicar 2x de {calcario_g_planta/2:.0f} g/planta"
        )
    else:
        st.success(f"Calcário: {calcario_g_planta:.0f} g/planta")

with c2:
    if gesso_g_planta > 200:
        st.success(
            f"Gesso: {gesso_g_planta:.0f} g/planta (dose anual)\n\n"
            f"➡ Aplicar 2x de {gesso_g_planta/2:.0f} g/planta"
        )
    else:
        st.success(f"Gesso: {gesso_g_planta:.0f} g/planta")

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
        "Cloreto de K (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Super S (ml/planta)": [""] * 12,
        "Multicafé Conilon (ml/planta)": [""] * 12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""] * 12,
        "20-10-05 (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Multicafé Conilon (ml/planta)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info("✏️ Edite livremente as doses. Célula vazia = sem aplicação.")

df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

st.session_state["tabela_adubacao"] = df_editado
