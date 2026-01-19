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
    plantas_ha = st.number_input("Plantas por ha", min_value=1, value=5000)
with c3:
    variedade = st.text_input("Variedade")
with c4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# ANÁLISE DE SOLO
# =====================================================
st.header("🧪 Análise de Solo")

col1, col2, col3, col4 = st.columns(4)
with col1:
    ph = st.number_input("pH", step=0.1, value=5.0)
with col2:
    v = st.number_input("V% (Saturação por bases)", min_value=0.0, max_value=100.0, value=50.0)
with col3:
    m = st.number_input("m% (Saturação por Alumínio)", min_value=0.0, max_value=100.0, value=5.0)
with col4:
    T = st.number_input("CTC a pH 7 (T) – cmolc/dm³", min_value=0.0, value=5.0)

col1, col2, col3, col4 = st.columns(4)
with col1:
    p_rem = st.number_input("P-rem (mg/L)", min_value=0.0, value=20.0)
with col2:
    p_mehlich = st.number_input("P Mehlich (mg/dm³)", min_value=0.0, value=5.0)
with col3:
    k_solo = st.number_input("K (mg/dm³)", min_value=0.0, value=100.0)
with col4:
    mo = st.number_input("Matéria Orgânica (dag/kg)", min_value=0.0, value=2.0)

col1, col2, col3 = st.columns(3)
with col1:
    ca = st.number_input("Ca (cmolc/dm³)", min_value=0.0, value=2.0)
with col2:
    mg = st.number_input("Mg (cmolc/dm³)", min_value=0.0, value=0.5)
with col3:
    s = st.number_input("S (mg/dm³)", min_value=0.0, value=5.0)

st.subheader("Micronutrientes")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    b = st.number_input("B (mg/dm³)", min_value=0.0, value=0.3, step=0.1)
with col2:
    cu = st.number_input("Cu (mg/dm³)", min_value=0.0, value=0.5, step=0.1)
with col3:
    zn = st.number_input("Zn (mg/dm³)", min_value=0.0, value=3.0, step=0.1)
with col4:
    fe = st.number_input("Fe (mg/dm³)", min_value=0.0, value=20.0, step=1.0)
with col5:
    mn = st.number_input("Mn (mg/dm³)", min_value=0.0, value=10.0, step=1.0)

textura = st.selectbox("Textura do Solo", ["Argiloso", "Médio", "Arenoso"])
produtividade = st.number_input("Expectativa de Produtividade (sc/ha)", min_value=20, max_value=210, value=60, step=10)

# =====================================================
# FUNÇÕES
# =====================================================

def classificar_k(k_solo):
    if k_solo < 60:
        return "Baixo"
    elif k_solo < 120:
        return "Médio"
    elif k_solo < 200:
        return "Bom"
    else:
        return "Muito Bom"

def get_n_dose(prod):
    tabela = {20:220,30:250,40:280,50:310,60:340,70:370,80:395,90:420,100:445,110:470,120:495,130:520,140:540,150:560,160:580,170:595,180:615,190:635,200:655,210:675}
    chave = min(tabela.keys(), key=lambda x: abs(x-prod))
    return tabela[chave]

# =====================================================
# CÁLCULOS
# =====================================================

classe_k = classificar_k(k_solo)
dose_n = get_n_dose(produtividade)

PRNT = 90
calcario = 0.0
gesso = 0.0

if T > 0 and v < 70:
    calcario = ((70 - v) * T / PRNT / 10000 * 1000 * 2)
    if m >= 10 or v <= 30:
        gesso = calcario * 0.30

# =====================================================
# RESULTADOS
# =====================================================
st.header("📊 Resultados")

c1, c2 = st.columns(2)
with c1:
    st.metric("Calcário recomendado", f"{calcario*1000:.0f} g/planta")
with c2:
    st.metric("Gesso agrícola", f"{gesso*1000:.0f} g/planta")

st.subheader("Adubação")
st.metric("Nitrogênio (N)", f"{dose_n} g/planta")
st.metric("Potássio (K₂O)", f"Classe {classe_k}")

st.info("Aplicar adubação conforme análise e parcelar durante período chuvoso.")
