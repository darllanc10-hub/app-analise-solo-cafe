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
# CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")

col1, col2, col3 = st.columns(3)
with col1:
    produtor = st.text_input("Produtor")
with col2:
    propriedade = st.text_input("Propriedade")
with col3:
    municipio = st.text_input("Município")

# =====================================================
# DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")

col1, col2, col3, col4 = st.columns(4)
with col1:
    area = st.number_input("Área (ha)", min_value=0.0)
with col2:
    plantas_ha = st.number_input("Plantas por ha", min_value=0)
with col3:
    variedade = st.text_input("Variedade")
with col4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# CORREÇÃO DO SOLO
# =====================================================
st.header("🧪 Correção do Solo")

col1, col2 = st.columns(2)
with col1:
    calcario = st.number_input("Calcário (g/planta)", min_value=0.0)
with col2:
    gesso = st.number_input("Gesso agrícola (g/planta)", min_value=0.0)

# =====================================================
# MODALIDADE
# =====================================================
st.header("🚜 Modalidade de Aplicação")

modalidade = st.selectbox(
    "Escolha a modalidade principal",
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

# Definição das colunas conforme modalidade
if modalidade == "Fertirrigação":
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "MAP (g/planta)": [""] * 12,
        "Cloreto de Potássio (g/planta)": [""] * 12,
        "Nitrato de Cálcio (g/planta)": [""] * 12,
        "Sulfato de Magnésio (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }
else:  # Manual
    dados = {
        "Ureia 46% (g/planta)": [""] * 12,
        "Caltimag (g/planta)": [""] * 12,
        "Boro (ml/ha)": [""] * 12,
        "Zinco (ml/ha)": [""] * 12,
        "Matéria Orgânica (ml/ha)": [""] * 12,
    }

df = pd.DataFrame(dados, index=meses)

st.info(
    "✏️ Edite diretamente as doses na tabela. "
    "Use g/planta ou ml/ha conforme o produto. "
    "Deixe vazio quando não houver aplicação."
)

df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

# Guarda para próximas etapas (cálculo / PDF)
st.session_state["tabela_adubacao"] = df_editado
