#%%
import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.write("# Bienvenido a los dashboard de temperaturas extremas para la Región Metropolitana! 👋")

st.sidebar.success("Selecciona una categoria.")

st.markdown(
    """
    Esta es una aplicacion para la visualizacion de las olas de calor y temperaturas extremas de la RM.
    ### Desarrollo y pilotaje
    Está desarrollado por la Unidad de Gestion de la información Estadistica.
    
"""
)
st.page_link("Hello.py", label="Home", icon="🏠")
st.page_link("pages/🌡_Temperaturas_Extremas.py", label="Temperaturas Extremas",  icon="🌡")
st.page_link("pages/🌡_Temperaturas_Extremas_y_defunciones.py", label="Temperaturas Extremas",  icon="🌡")
# %%
