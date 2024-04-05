#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# pydeck eliminado porque no se usa en el ejemplo proporcionado

# Carga de datos
df = pd.read_csv("data/datos_meteo_def.csv")
df_est = pd.read_csv("data/datos_est.csv")

# Título
st.write("# SEREMI RM - Análisis exploratorio de datos - Temperaturas extremas")

## Selección de estaciones
estaciones = df_est['NOMBRE'].tolist()
indice_quinta_normal = estaciones.index('Quinta Normal') if 'Quinta Normal' in estaciones else 0
nombre_estacion_seleccionada = st.selectbox('Selecciona una estación:', estaciones, index=indice_quinta_normal)

# Asegurarse de que se usa el nombre de la columna correcto para el código de estación
codigo_estacion_seleccionada = df_est[df_est['NOMBRE'] == nombre_estacion_seleccionada]['CODIGO'].iloc[0]

# Ajuste para seleccionar los datos correctos para la estación
df_seleccionado = df[df['est'] == codigo_estacion_seleccionada]

# Mostrar el título del mapa
st.title("Mapa de Estaciones")
df_est['LATITUD'] = df_est['lat']
df_est['LONGITUDE'] = df_est['long']
df_est_mapa = df_est[df_est['CODIGO'] == codigo_estacion_seleccionada]
st.map(df_est_mapa)

# %%
df_seleccionado['fecha'] = pd.to_datetime(df_seleccionado['fecha'], errors='coerce')
df_seleccionado.dropna(subset=['fecha'], inplace=True)
años_disponibles = df_seleccionado['fecha'].dt.year.unique()

# Si es posible que aún no haya años disponibles, se puede manejar este caso también
if len(años_disponibles) > 0:
    año_inicio, año_fin = st.select_slider(
        'Selecciona el rango de años:',
        options=sorted(años_disponibles),
        value=(min(años_disponibles), max(años_disponibles))
    )
else:
    st.error("No hay datos disponibles para mostrar.")
    
# Filtrar el DataFrame por el rango de años seleccionado
df_seleccionado = df_seleccionado[df_seleccionado['fecha'].dt.year.between(año_inicio, año_fin)]

# Crear un gráfico combinado
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Agregar las temperaturas máximas al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado['fecha'], y=df_seleccionado['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)

# Agregar el total de defunciones al gráfico
# Asegúrate de que 'total_defunciones' es el nombre correcto de tu columna. Si no, ajusta según tu DataFrame.
fig.add_trace(
    go.Scatter(x=df_seleccionado['fecha'], y=df_seleccionado['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='red')),
    secondary_y=True,
)

# Añadir títulos al gráfico y a los ejes
fig.update_layout(title_text=f"Temperaturas Máximas y Total de Defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
