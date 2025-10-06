import streamlit as st
from streamlit_option_menu import option_menu

# Configuración inicial de la app
st.set_page_config(page_title="App con Mapas", layout="wide")

# Menú lateral
with st.sidebar:
    selected = option_menu("Menú", ["Inicio", "Mapa", "Dashboard"],
        icons=["house", "geo-alt", "bar-chart"], menu_icon="cast", default_index=0)

# Página de contextualización
if selected == "Inicio":
    st.title("📊 Bienvenido a la App Interactiva de Georreferenciación")
    st.markdown("Esta aplicación permite explorar **mapas interactivos** y un **dashboard analítico** sobre los precios del Gas Natural Comprimido Vehicular (GNCV) en Colombia.")

    st.subheader("📌 Contextualización del Conjunto de Datos")
    st.write("""
    El dataset utilizado corresponde a un **registro público** de los precios promedio del Gas Natural Comprimido Vehicular (GNCV) 
    reportados automáticamente en estaciones de servicio en Colombia.  
    Fuente: **Datos Abiertos Colombia**, última actualización: **16 de septiembre de 2025**.
    """)

    # Secciones organizadas en expander
    with st.expander("📂 ¿Qué representa el conjunto de datos?"):
        st.write("""
        - Registra precios promedio del GNCV en distintas localidades (departamentos, municipios, ciudades).  
        - Incluye nombres de estaciones de servicio.  
        - Contiene la fecha de reporte del precio, lo que permite ver la evolución en el tiempo.  
        """)

    with st.expander("🏛️ ¿Quién lo produce y por qué?"):
        st.write("""
        - Publicado por el **Gobierno de Colombia** a través de **Datos Abiertos** bajo el sector de **Minas y Energía**.  
        - Busca brindar transparencia al consumidor, fomentar la competencia y permitir el análisis de precios regionales.  
        - Apoya a entidades regulatorias, investigadores, transportadores y usuarios para tomar decisiones informadas.  
        """)

    with st.expander("⚡ Aspectos relevantes a tener en cuenta"):
        st.write("""
        - **Automatizado**: los reportes son automáticos, lo que reduce error humano pero puede traer retrasos.  
        - **Frecuencia y actualización**: suficiente para construir series de tiempo confiables.  
        - **Variabilidad regional**: los precios cambian según transporte, redes de distribución, impuestos y políticas locales.  
        """)

    with st.expander("🔎 Posibles usos del conjunto de datos"):
        st.write("""
        - Analizar variaciones de precio del GNCV a lo largo del tiempo.  
        - Comparar precios entre regiones.  
        - Relacionar precios con factores logísticos e impuestos.  
        - Ayudar a usuarios de vehículos a decidir dónde y cuándo repostar.  
        - Apoyar políticas públicas sobre combustibles alternativos y transición energética.  
        """)

    with st.expander("📑 Información del dataset"):
        st.write("""
        - Filas: **10,870**  
        - Columnas: **12**  
        - Valores nulos: **0**  
        - Duplicados: **0**  
        """)

elif selected == "Mapa":
    st.switch_page("pages/1_Mapa.py")

elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")