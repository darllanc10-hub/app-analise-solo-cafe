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
