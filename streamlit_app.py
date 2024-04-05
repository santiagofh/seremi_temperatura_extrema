import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Temperaturas Extremas RM", page_icon="🌡️")

# Uso de columnas para colocar la imagen al lado izquierdo del texto
col1, col2 = st.columns([1, 3], gap="small")  # Ajusta los valores para cambiar el ancho relativo de las columnas
with col1:
    st.image("646px-SEREMISALUDMET (1).png", use_column_width = True)
    
st.markdown("# Bienvenido al dashboard de temperaturas extremas para la Región Metropolitana! 👋", unsafe_allow_html=True)

st.markdown(
    """
    Bienvenidos a la aplicación dedicada a la visualización de olas de calor y temperaturas extremas en la Región Metropolitana (RM). 
    A través de esta plataforma, usuarios pueden acceder a datos relevantes y análisis actualizados sobre eventos de temperatura extrema, facilitando la comprensión y la gestión de sus impactos.
    
    ### Desarrollo y Pilotaje
    Este proyecto ha sido cuidadosamente desarrollado por la Unidad de Gestión de la Información Estadística, comprometidos con la entrega de herramientas para el análisis y la toma de decisiones basadas en datos precisos y oportunos.
    """
)
st.markdown(
    """
    ### Indice    """
)
st.page_link("streamlit_app.py", label="Home", icon="🏠")
st.page_link("pages/🌡_Temperaturas_Extremas.py", label="Temperaturas Extremas",  icon="🌡")
st.page_link("pages/🌡_Temperaturas_Extremas_y_defunciones.py", label="Temperaturas Extremas y Defunciones",  icon="🌡")
# %%
