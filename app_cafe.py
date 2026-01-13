import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# 🔢 TABELAS BASE – 5ª APROXIMAÇÃO (MODELO)
# ⚠️ SUBSTITUIR PELOS VALORES REAIS DEPOIS
# =====================================================

# Necessidade anual de NPK (kg/ha) por SC/ha
TABELA_NPK = [
    {"sc_min": 10, "sc_max": 30, "N": 120, "P": 60, "K": 120},
    {"sc_min": 31, "sc_max": 60, "N": 180, "P": 90, "K": 180},
    {"sc_min": 61, "sc_max": 100, "N": 240, "P": 120, "K": 240},
    {"sc_min": 101, "sc_max": 220, "N": 300, "P": 150, "K": 300},
]

# Micronutrientes – necessidade anual (kg/ha)
TABELA_MICROS = {
    "B": 1.5,
    "Zn": 3.0,
    "Cu": 1.0,
    "Mn": 5.0,
    "Fe": 6.0,
}

# Matéria Orgânica (L/ha)
MO_PADRAO_L_HA = 20

# Teores dos produtos (%)
PRODUTOS = {
    "Ureia": {"N": 46},
    "MAP": {"P": 61},
    "KCl": {"K": 60},
    "Super S": {"S": 12},
}

# =====================================================
# 🧮 FUNÇÕES
# =====================================================

def buscar_npk(sc):
    for faixa in TABELA_NPK:
        if faixa["sc_min"] <= sc <= faixa["sc_max"]:
            return faixa
    return None

def dose_por_planta(necessidade_kg_ha, teor_percent, plantas_ha):
    if plantas_ha == 0 or teor_percent == 0:
        return 0
    return (necessidade_kg_ha * 100) / teor_percent / plantas_ha * 1000

# =====================================================
# 📌 DADOS DA ÁREA
# =====================================================

st.header("🌱 Dados da Área")

c1, c2 = st.columns(2)
with c1:
    plantas_ha = st.number_input("Plantas por hectare", min_value=1)
with c2:
    sc_ha = st.number_input("Produtividade (sc/ha)", min_value=10, max_value=220)

# =====================================================
# 🧪 ANÁLISE DE SOLO (entrada)
# =====================================================

st.header("🧪 Análise de Solo")

c1, c2, c3 = st.columns(3)
with c1:
    b = st.number_input("Boro (B)")
with c2:
    zn = st.number_input("Zinco (Zn)")
with c3:
    cu = st.number_input("Cobre (Cu)")

# =====================================================
# ⚙️ CÁLCULO AUTOMÁTICO
# =====================================================

st.header("📊 Resultado da Correção Automática")

faixa = buscar_npk(sc_ha)

if faixa:
    n_planta = dose_por_planta(faixa["N"], PRODUTOS["Ureia"]["N"], plantas_ha)
    p_planta = dose_por_planta(faixa["P"], PRODUTOS["MAP"]["P"], plantas_ha)
    k_planta = dose_por_planta(faixa["K"], PRODUTOS["KCl"]["K"], plantas_ha)

    st.success(f"🌿 Nitrogênio (Ureia): {n_planta:.1f} g/planta/ano")
    st.success(f"🌱 Fósforo (MAP): {p_planta:.1f} g/planta/ano")
    st.success(f"🍃 Potássio (KCl): {k_planta:.1f} g/planta/ano")

# Micros
st.subheader("🧬 Micronutrientes")

for micro, necessidade in TABELA_MICROS.items():
    dose = dose_por_planta(necessidade, 10, plantas_ha)  # 10% exemplo
    st.write(f"{micro}: {dose:.2f} g/planta/ano")

# MO
st.subheader("🌾 Matéria Orgânica")
mo_planta = (MO_PADRAO_L_HA * 1000) / plantas_ha
st.write(f"Biogrow Mol: {mo_planta:.1f} ml/planta/ano")

# =====================================================
# 📅 TABELA FINAL EDITÁVEL
# =====================================================

st.header("📅 Distribuição Anual (g/ml por planta)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

df = pd.DataFrame({
    "Ureia (g/planta)": [""]*12,
    "MAP (g/planta)": [""]*12,
    "KCl (g/planta)": [""]*12,
    "Micros / Multicafé (ml/planta)": [""]*12,
    "MO (ml/planta)": [""]*12,
}, index=meses)

st.data_editor(df, use_container_width=True, num_rows="fixed")
