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

c1, c2, c3, c4 = st.columns(4)
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
# CORREÇÃO AUTOMÁTICA DE SOLO (FUNCIONAL)
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
# TABELA DE DISTRIBUIÇÃO ANUAL (BASE – SEM CÁLCULO)
# =====================================================
st.header("📅 Distribuição Anual de Adubação")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

dados = {
    "Ureia 46% (g/planta)": ["" for _ in meses],
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

st.info("✏️ A tabela será calculada automaticamente nas próximas etapas. "
        "Por enquanto, serve como base estrutural e é totalmente editável.")

st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)
