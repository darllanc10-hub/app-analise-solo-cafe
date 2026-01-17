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
# CÁLCULO AUTOMÁTICO DE NITROGÊNIO (5ª APROXIMAÇÃO)
# =====================================================

st.header("🌿 Nitrogênio – Cálculo Automático")

# Tabela oficial de necessidade de N (kg/ha)
tabela_N = {
    20:220, 30:250, 40:280, 50:310, 60:340, 70:370, 80:395, 90:420,
    100:445, 110:470, 120:495, 130:520, 140:540, 150:560, 160:580,
    170:595, 180:615, 190:635, 200:655, 210:675, 220:675
}

# pega o valor mais próximo da produtividade escolhida
prod_ref = max([k for k in tabela_N if produtividade >= k])
necessidade_N = tabela_N[prod_ref]

# Produto comercial utilizado
ureia_percent = 46

# Conversão para ureia kg/ha
ureia_kg_ha = necessidade_N * 100 / ureia_percent

# Conversão para g/planta/ano
ureia_g_planta = (ureia_kg_ha / plantas_ha) * 1000

st.metric("Necessidade de N", f"{necessidade_N} kg/ha")
st.metric("Ureia recomendada", f"{ureia_g_planta:.0f} g/planta/ano")

st.info("📌 Esse valor é a dose TOTAL anual por planta. Distribua nos meses desejados.")
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
        return "2 aplicações (50% agora e 50% após 6 meses)"
    elif valor > 0:
        return "Aplicação única"
    else:
        return "-"

c1, c2 = st.columns(2)
with c1:
    st.metric("Calcário", f"{calcario_g:.0f} g/planta")
    st.caption(parcela(calcario_g, 300))
with c2:
    st.metric("Gesso", f"{gesso_g:.0f} g/planta" if gesso_g > 0 else "Não recomendado")
    if gesso_g > 0:
        st.caption(parcela(gesso_g, 200))

# =====================================================
# NECESSIDADES – VISUAL (TESTE)
# =====================================================
st.header("📊 Necessidade Anual (visual para conferência)")

# --- TABELA DE NITROGÊNIO (kg/ha)
tabela_N = {
    10: 220, 20: 220, 30: 250, 40: 280, 50: 310,
    60: 340, 70: 370, 80: 395, 90: 420,
    100: 445, 110: 470, 120: 495, 130: 520,
    140: 540, 150: 560, 160: 580, 170: 595,
    180: 615, 190: 635, 200: 655, 210: 675, 220: 675
}

necessidade_N = tabela_N.get(produtividade, 0)

# Conversão para ureia 46%
ureia_g_planta = 0
if plantas_ha > 0:
    ureia_g_planta = necessidade_N * 100 / 46 / plantas_ha * 1000

# =====================================================
# TABELA FINAL (SÓ PARA VISUALIZAR)
# =====================================================
df = pd.DataFrame({
    "Nutriente": ["Nitrogênio (Ureia 46%)"],
    "Dose anual": [f"{ureia_g_planta:.1f} g/planta"]
})

st.table(df)

st.info(
    "⚠️ Esta tabela é APENAS para conferência visual.\n"
    "Nada foi distribuído por mês ainda.\n"
    "Se os números baterem, avançamos. Se não, voltamos exatamente como estava."
)
