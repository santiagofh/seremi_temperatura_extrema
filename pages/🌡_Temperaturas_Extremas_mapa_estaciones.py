#%%
# Importación de bibliotecas necesarias
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import griddata
from datetime import datetime
import numpy as np
#%%
# Carga de datos
df = pd.read_csv("data/datos_meteo.csv")
df_est = pd.read_csv("data/datos_est.csv")
df_def = pd.read_csv("data/datos_def.csv")
df_def['fecha'] = pd.to_datetime(df_def['fecha'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df_meteo_est=df_est[['CODIGO','NOMBRE','ALTITUD','Propietario','lat','long']].merge(df,left_on='CODIGO',right_on='est',how='left')
#%%
# Configuración inicial de Streamlit (título de la aplicación)
st.write("# SEREMI RM - Análisis exploratorio de datos - Temperaturas extremas")

#%%
# Mapa de estaciones
st.title("Mapa de Estaciones")
df_est['LATITUD'] = df_est['lat']
df_est['LONGITUDE'] = df_est['long']
st.map(df_est)
#%%

# Selector de fecha
st.title("Seleccione una Fecha")
fecha_seleccionada = st.date_input("Fecha", value=df['date'].max(), min_value=df['date'].min(), max_value=df['date'].max())
df_fecha = df_meteo_est[df_meteo_est['date'] == pd.to_datetime(fecha_seleccionada)]
#%%
# Asumiendo que df_fecha ya está filtrado por fecha y contiene las columnas necesarias
points = df_fecha[['lat', 'long']].values
values = df_fecha['t_max'].values
grid_x, grid_y = np.mgrid[min(df_fecha['lat']):max(df_fecha['lat']):100j, min(df_fecha['long']):max(df_fecha['long']):100j]
grid_z = griddata(points, values, (grid_x, grid_y), method='linear')

# %%
latitude = grid_x.ravel()
longitude = grid_y.ravel()
temperatures = grid_z.ravel()
df_grid = pd.DataFrame({
    'LATITUDE': latitude,
    'LONGITUDE': longitude,
    'T_MAX': temperatures
})
df_grid.dropna(inplace=True)
st.map(df_grid)
# %%
def categorize_temperature(t_max):
    if t_max < 30:
        return "green"
    elif 30 <= t_max <= 35:
        return "yellow"
    else:
        return "red"

df_grid['color'] = df_grid['T_MAX'].apply(categorize_temperature)

# Asegúrate de que los valores estén en el rango deseado y normalízalos para la visualización
import plotly.express as px

fig = px.scatter_mapbox(df_grid,
                        lat="LATITUDE",
                        lon="LONGITUDE",
                        color="color",
                        color_discrete_map={"green": "green", "yellow": "yellow", "red": "red"},
                        size_max=15,
                        zoom=10)

fig.update_layout(mapbox_style="open-street-map",
                  mapbox_center_lon=df_grid['LONGITUDE'].mean(),
                  mapbox_center_lat=df_grid['LATITUDE'].mean())

st.plotly_chart(fig, use_container_width=True)
