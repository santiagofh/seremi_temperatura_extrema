import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/temperaturas_extremas.py", label="Temperaturas Extremas",  icon="🌡")