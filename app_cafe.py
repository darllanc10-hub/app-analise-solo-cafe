import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Solo – Café", layout="wide")

# =========================
# CADASTRO DA ÁREA
# =========================
st.title("🌱 Análise de Solo – Café")

with st.expander("📋 Descrição da Área", expanded=True):
    area_ha = st.number_input("Área (ha)", 0.1, 1000.0, 10.0)
    plantas_ha = st.number_input("Plantas por ha", 1000, 10000, 3333)
    variedade = st.text_input("Variedade")
    idade = st.number_input("Idade da lavoura (anos)", 1, 50, 3)
    produtividade = st.selectbox(
        "Produtividade esperada (SC/ha)",
        [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220]
    )

# =========================
# ANÁLISE DE SOLO
# =========================
with st.expander("🧪 Análise de Solo", expanded=True):
    pH = st.number_input("pH", 3.5, 7.5, 4.0)
    V = st.number_input("V% (Saturação por bases)", 0.0, 100.0, 50.0)
    m = st.number_input("m% (Alumínio)", 0.0, 100.0, 20.0)
    CTC = st.number_input("CTC T (cmolc/dm³)", 1.0, 30.0, 4.8)

    st.subheader("Macronutrientes (mg/dm³)")
    P_rem = st.number_input("P_rem", 0.0, 60.0, 10.0)
    K_solo = st.number_input("Potássio (K)", 0.0, 300.0, 60.0)

# =========================
# CORREÇÃO COM CALCÁRIO
# =========================
V2 = 70
PRNT = 90

calcario_kg_ha = ((V2 - V) * CTC) / PRNT * 100
calcario_g_planta = (calcario_kg_ha * 1000) / plantas_ha

# Gesso: regra prática
gesso_g_planta = calcario_g_planta * 0.3

st.subheader("📊 Correção do Solo")
st.success(f"Calcário: {calcario_g_planta:.0f} g/planta")
st.success(f"Gesso: {gesso_g_planta:.0f} g/planta")
st.markdown("### ⚙️ Cálculo automático (opcional)")

if st.button("Calcular calcário e gesso automaticamente"):
    V2 = 70        # Saturação ideal para café
    PRNT = 90      # PRNT do calcário
    fator = 2      # fator agronômico que você utiliza

    if V < V2:
        # Fórmula conforme você usa no campo
        calcario_kg_planta = ((V2 - V) * CTC) / PRNT / 10000 * fator
        calcario_g_planta = calcario_kg_planta * 1000
    else:
        calcario_g_planta = 0

    # Limite máximo anual
    if calcario_g_planta > 300:
        st.warning("Dose de calcário > 300 g/planta. Recomenda-se dividir em 2 aplicações.")

    # Gesso: 30% do calcário
    if m >= 10 or V <= 30:
        gesso_g_planta = calcario_g_planta * 0.30
    else:
        gesso_g_planta = 0

    if gesso_g_planta > 200:
        st.warning("Dose de gesso > 200 g/planta. Recomenda-se dividir em 2 aplicações.")

    # Atualiza os campos existentes
    st.session_state["calcario"] = round(calcario_g_planta, 1)
    st.session_state["gesso"] = round(gesso_g_planta, 1)

st.number_input(
    "Calcário (g/planta)",
    min_value=0.0,
    key="calcario"
)

st.number_input(
    "Gesso agrícola (g/planta)",
    min_value=0.0,
    key="gesso"
)
# =========================
# TABELA 5ª APROXIMAÇÃO
# =========================
tabela_N = {
    10:220,20:250,30:280,40:310,50:340,60:370,70:395,80:420,90:445,
    100:470,110:495,120:520,130:540,140:560,150:580,160:595,
    170:615,180:635,190:655,200:675,220:675
}

tabela_K = {
    "baixo": {10:165,20:188,30:210,40:233,50:255,60:280,70:297,80:316,90:335,100:353},
    "medio": {10:110,20:125,30:140,40:155,50:170,60:185,70:198,80:210,90:222,100:235},
    "bom": {10:0,20:0,30:0,40:15,50:40,60:70,70:80,80:85,90:90,100:95}
}

# =========================
# CÁLCULO NPK
# =========================
N_necessidade = tabela_N.get(produtividade, 470)

# Nitrogênio → Ureia 46%
ureia_g_planta = (N_necessidade * 100 / 46) / plantas_ha * 1000

# Fósforo
if P_rem < 15:
    P_classe = "baixo"
elif P_rem < 30:
    P_classe = "medio"
else:
    P_classe = "bom"

P2O5_necessidade = N_necessidade * 0.5
map_g_planta = (P2O5_necessidade * 100 / 60) / plantas_ha * 1000
petrum_ml_planta = map_g_planta * 0.10

# Potássio
if K_solo < 60:
    K_classe = "baixo"
elif K_solo < 120:
    K_classe = "medio"
else:
    K_classe = "bom"

K2O_necessidade = tabela_K[K_classe].get(produtividade, 200)
kcl_g_planta = (K2O_necessidade * 100 / 60) / plantas_ha * 1000

# =========================
# DISTRIBUIÇÃO ANUAL
# =========================
meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

df = pd.DataFrame({
    "Ureia 46% (g/planta)": [ureia_g_planta/4 if m in ["Out","Nov","Dez","Jan"] else 0 for m in meses],
    "MAP (g/planta)": [map_g_planta/2 if m in ["Out","Nov"] else 0 for m in meses],
    "Petrum (ml/planta)": [petrum_ml_planta/2 if m in ["Out","Nov"] else 0 for m in meses],
    "KCl (g/planta)": [kcl_g_planta/4 if m in ["Out","Nov","Dez","Jan"] else 0 for m in meses],
}, index=meses)

st.subheader("📅 Distribuição Anual de Adubação (editável)")
st.data_editor(df, use_container_width=True)
