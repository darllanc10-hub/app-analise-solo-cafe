
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

st.title("☕ Interpretação de Análise de Solo – Café")

st.markdown("### 📌 Dados do Produtor")

nome = st.text_input("Nome do produtor")
talhao = st.text_input("Talhão")

st.markdown("### 🌱 Espaçamento e Produção")

col1, col2 = st.columns(2)
with col1:
    espac_linha = st.number_input("Espaçamento entre linhas (m)", value=3.0)
with col2:
    espac_planta = st.number_input("Espaçamento entre plantas (m)", value=1.0)

produtividade = st.number_input("Produtividade (sc/ha)", value=60)

plantas_ha = 10000 / (espac_linha * espac_planta)

st.markdown("---")

st.markdown("### 🧪 Saturação de Bases")

V_atual = st.number_input("V atual (%)", value=45)
V_desejado = 70
PRNT = 90

if V_atual < V_desejado:
    dose_calcario = ((V_desejado - V_atual) / V_desejado) * 2
    dose_calcario = min(dose_calcario, 3)
else:
    dose_calcario = 0

calcario_planta = (dose_calcario * 1_000_000) / plantas_ha
dose_gesso = dose_calcario * 0.30
gesso_planta = (dose_gesso * 1_000_000) / plantas_ha

st.markdown("### 🟤 Calagem e Gessagem")

st.success(f"Calcário: {calcario_planta:.0f} g por planta")
st.warning(f"Gesso agrícola: {gesso_planta:.0f} g por planta")

st.markdown("---")

st.markdown("### 📅 Tabela de Distribuição Anual (g por planta)")

meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
tabela = pd.DataFrame(index=meses)

dose_20_10_05 = 100
dose_19_04_19 = 100
dose_fertium = 150

mes_florada = ["Jun","Jul","Ago"]
mes_granacao = ["Out","Nov","Dez","Jan","Fev","Mar","Abr"]

tabela["20-10-05"] = [
    dose_20_10_05 if m in mes_florada and meses.index(m) % 2 == 0 else ""
    for m in meses
]

tabela["19-04-19"] = [
    dose_19_04_19 if m in mes_granacao and meses.index(m) % 2 == 0 else ""
    for m in meses
]

tabela["Fertium Produção"] = [
    dose_fertium if m in mes_granacao and meses.index(m) % 2 == 0 else ""
    for m in meses
]

st.dataframe(tabela, use_container_width=True)

st.markdown("---")
st.caption("Resultado expresso em g por planta. Aplicações com residual de 2 meses.")
