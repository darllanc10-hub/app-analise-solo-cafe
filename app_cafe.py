import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="wide"
)

st.title("☕ Análise de Solo e Adubação – Café")

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
    plantas_ha = st.number_input("Plantas por ha", min_value=0)
with c3:
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# CORREÇÃO DO SOLO
# =====================================================
st.header("🧪 Correção do Solo")

c1, c2 = st.columns(2)
with c1:
    calcario = st.number_input("Calcário (g/planta)", min_value=0.0)
with c2:
    gesso = st.number_input("Gesso agrícola (g/planta)", min_value=0.0)

# =====================================================
# MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")

modalidade = st.selectbox(
    "Escolha a modalidade",
    ["Fertirrigação", "Manual"]
)

# =====================================================
# TABELA EDITÁVEL
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
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }
else:  # MANUAL
    dados = {
        "19-04-19 (g/planta)": [""] * 12,
        "20-10-05 (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Multicafé Conilon (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info(
    "✏️ Edite as doses diretamente na tabela. "
    "Deixe vazio quando não houver aplicação."
)

df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

st.session_state["tabela_adubacao"] = df_editado
# =====================================================
# ETAPA B – ANÁLISE DE SOLO
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

st.markdown("### 🌱 Macronutrientes (cmolc/dm³ ou mg/dm³)")

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

st.markdown("### 🧬 Micronutrientes (mg/dm³)")

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

# Salvar análise para uso futuro
st.session_state["analise_solo"] = {
    "pH": ph,
    "V%": v_percent,
    "m%": m_percent,
    "Ca": ca,
    "Mg": mg,
    "K": k,
    "P": p,
    "S": s,
    "B": b,
    "Zn": zn,
    "Cu": cu,
    "Mn": mn,
    "Fe": fe,
    "MO": mo
}
