import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Correção de Solo – Café", layout="wide")
st.title("☕ Correção de Solo – Café")

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

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    area = st.number_input("Área (ha)", min_value=0.0)
with c2:
    plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c3:
    produtividade = st.selectbox(
        "Produtividade esperada (sc/ha)",
        list(range(10, 221, 10))
    )
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)
with c5:
    necessidade_n = st.number_input(
        "Necessidade de Nitrogênio (kg/ha)",
        min_value=0.0,
        help="Valor retirado da tabela técnica (5ª aproximação)"
    )

variedade = st.text_input("Variedade")

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH", step=0.1)
with c2:
    v = st.number_input("V% (Saturação por bases)", min_value=0.0, max_value=100.0)
with c3:
    m = st.number_input("m% (Saturação por Alumínio)", min_value=0.0, max_value=100.0)
with c4:
    T = st.number_input("CTC a pH 7 (T) – cmolc/dm³", min_value=0.0)

# =====================================================
# CORREÇÃO DE SOLO (MANTIDA)
# =====================================================
st.header("🧮 Correção do Solo")

PRNT = 90
calcario_g = 0.0
gesso_g = 0.0

if T > 0 and plantas_ha > 0 and v < 70:
    calcario_t_ha = (70 - v) * T / PRNT
    calcario_g = (calcario_t_ha * 1_000_000) / plantas_ha

    if m >= 10 or v <= 30:
        gesso_g = calcario_g * 0.30

def parcela(valor, limite):
    if valor > limite:
        return "Aplicar em 2 parcelas (50% agora e 50% após 6 meses)"
    elif valor > 0:
        return "Aplicação única"
    else:
        return "-"

c1, c2 = st.columns(2)
with c1:
    st.metric("Calcário recomendado", f"{calcario_g:.0f} g/planta")
    st.caption(parcela(calcario_g, 300))
with c2:
    if gesso_g > 0:
        st.metric("Gesso agrícola recomendado", f"{gesso_g:.0f} g/planta")
        st.caption(parcela(gesso_g, 200))
    else:
        st.metric("Gesso agrícola", "Não recomendado")

# =====================================================
# TABELA DE ADUBAÇÃO (COM NITROGÊNIO AUTOMÁTICO)
# =====================================================
st.header("📅 Distribuição Anual de Adubação")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

# ---- CÁLCULO CORRETO DA UREIA ----
ureia_g_planta_ano = 0.0
if necessidade_n > 0 and plantas_ha > 0:
    ureia_g_planta_ano = (
        necessidade_n * 100 / 46 / plantas_ha * 1000
    )

ureia_mensal = ureia_g_planta_ano / 12 if ureia_g_planta_ano > 0 else ""

dados = {
    "Ureia 46% (g/planta)": [f"{ureia_mensal:.1f}" if ureia_mensal else "" for _ in meses],
    "MAP / Petrum (g ou ml/planta)": ["" for _ in meses],
    "Cloreto de Potássio (g/planta)": ["" for _ in meses],
    "Cálcio (g/planta)": ["" for _ in meses],
    "Magnésio (g/planta)": ["" for _ in meses],
    "Super S – Enxofre (ml/planta)": ["" for _ in meses],
    "Boro (ml/planta)": ["" for _ in meses],
    "Zinco (ml/planta)": ["" for _ in meses],
    "Multicafé Conilon (ml/planta)": ["" for _ in meses],
    "Matéria Orgânica (ml/planta)": ["" for _ in meses],
}

df = pd.DataFrame(dados, index=meses)

st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

st.info(
    "📌 Nitrogênio calculado a partir da NECESSIDADE (kg/ha) informada.\n"
    "📌 Conversão automática para ureia 46% em g/planta/ano.\n"
    "📌 Distribuição mensal igual — ajuste os meses como desejar."
)
