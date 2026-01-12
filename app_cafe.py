import streamlit as st
import pandas as pd

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Análise de Solo – Café",
    layout="centered"
)

st.title("🌱 Análise de Solo – Café")

# =============================
# DADOS DO PRODUTOR / ÁREA
# =============================
st.header("👨‍🌾 Identificação da Área")

produtor = st.text_input("Produtor")
area = st.text_input("Área / Talhão")
cultura = st.selectbox("Cultura", ["Café Conilon", "Café Arábica"])
plantas_ha = st.number_input("Plantas por hectare", min_value=1000, value=3000, step=100)

# =============================
# PARÂMETROS QUÍMICOS
# =============================
st.header("🧪 Parâmetros Químicos do Solo")

ph = st.number_input("pH (H₂O)", value=5.2, step=0.1)
v_atual = st.number_input("V% atual", value=45.0, step=1.0)
v_desejado = st.number_input("V% desejado", value=60.0, step=1.0)

ca = st.number_input("Cálcio (Ca) cmolc/dm³", value=1.5, step=0.1)
mg = st.number_input("Magnésio (Mg) cmolc/dm³", value=0.4, step=0.1)
al = st.number_input("Alumínio (Al) cmolc/dm³", value=0.2, step=0.1)

st.header("🌾 Micronutrientes (mg/dm³)")
fe = st.number_input("Ferro (Fe)", value=50.0)
zn = st.number_input("Zinco (Zn)", value=2.0)
cu = st.number_input("Cobre (Cu)", value=1.0)
mn = st.number_input("Manganês (Mn)", value=20.0)
b = st.number_input("Boro (B)", value=0.3)

st.header("🌱 Matéria Orgânica")
mo = st.number_input("Matéria Orgânica (%)", value=1.8, step=0.1)

# =============================
# MODALIDADE DE APLICAÇÃO
# =============================
st.header("🚜 Modalidade de Aplicação")
modalidade = st.selectbox(
    "Escolha a modalidade",
    ["Manual", "Fertirrigação"]
)

# =============================
# CÁLCULO DE CALAGEM E GESSAGEM
# =============================
st.header("🧮 Cálculo de Calagem e Gessagem")

calcario_t_ha = 0.0
gesso_t_ha = 0.0

if v_atual < v_desejado:
    calcario_t_ha = round((v_desejado - v_atual) * 0.05, 2)

if ca < 2.0:
    gesso_t_ha = 1.0

kg_calcario_ha = calcario_t_ha * 1000
kg_gesso_ha = gesso_t_ha * 1000

g_calcario_planta = (kg_calcario_ha * 1000) / plantas_ha if plantas_ha > 0 else 0
g_gesso_planta = (kg_gesso_ha * 1000) / plantas_ha if plantas_ha > 0 else 0

# =============================
# RESULTADO FINAL DA CORREÇÃO
# =============================
st.subheader("📊 Resultado da Correção do Solo")

col1, col2 = st.columns(2)

with col1:
    st.success("🪨 Calcário")
    st.write(f"**Dose:** {calcario_t_ha:.2f} t/ha")
    st.write(f"{kg_calcario_ha:.0f} kg/ha")
    st.write(f"{g_calcario_planta:.0f} g por planta")

with col2:
    st.warning("🟡 Gesso agrícola")
    st.write(f"**Dose:** {gesso_t_ha:.2f} t/ha")
    st.write(f"{kg_gesso_ha:.0f} kg/ha")
    st.write(f"{g_gesso_planta:.0f} g por planta")

# =============================
# ADUBOS (EDITÁVEIS NA TABELA)
# =============================
st.header("🧾 Seleção e Ajuste de Adubos")

adubos = {
    "Ureia 46%": {"dose": 10, "unidade": "g/planta", "modalidade": "Fertirrigação"},
    "19-04-19": {"dose": 15, "unidade": "g/planta", "modalidade": "Manual"},
    "20-10-05": {"dose": 20, "unidade": "g/planta", "modalidade": "Manual"},
    "MAP": {"dose": 5, "unidade": "g/planta", "modalidade": "Fertirrigação"},
    "Cloreto de Potássio": {"dose": 8, "unidade": "g/planta", "modalidade": "Fertirrigação"},
    "Caltimag": {"dose": 10, "unidade": "g/planta", "modalidade": "Manual"},
    "Multicafé Conilon": {"dose": 15, "unidade": "g/planta", "modalidade": "Manual"}
}

adubos_ativos = {}

for nome, info in adubos.items():
    if info["modalidade"] != modalidade:
        continue

    col1, col2 = st.columns([3, 2])

    with col1:
        ativo = st.checkbox(nome, value=True, key=f"chk_{nome}")

    with col2:
        dose = st.number_input(
            f"Dose ({info['unidade']})",
            value=float(info["dose"]),
            step=1.0,
            key=f"dose_{nome}"
        )

    if ativo:
        adubos_ativos[nome] = {
            "dose": dose,
            "unidade": info["unidade"]
        }

# =============================
# TABELA DE DISTRIBUIÇÃO
# =============================
st.header("📅 Tabela de Distribuição Anual")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

tabela = pd.DataFrame(index=meses)

for nome, info in adubos_ativos.items():
    tabela[nome] = [f"{info['dose']} {info['unidade']}" for _ in meses]

st.dataframe(tabela, use_container_width=True)

# =============================
# UPLOAD DA FOTO (ETAPA C – PREPARADO)
# =============================
st.header("📸 Foto da Análise de Solo (opcional)")
st.file_uploader(
    "Envie a foto ou PDF da análise (em breve leitura automática)",
    type=["jpg", "png", "jpeg", "pdf"]
)

st.info("🔜 Em breve: leitura automática da análise via imagem (OCR).")
