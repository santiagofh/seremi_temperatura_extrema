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
st.markdown("""
            ## Metodología

            ### Extracción de datos
                        
            **Identificación y Selección de Fuentes de Datos**: Se identificaron las estaciones meteorológicas de interés (RM y alrededores) y la página web de la Dirección Meteorológica de Chile como fuentes de datos para la extracción de temperaturas maximas, minimas y medias diarias.

            **Extracción de Datos**: Se realizaron solicitudes automatizadas a la página web para obtener los datos de temperatura de varias estaciones meteorológicas, cubriendo un rango temporal desde enero de 2013 hasta la fecha actual.

            **Limpieza y Preprocesamiento de Datos**: Tras la extracción, se llevó a cabo un proceso de limpieza que incluyó la transformación de los datos a un formato csv más manejable, la eliminación de datos no relevantes, y la conversión de tipos de datos para su correcta manipulación.

            **Estructuración de Datos**: Se reorganizaron los datos para facilitar su análisis, lo que incluyó renombrar columnas para mejorar la claridad, y extraer información clave como la estación meteorológica, el año, y el mes de cada registro.

            ### Evaluación de alerta
            **Análisis de Datos y Evaluación de Alertas**: 
            - Se definen funciones para evaluar y clasificar días según criterios específicos de temperatura, como la asignación de alertas (sin alerta, alerta temprana preventiva, alerta amarilla, alerta roja) basadas en la temperatura máxima y la temporalidad.
            - Se calcula si las temperaturas superan los 35°C, marcando esos días específicamente para una revisión más detallada o acciones preventivas.

            
                    
                        
""")
st.markdown(
    """
    ### Indice    """
)
st.page_link("streamlit_app.py", label="Home", icon="🏠")
st.page_link("pages/🌡_Temperaturas_Extremas.py", label="Temperaturas Extremas",  icon="🌡")
st.page_link("pages/🌡_Temperaturas_Extremas_y_defunciones.py", label="Temperaturas Extremas y Defunciones",  icon="🌡")
# %%
