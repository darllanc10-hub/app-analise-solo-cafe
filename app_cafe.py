import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURAÇÃO GERAL
# =====================================================
st.set_page_config(page_title="Análise de Solo – Café", layout="wide")
st.title("☕ Análise de Solo e Adubação – Café")

# =====================================================
# FUNÇÕES
# =====================================================

def dose_por_planta(necessidade_kg_ha, teor_percent, plantas_ha):
    if plantas_ha == 0 or teor_percent == 0:
        return 0
    return (necessidade_kg_ha * 100) / teor_percent / plantas_ha * 1000

def distribuir(dose_anual, meses):
    if meses == 0:
        return 0
    return dose_anual / meses

# =====================================================
# 1️⃣ CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")
c1, c2, c3 = st.columns(3)
with c1: produtor = st.text_input("Produtor")
with c2: propriedade = st.text_input("Propriedade")
with c3: municipio = st.text_input("Município")

# =====================================================
# 2️⃣ DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")
c1, c2, c3, c4 = st.columns(4)
with c1: area = st.number_input("Área (ha)", min_value=0.0)
with c2: plantas_ha = st.number_input("Plantas por ha", min_value=1)
with c3: variedade = st.text_input("Variedade")
with c4: idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 3️⃣ PRODUTIVIDADE
# =====================================================
st.header("📈 Produtividade")
sc_ha = st.number_input("Produtividade (sc/ha)", min_value=10, max_value=220)

# =====================================================
# 4️⃣ ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

c1, c2, c3 = st.columns(3)
with c1: ph = st.number_input("pH", step=0.1)
with c2: v_percent = st.number_input("V%", step=1.0)
with c3: m_percent = st.number_input("m%", step=1.0)

st.subheader("Macronutrientes")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: ca = st.number_input("Ca", step=0.1)
with c2: mg = st.number_input("Mg", step=0.1)
with c3: k = st.number_input("K", step=0.1)
with c4: p = st.number_input("P", step=0.1)
with c5: s = st.number_input("S", step=0.1)

st.subheader("Micronutrientes")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: b = st.number_input("B", step=0.1)
with c2: zn = st.number_input("Zn", step=0.1)
with c3: cu = st.number_input("Cu", step=0.1)
with c4: mn = st.number_input("Mn", step=0.1)
with c5: fe = st.number_input("Fe", step=0.1)

mo = st.number_input("Matéria Orgânica (%)", step=0.1)

# =====================================================
# 5️⃣ MODALIDADE
# =====================================================
st.header("🚜 Modalidade")
modalidade = st.selectbox("Modalidade de aplicação", ["Fertirrigação", "Manual"])

# =====================================================
# 6️⃣ TABELA ANUAL
# =====================================================
st.header("📅 Distribuição Anual (g/ml por planta)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

if modalidade == "Fertirrigação":
    dados = {
        "Ureia (g/planta)": [""]*12,
        "MAP (g/planta)": [""]*12,
        "KCl (g/planta)": [""]*12,
        "Super S (ml/planta)": [""]*12,
        "Multicafé Conilon (ml/planta)": [""]*12,
        "Biogrow Mol (ml/planta)": [""]*12,
    }
else:
    dados = {
        "19-04-19 (g/planta)": [""]*12,
        "20-10-05 (g/planta)": [""]*12,
        "Caltimag (g/planta)": [""]*12,
        "Multicafé Conilon (ml/planta)": [""]*12,
        "Biogrow Mol (ml/planta)": [""]*12,
    }

df = pd.DataFrame(dados, index=meses)
df_editado = st.data_editor(df, use_container_width=True, num_rows="fixed")

# =====================================================
# 7️⃣ BOTÃO DE CÁLCULO
# =====================================================
st.header("⚙️ Cálculo")

if st.button("Calcular recomendação"):
    # ====== MODELO DE NECESSIDADE ANUAL (SUBSTITUIR PELA 5ª APROXIMAÇÃO REAL) ======
    necessidade = {
        "N": 200,
        "P": 120,
        "K": 200,
        "MO": 20,   # L/ha
    }

    ureia = dose_por_planta(necessidade["N"], 46, plantas_ha)
    map_ = dose_por_planta(necessidade["P"], 61, plantas_ha)
    kcl = dose_por_planta(necessidade["K"], 60, plantas_ha)

    mo_planta = (necessidade["MO"] * 1000) / plantas_ha

    meses_aplicacao = 6  # distribuição automática

    for i in range(12):
        if i < meses_aplicacao:
            if modalidade == "Fertirrigação":
                df_editado.iloc[i, 0] = round(distribuir(ureia, meses_aplicacao), 2)
                df_editado.iloc[i, 1] = round(distribuir(map_, meses_aplicacao), 2)
                df_editado.iloc[i, 2] = round(distribuir(kcl, meses_aplicacao), 2)
                df_editado.iloc[i, 5] = round(distribuir(mo_planta, meses_aplicacao), 2)
            else:
                df_editado.iloc[i, 0] = round(distribuir(ureia, meses_aplicacao), 2)
                df_editado.iloc[i, 1] = round(distribuir(map_, meses_aplicacao), 2)
                df_editado.iloc[i, 4] = round(distribuir(mo_planta, meses_aplicacao), 2)

    st.success("✅ Recomendação calculada e distribuída automaticamente.")
