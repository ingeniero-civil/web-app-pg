import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Selección de PG en Perú",
    page_icon="🛣️",
    layout="wide"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #6366f1;
        color: white;
        width: 100%;
        padding: 15px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4f46e5;
    }
    h1 {
        color: white;
        padding: 20px;
        background-color: #F0F2F6;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-box {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("# 🛣️ Sistema de Selección de PG en Perú")
st.markdown("### Evaluación de Pavimentos Asfálticos - Perú")

# Inicializar session state
if 'coordenadas' not in st.session_state:
    st.session_state.coordenadas = [-12.04374415711892, -77.04273545646473]
if 'ubicacion' not in st.session_state:
    st.session_state.ubicacion = "Buscando ubicación..."

# Layout en columnas
col1, col2 = st.columns([1, 2])

with col1:
    # Modo de interpolación
    st.markdown("### Modo de interpolación")
    modo_interpolacion = st.selectbox(
        "",
        ["Estación más cercana (rápido)", "Interpolación lineal", "Interpolación IDW"],
        label_visibility="collapsed"
    )
    
    # Mapa
    st.markdown("### 📍 Ubicación")
    m = folium.Map(
        location=st.session_state.coordenadas,
        zoom_start=15,
        tiles="OpenStreetMap"
    )
    
    # Agregar marcador
    folium.Marker(
        st.session_state.coordenadas,
        popup="Punto Personalizado",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    folium_static(m, width=400, height=300)
    
    # Información del punto
    st.markdown("### 📌 Punto personalizado")
    st.markdown(f"**Coordenadas:** {st.session_state.coordenadas[0]:.4f}°N, {st.session_state.coordenadas[1]:.4f}°W")
    st.markdown(f"**Modo:** 1_Estacion")
    st.info(st.session_state.ubicacion)

with col2:
    # Pestañas
    tabs = st.tabs(["🛣️ Pavimento", "🌡️ Clima", "📊 Gráficas", "⚙️ SHRP/LTPP", "📈 RDM"])
    
    with tabs[0]:  # Pestaña Pavimento
        st.markdown("## 🛣️ Parámetros del Pavimento")
        
        # Profundidad de rodera
        st.markdown("### 🔧 Profundidad de rodera")
        prof_rodera = st.number_input(
            "",
            min_value=0,
            max_value=100,
            value=12,
            key="prof_rodera",
            label_visibility="collapsed"
        )
        st.markdown(f"**{prof_rodera} mm**")
        
        # ESAL
        st.markdown("### 🚛 ESAL")
        esal = st.number_input(
            "",
            min_value=0,
            max_value=1000,
            value=35,
            key="esal",
            label_visibility="collapsed"
        )
        st.markdown(f"**{esal} mill.**")
        
        # Velocidad de tráfico
        st.markdown("### 🚗 Velocidad de tráfico")
        velocidad = st.number_input(
            "",
            min_value=0,
            max_value=200,
            value=40,
            key="velocidad",
            label_visibility="collapsed"
        )
        st.markdown(f"**{velocidad} km/h**")
        
        # Profundidad de capa
        st.markdown("### 📏 Profundidad de capa")
        prof_capa = st.number_input(
            "",
            min_value=0,
            max_value=500,
            value=70,
            key="prof_capa",
            label_visibility="collapsed"
        )
        st.markdown(f"**{prof_capa} mm**")
        
        # Confiabilidad
        st.markdown("### ✅ Confiabilidad")
        confiabilidad = st.slider(
            "",
            min_value=0,
            max_value=100,
            value=98,
            key="confiabilidad",
            label_visibility="collapsed"
        )
        st.markdown(f"**{confiabilidad} %**")
        
        # Botón de calcular
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Guardar y Calcular", type="primary"):
            st.success("✅ Parámetros guardados correctamente")
            st.balloons()
            
            # Aquí iría la lógica de cálculo
            st.markdown("### Resultados del Cálculo")
            st.info(f"""
            **Performance Grade Recomendado:** PG 64-22
            
            **Parámetros utilizados:**
            - Profundidad de rodera: {prof_rodera} mm
            - ESAL: {esal} millones
            - Velocidad: {velocidad} km/h
            - Profundidad de capa: {prof_capa} mm
            - Confiabilidad: {confiabilidad}%
            """)
    
    with tabs[1]:  # Pestaña Clima
        st.markdown("## 🌡️ Datos Climáticos")
        
        col_clima1, col_clima2 = st.columns(2)
        
        with col_clima1:
            st.metric("Temperatura Máxima", "35°C", "↑ 2°C")
            st.metric("Temperatura Mínima", "22°C", "↓ 1°C")
            st.metric("Humedad Relativa", "75%")
        
        with col_clima2:
            st.metric("Precipitación Anual", "2,500 mm")
            st.metric("Velocidad del Viento", "15 km/h")
            st.metric("Radiación Solar", "850 W/m²")
    
    with tabs[2]:  # Pestaña Gráficas
        st.markdown("## 📊 Gráficas")
        st.info("Esta sección mostrará gráficas de temperaturas, distribución de cargas y análisis de desempeño.")
        
    with tabs[3]:  # Pestaña SHRP/LTPP
        st.markdown("## ⚙️ SHRP/LTPP")
        st.info("Esta sección mostrará datos del programa Strategic Highway Research Program y Long-Term Pavement Performance.")
        
    with tabs[4]:  # Pestaña RDM
        st.markdown("## 📈 RDM")
        st.info("Esta sección mostrará el análisis de Diseño de Mezcla Resiliente.")

# Barra lateral con recomendaciones
with st.sidebar:
    st.markdown("## 💡 Recomendaciones")
    st.info("""
    ### Guía de uso:
    1. Seleccione el modo de interpolación
    2. Ingrese los parámetros del pavimento
    3. Verifique la ubicación en el mapa
    4. Presione 'Guardar y Calcular'
    5. Revise los resultados y gráficas
    """)
    
    st.markdown("## ℹ️ Acerca de")
    st.markdown("""
    Sistema de evaluación y selección de Performance Grade 
    para pavimentos asfálticos en Perú.
    
    **Versión:** 1.0
    
    **Desarrollado para:** Evaluación de Pavimentos
    """)

# Footer
st.markdown("---")
st.markdown("© 2024 Sistema de Selección de PG en Perú | Evaluación de Pavimentos Asfálticos")
