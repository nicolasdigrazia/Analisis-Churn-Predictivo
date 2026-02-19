import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Priorización de Clientes en Riesgo", layout="wide")

st.title("📊 Priorización de Clientes en Riesgo de Churn")
st.write("Sistema de apoyo a decisiones para campañas de retención")

# -----------------------------
# CARGAR DATOS
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("analisis_riesgo_clientes.csv")
    return df

df = load_data()

# -----------------------------
# FILTROS (SIDEBAR)
# -----------------------------
st.sidebar.header("🎯 Filtros")

ciudades = st.sidebar.multiselect(
    "Ciudad",
    options=df["ciudad"].unique(),
    default=["Rosario", "Cordoba", "Buenos aires"]
)

productos = st.sidebar.multiselect(
    "Producto",
    options=df["producto"].unique(),
    default=["Tv", "Internet"]
)

edad_min = st.sidebar.slider("Edad mínima", 18, 90, 42)

# 🔹 NUEVO: filtro por soporte_tickets
soporte_min, soporte_max = st.sidebar.slider(
    "Cantidad de tickets de soporte",
    int(df["soporte_tickets"].min()),
    int(df["soporte_tickets"].max()),
    (0, int(df["soporte_tickets"].max()))
)

riesgos = st.sidebar.multiselect(
    "Nivel de riesgo",
    options=df["riesgo"].unique(),
    default=["Alto", "Medio"]
)

# -----------------------------
# FILTRADO
# -----------------------------
df_filtrado = df[
    (df["churn"] == 0) &
    (df["edad"] >= edad_min) &
    (df["ciudad"].isin(ciudades)) &
    (df["producto"].isin(productos)) &
    (df["soporte_tickets"].between(soporte_min, soporte_max)) &
    (df["riesgo"].isin(riesgos))
].sort_values("prob_churn", ascending=False)

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Clientes Prioritarios", len(df_filtrado))

with col2:
    st.metric("Probabilidad promedio de churn", f"{df_filtrado['prob_churn'].mean():.2%}")

with col3:
    st.metric("Máx. probabilidad", f"{df_filtrado['prob_churn'].max():.2%}")

# -----------------------------
# TABLA PRINCIPAL (NO TOCAR)
# -----------------------------
st.subheader("📋 Lista priorizada de clientes")

st.dataframe(
    df_filtrado[[
        "edad",
        "ciudad",
        "producto",
        "soporte_tickets",
        "meses_activo",
        "prob_churn",
        "riesgo"
    ]],
    width='stretch'
)


# -----------------------------
# DESCARGA CSV
# -----------------------------
st.download_button(
    label="📥 Descargar lista priorizada",
    data=df_filtrado.to_csv(index=False),
    file_name="clientes_prioritarios.csv",
    mime="text/csv"
)
