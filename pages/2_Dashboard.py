import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------
st.set_page_config(page_title="Dashboard GNCV", layout="wide")

# -------------------------------------------------------
# CARGA DE DATOS
# -------------------------------------------------------
@st.cache_data
def load_data():
    # ⚠️ Ajusta esta ruta al archivo real
    df = pd.read_csv("precios.csv")
    
    # Conversión de tipos
    df["FECHA_PRECIO"] = pd.to_datetime(df["FECHA_PRECIO"], errors="coerce")
    df["PRECIO_PROMEDIO_PUBLICADO"] = pd.to_numeric(df["PRECIO_PROMEDIO_PUBLICADO"], errors="coerce")
    
    # Eliminar filas sin coordenadas o sin precio
    df = df.dropna(subset=["LATITUD_MUNICIPIO", "LONGITUD_MUNICIPIO", "PRECIO_PROMEDIO_PUBLICADO"])
    return df

df = load_data()

# -------------------------------------------------------
# TÍTULO Y DESCRIPCIÓN
# -------------------------------------------------------
st.title("📊 Dashboard Interactivo del GNCV en Colombia")
st.markdown("""
Analiza y visualiza los precios del **Gas Natural Comprimido Vehicular (GNCV)** por región, fecha y estación.
Utiliza los filtros para explorar variaciones regionales, tendencias temporales y ubicaciones geográficas.
""")

# -------------------------------------------------------
# FILTROS LATERALES
# -------------------------------------------------------
st.sidebar.header("🔎 Filtros del Dashboard")

# Año y mes
anios = sorted(df["ANIO_PRECIO"].unique())
anio_sel = st.sidebar.multiselect("Selecciona Año", anios, default=anios)

meses = sorted(df["MES_PRECIO"].unique())
mes_sel = st.sidebar.multiselect("Selecciona Mes", meses, default=meses)

# Departamento
deptos = sorted(df["DEPARTAMENTO_EDS"].unique())
# Verificar si CUNDINAMARCA está realmente en la lista
default_depto = ["CUNDINAMARCA"] if "CUNDINAMARCA" in deptos else [deptos[0]]

depto_sel = st.sidebar.multiselect(
    "Selecciona Departamento",
    deptos,
    default=default_depto
)

# Aplicar filtros
df_filtrado = df[
    (df["ANIO_PRECIO"].isin(anio_sel)) &
    (df["MES_PRECIO"].isin(mes_sel)) &
    (df["DEPARTAMENTO_EDS"].isin(depto_sel))
]

# -------------------------------------------------------
# INDICADORES CLAVE (KPI)
# -------------------------------------------------------
st.subheader("📌 Indicadores Clave")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Precio promedio", f"${df_filtrado['PRECIO_PROMEDIO_PUBLICADO'].mean():,.0f}")

with col2:
    st.metric("📉 Precio mínimo", f"${df_filtrado['PRECIO_PROMEDIO_PUBLICADO'].min():,.0f}")

with col3:
    st.metric("📈 Precio máximo", f"${df_filtrado['PRECIO_PROMEDIO_PUBLICADO'].max():,.0f}")

st.divider()

# -------------------------------------------------------
# VISUALIZACIONES (TABS)
# -------------------------------------------------------
# -------------------------------------------------------
# VISUALIZACIONES (TABS)
# -------------------------------------------------------
tab1, tab2 = st.tabs(["📈 Tendencia Temporal", "📊 Comparación Regional"])

# --- TAB 1: Evolución temporal ---
with tab1:
    st.markdown("### Evolución del Precio en el Tiempo")
    df_time = (
        df_filtrado.groupby("FECHA_PRECIO")["PRECIO_PROMEDIO_PUBLICADO"]
        .mean().reset_index()
    )

    fig_linea = px.line(
        df_time,
        x="FECHA_PRECIO",
        y="PRECIO_PROMEDIO_PUBLICADO",
        title="Tendencia del Precio Promedio Diario del GNCV",
        markers=True
    )
    fig_linea.update_layout(xaxis_title="Fecha", yaxis_title="Precio ($)")
    st.plotly_chart(fig_linea, use_container_width=True)

# --- TAB 2: Comparación por Departamento ---
with tab2:
    st.markdown("### Promedio de Precios por Departamento")
    df_region = (
        df_filtrado.groupby("DEPARTAMENTO_EDS")["PRECIO_PROMEDIO_PUBLICADO"]
        .mean().reset_index().sort_values(by="PRECIO_PROMEDIO_PUBLICADO", ascending=False)
    )

    fig_bar = px.bar(
        df_region,
        x="DEPARTAMENTO_EDS",
        y="PRECIO_PROMEDIO_PUBLICADO",
        color="PRECIO_PROMEDIO_PUBLICADO",
        title="Promedio de Precios por Departamento",
    )
    fig_bar.update_layout(xaxis_title="Departamento", yaxis_title="Precio Promedio ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

