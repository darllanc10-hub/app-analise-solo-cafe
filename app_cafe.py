import streamlit as st
import pandas as pd

st.set_page_config(page_title="Correção de Solo – Café", layout="wide")
st.title("☕ Correção e Adubação – Café")

# =====================================================
# ÁREA E PRODUTIVIDADE
# =====================================================
st.header("🌱 Descrição da Área")

c1, c2, c3 = st.columns(3)
with c1:
    plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c2:
    produtividade = st.selectbox("Produtividade esperada (sc/ha)", list(range(10,221,10)))
with c3:
    T = st.number_input("CTC (T) – cmolc/dm³", min_value=0.0)

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3, c4 = st.columns(4)
with c1:
    v = st.number_input("V%", 0.0, 100.0)
with c2:
    m = st.number_input("m%", 0.0, 100.0)
with c3:
    p_rem = st.number_input("P_rem")
with c4:
    k_teor = st.number_input("K")

# =====================================================
# CALAGEM E GESSAGEM
# =====================================================
PRNT = 90

calcario_t_ha = max(0, (70 - v) * T / PRNT)
calcario_g_planta = (calcario_t_ha * 1_000_000) / plantas_ha

gesso_g_planta = calcario_g_planta * 0.30 if (m >= 10 or v <= 30) else 0

st.header("🧮 Correção do Solo")

st.metric("Calcário", f"{calcario_g_planta:.0f} g/planta")
st.metric("Gesso", f"{gesso_g_planta:.0f} g/planta")

# =====================================================
# NITROGÊNIO
# =====================================================
tabela_N = {
20:220,30:250,40:280,50:310,60:340,70:370,80:395,90:420,
100:445,110:470,120:495,130:520,140:540,150:560,160:580,
170:595,180:615,190:635,200:655,210:675,220:675
}

prod_ref = max([k for k in tabela_N if produtividade >= k])
necessidade_N = tabela_N[prod_ref]

ureia_g_planta = (necessidade_N * 100 / 46 / plantas_ha) * 1000

# =====================================================
# POTÁSSIO
# =====================================================
tabela_K = {
20:220,30:250,40:280,50:310,60:340,70:370,80:395,90:420,
100:445,110:470,120:495,130:520,140:540,150:560,160:580,
170:595,180:615,190:635,200:655,210:675,220:675
}

necessidade_K = tabela_K[prod_ref]

kcl_g_planta = (necessidade_K * 100 / 60 / plantas_ha) * 1000
fert26_g_planta = (necessidade_K * 100 / 26 / plantas_ha) * 1000

# =====================================================
# FÓSFORO
# =====================================================
if p_rem <= 10:
    necessidade_P = 30
elif p_rem <= 30:
    necessidade_P = 40
elif p_rem <= 60:
    necessidade_P = 50
else:
    necessidade_P = 0

map_g_planta = (necessidade_P * 100 / 60 / plantas_ha) * 1000
petrum_ml_planta = map_g_planta * 0.10

# =====================================================
# CÁLCIO E MAGNÉSIO
# =====================================================
tabela_Ca = {20:20,50:50,100:85,150:109,200:131}
tabela_Mg = {20:6.66,50:16.66,100:28.33,150:36.66,200:44.99}

prod_ca = max([k for k in tabela_Ca if produtividade >= k])
necessidade_Ca = tabela_Ca[prod_ca]
necessidade_Mg = tabela_Mg[prod_ca]

calcimag_g_planta = ((necessidade_Ca+necessidade_Mg)*100/100/plantas_ha)*1000

# =====================================================
# ENXOFRE LÍQUIDO
# =====================================================
if p_rem <= 10:
    necessidade_S = 1.92
elif p_rem <= 30:
    necessidade_S = 3.7
elif p_rem <= 60:
    necessidade_S = 7.0
else:
    necessidade_S = 0

superS_ml_planta = (necessidade_S * 1000) / plantas_ha

# =====================================================
# RESULTADOS
# =====================================================
st.header("📊 Resultado da Adubação por Planta")

st.metric("Ureia (46%)", f"{ureia_g_planta:.0f} g/planta/ano")
st.metric("KCl (60%)", f"{kcl_g_planta:.0f} g/planta/ano")
st.metric("26-00-26", f"{fert26_g_planta:.0f} g/planta/ano")
st.metric("MAP (60%)", f"{map_g_planta:.0f} g/planta/ano")
st.metric("Petrum", f"{petrum_ml_planta:.1f} ml/planta")
st.metric("Caltimag", f"{calcimag_g_planta:.0f} g/planta/ano")
st.metric("Super S", f"{superS_ml_planta:.1f} ml/planta")
