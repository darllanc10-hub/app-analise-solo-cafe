import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="Análise de Solo - Café",
    layout="wide"
)

st.title("☕ Análise de Solo – Café")

# =====================================================
# 📌 CADASTRO DO PRODUTOR
# =====================================================
st.header("👨‍🌾 Cadastro do Produtor")

col1, col2, col3 = st.columns(3)

with col1:
    produtor = st.text_input("Nome do produtor")
with col2:
    propriedade = st.text_input("Propriedade")
with col3:
    municipio = st.text_input("Município")

# =====================================================
# 🌱 DESCRIÇÃO DA ÁREA
# =====================================================
st.header("🌱 Descrição da Área")

col1, col2, col3, col4 = st.columns(4)

with col1:
    area_ha = st.number_input("Área (ha)", min_value=0.0)
with col2:
    plantas_ha = st.number_input("Plantas por ha", min_value=0)
with col3:
    variedade = st.text_input("Variedade")
with col4:
    idade = st.number_input("Idade da lavoura (anos)", min_value=0)

# =====================================================
# 🧪 CORREÇÃO DO SOLO
# =====================================================
st.header("🧪 Correção do Solo")

col1, col2 = st.columns(2)

with col1:
    calcario = st.number_input("Calcário (g por planta)", min_value=0.0)
    if calcario > 0:
        st.success(f"Calcário: {calcario:.0f} g por planta")

with col2:
    gesso = st.number_input("Gesso agrícola (g por planta)", min_value=0.0)
    if gesso > 0:
        st.warning(f"Gesso agrícola: {gesso:.0f} g por planta")

# =====================================================
# 🚜 MODALIDADE DE APLICAÇÃO
# =====================================================
st.header("🚜 Modalidade de Aplicação")

tipo_aplicacao = st.radio(
    "Escolha a modalidade:",
    ["Manual", "Fertirrigação"]
)

# =====================================================
# 🧂 ADUBOS CADASTRADOS
# =====================================================
adubos = {
    "Ureia 46%": {
        "dose": 120,
        "unidade": "g/planta",
        "modalidade": "Fertirrigação",
        "meses": ["Jan", "Fev", "Mar", "Abr"]
    },
    "MAP": {
        "dose": 80,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Set", "Out"]
    },
    "KCl": {
        "dose": 100,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Nov", "Dez"]
    },
    "Boro": {
        "dose": 2,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Jan"]
    },
    "Zinco": {
        "dose": 2,
        "unidade": "g/planta",
        "modalidade": "Manual",
        "meses": ["Fev"]
    }
}

st.markdown("### 🧾 Seleção e Ajuste de Adubos")

modalidade_escolhida = st.selectbox(
    "Modalidade principal de aplicação",
    ["Manual", "Fertirrigação"]
)

adubos = {
    "Ureia 46%": {
        "grupo": "Nitrogênio",
        "modalidade": "Fertirrigação",
        "dose": 10.0,
        "unidade": "g/planta",
        "meses": ["Jan", "Fev", "Mar"]
    },
    "Nitrato de Cálcio": {
        "grupo": "Nitrogênio",
        "modalidade": "Fertirrigação",
        "dose": 8.0,
        "unidade": "g/planta",
        "meses": ["Abr", "Mai"]
    },
    "MAP": {
        "grupo": "Fósforo",
        "modalidade": "Manual",
        "dose": 50.0,
        "unidade": "g/planta",
        "meses": ["Nov"]
    },
    "Cloreto de Potássio": {
        "grupo": "Potássio",
        "modalidade": "Manual",
        "dose": 40.0,
        "unidade": "g/planta",
        "meses": ["Dez", "Jan"]
    }
}

adubos_ativos = {}

for nome, info in adubos.items():
    st.markdown("---")
    col1, col2, col3 = st.columns([3, 2, 3])

    ativo_padrao = info["modalidade"] == modalidade_escolhida

    with col1:
        ativo = st.checkbox(
            f"{nome} ({info['modalidade']})",
            value=ativo_padrao,
            key=f"ativo_{nome}"
        )

    with col2:
        dose = st.number_input(
            f"Dose ({info['unidade']})",
            min_value=0.0,
            value=info["dose"],
            step=1.0,
            key=f"dose_{nome}"
        )

    with col3:
        meses = st.multiselect(
            "Meses de aplicação",
            ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
            default=info["meses"],
            key=f"meses_{nome}"
        )

    if ativo:
        adubos_ativos[nome] = {
            "grupo": info["grupo"],
            "modalidade": info["modalidade"],
            "dose": dose,
            "unidade": info["unidade"],
            "meses": meses
        }

st.markdown("### 📅 Distribuição Anual de Adubação (editável)")

meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]

# Tabela base (valores iniciais)
 dados = {
    "Ureia 46% (g/planta)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "MAP (g/planta)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Cloreto de Potássio (g/planta)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Nitrato de Cálcio (g/planta)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Sulfato de Magnésio (g/planta)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Boro (ml/ha)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Zinco (ml/ha)": ["", "", "", "", "", "", "", "", "", "", "", ""],
    "Matéria Orgânica (ml/ha)": ["", "", "", "", "", "", "", "", "", "", "", ""],
 }
df = pd.DataFrame(dados, index=meses)

st.info("✏️ Clique nas células para editar as doses (g ou ml). Deixe vazio quando não houver aplicação.")

df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

# Guardando o resultado para uso futuro
st.session_state["tabela_adubacao"] = df_editado
