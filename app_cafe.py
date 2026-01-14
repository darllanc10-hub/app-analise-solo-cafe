import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO GERAL
# =====================================================
st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")
c1, c2, c3 = st.columns(3)
produtor = c1.text_input("Produtor")
propriedade = c2.text_input("Propriedade")
municipio = c3.text_input("Município")

# =====================================================
# DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")
c1, c2, c3, c4 = st.columns(4)
area = c1.number_input("Área (ha)", min_value=0.0)
plantas_ha = c2.number_input("Plantas por ha", min_value=0)
variedade = c3.text_input("Variedade")
idade = c4.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# PRODUTIVIDADE
# =====================================================
st.header("📦 Produtividade Esperada")
sc_ha = st.selectbox(
    "Sacas por hectare (SC/ha)",
    options=list(range(10, 230, 10))
)

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3 = st.columns(3)
ph = c1.number_input("pH", step=0.1)
v_percent = c2.number_input("V%", step=1.0)
m_percent = c3.number_input("m%", step=1.0)

c1, c2, c3, c4, c5 = st.columns(5)
ca = c1.number_input("Ca", step=0.1)
mg = c2.number_input("Mg", step=0.1)
k = c3.number_input("K", step=0.1)
p = c4.number_input("P", step=0.1)
s = c5.number_input("S", step=0.1)

mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# CORREÇÃO DO SOLO
# =====================================================
st.header("🧪 Correção do Solo")

if plantas_ha > 0:
    calcario_t_ha = 3 if v_percent < 60 else 0
    gesso_t_ha = 0.9 if ca < 4 else 0

    calc_g_planta = (calcario_t_ha * 1_000_000) / plantas_ha
    gesso_g_planta = (gesso_t_ha * 1_000_000) / plantas_ha

    if calc_g_planta > 300:
        st.success(
            f"🪨 Calcário: {calc_g_planta:.0f} g/planta/ano "
            f"(aplicar em 2x de {calc_g_planta/2:.0f} g)"
        )
    else:
        st.success(f"🪨 Calcário: {calc_g_planta:.0f} g/planta")

    if gesso_g_planta > 200:
        st.success(
            f"🧂 Gesso: {gesso_g_planta:.0f} g/planta/ano "
            f"(aplicar em 2x de {gesso_g_planta/2:.0f} g)"
        )
    else:
        st.success(f"🧂 Gesso: {gesso_g_planta:.0f} g/planta")
st.markdown("### 🧬 Micronutrientes (análise de solo)")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    b = st.number_input("Boro (B) – mg/dm³", step=0.1)
with c2:
    zn = st.number_input("Zinco (Zn) – mg/dm³", step=0.1)
with c3:
    cu = st.number_input("Cobre (Cu) – mg/dm³", step=0.1)
with c4:
    mn = st.number_input("Manganês (Mn) – mg/dm³", step=0.1)
with c5:
    fe = st.number_input("Ferro (Fe) – mg/dm³", step=0.1)

st.session_state["micros_analise"] = {
    "B": b,
    "Zn": zn,
    "Cu": cu,
    "Mn": mn,
    "Fe": fe
}
# =====================================================
# NPK – 5ª APROXIMAÇÃO (BASE)
# =====================================================
st.header("🧮 Correção Automática de NPK")

# Necessidade base (AJUSTÁVEL)
necessidade_npk = {
    "N": sc_ha * 3.2,
    "P2O5": sc_ha * 1.2,
    "K2O": sc_ha * 3.5
}

# Fontes
fontes = {
    "N": {"Ureia": 0.46},
    "P2O5": {"MAP": 0.52},
    "K2O": {"KCl": 0.60}
}

if plantas_ha > 0:
    st.info("📌 Doses calculadas em g/planta/ano")

    n_g = (necessidade_npk["N"] * 100) / 0.46 / plantas_ha * 1000
    p_g = (necessidade_npk["P2O5"] * 100) / 0.52 / plantas_ha * 1000
    k_g = (necessidade_npk["K2O"] * 100) / 0.60 / plantas_ha * 1000

    st.success(f"🌿 Nitrogênio (Ureia): {n_g:.1f} g/planta/ano")
    st.success(f"🌱 Fósforo (MAP): {p_g:.1f} g/planta/ano")
    st.success(f"🍃 Potássio (KCl): {k_g:.1f} g/planta/ano")

# =====================================================
# TABELA FINAL
# =====================================================
st.header("📅 Distribuição Anual de Adubação (editável)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

df = pd.DataFrame({
    "Ureia (g/planta)": [""]*12,
    "MAP (g/planta)": [""]*12,
    "KCl (g/planta)": [""]*12,
    "Super S (ml/planta)": [""]*12,
    "Multicafé Conilon (ml/planta)": [""]*12
}, index=meses)

st.data_editor(df, use_container_width=True)
