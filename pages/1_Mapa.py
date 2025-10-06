import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =====================================
# 1. Configuración de la página
# =====================================
st.set_page_config(page_title="Mapa de estaciones", layout="wide")

# =====================================
# 2. Cargar datos
# =====================================
@st.cache_data
def cargar_datos():
    # Cargar datos
    df = pd.read_csv("precios.csv")

    # Asegurar tipo de dato correcto
    df["FECHA_PRECIO"] = pd.to_datetime(df["FECHA_PRECIO"], errors="coerce")

    # 🔧 Convertir precio a numérico
    df["PRECIO_PROMEDIO_PUBLICADO"] = pd.to_numeric(df["PRECIO_PROMEDIO_PUBLICADO"], errors="coerce")

    # Ordenar y quedarse con el último registro por municipio
    df = df.sort_values("FECHA_PRECIO").drop_duplicates(subset=["CODIGO_MUNICIPIO_DANE"], keep="last")

    # Filtrar coordenadas válidas dentro de Colombia
    df = df.dropna(subset=["LATITUD_MUNICIPIO", "LONGITUD_MUNICIPIO"])
    df = df[
        (df["LATITUD_MUNICIPIO"].between(-5, 15)) &
        (df["LONGITUD_MUNICIPIO"].between(-85, -65))
    ]

    return df

# =====================================
# 3. Crear mapa
# =====================================
def crear_mapa(df, departamento):
    # Si se selecciona un departamento específico
    if departamento != "TODOS":
        df = df[df["DEPARTAMENTO_EDS"] == departamento]

    # Crear mapa centrado en Colombia
    mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

    # Agregar marcadores al mapa
    for _, fila in df.iterrows():
        folium.CircleMarker(
            location=[fila["LATITUD_MUNICIPIO"], fila["LONGITUD_MUNICIPIO"]],
            radius=6,
            popup=(
                f"<b>Municipio:</b> {fila['MUNICIPIO_EDS']}<br>"
                f"<b>Departamento:</b> {fila['DEPARTAMENTO_EDS']}<br>"
                f"<b>Tipo Combustible:</b> {fila['TIPO_COMBUSTIBLE']}<br>"
                f"<b>Precio Promedio:</b> ${fila['PRECIO_PROMEDIO_PUBLICADO']:,.0f}"
            ),
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
        ).add_to(mapa)

    return mapa

# =====================================
# 4. Interfaz principal
# =====================================
st.title("⛽ Estaciones en Colombia")

df = cargar_datos()

# Selector de departamento con opción "TODOS"
departamentos = ["TODOS"] + sorted(df["DEPARTAMENTO_EDS"].dropna().unique().tolist())
departamento_sel = st.selectbox("Selecciona un departamento:", departamentos)

# Crear mapa
mapa = crear_mapa(df, departamento_sel)
st_folium(mapa, width=1200, height=600)


# --- Nota final ---
st.markdown("""
---
📝 **Nota:**  
- Si hay múltiples registros por municipio, se muestra **solo el más reciente** según la fecha.  
- El tamaño y color del punto representan el **precio promedio publicado (COP)**.  
- La opción “Todos” permite visualizar el panorama nacional de precios del GNCV.
""")