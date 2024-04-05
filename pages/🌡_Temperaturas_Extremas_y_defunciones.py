#%%
# Importación de bibliotecas necesarias
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#%%
# Carga de datos
df = pd.read_csv("data/datos_meteo_def.csv")
df_est = pd.read_csv("data/datos_est.csv")

#%%
# Configuración inicial de Streamlit (título de la aplicación)
st.write("# SEREMI RM - Análisis exploratorio de datos - Temperaturas extremas")

#%%
# Selección de estaciones mediante un widget de selección
estaciones = df_est['NOMBRE'].tolist()
indice_quinta_normal = estaciones.index('Quinta Normal') if 'Quinta Normal' in estaciones else 0
nombre_estacion_seleccionada = st.selectbox('Selecciona una estación:', estaciones, index=indice_quinta_normal)
codigo_estacion_seleccionada = df_est[df_est['NOMBRE'] == nombre_estacion_seleccionada]['CODIGO'].iloc[0]
df_seleccionado = df[df['est'] == codigo_estacion_seleccionada]
#%%
# Mapa de estaciones
st.title("Mapa de Estaciones")
df_est['LATITUD'] = df_est['lat']
df_est['LONGITUDE'] = df_est['long']
df_est_mapa = df_est[df_est['CODIGO'] == codigo_estacion_seleccionada]
st.map(df_est_mapa)
#%%
# Preparación de los datos para análisis
df_seleccionado['date'] = pd.to_datetime(df_seleccionado['date'])
df_seleccionado['fecha'] = pd.to_datetime(df_seleccionado['fecha'])
df_seleccionado.dropna(subset=['date'], inplace=True)
años_disponibles = df_seleccionado['date'].dt.year.unique()

# Selección del rango de años para el análisis
if len(años_disponibles) > 0:
    año_inicio, año_fin = st.select_slider(
        'Selecciona el rango de años:',
        options=sorted(años_disponibles),
        value=(min(años_disponibles), max(años_disponibles))
    )
else:
    st.error("No hay datos disponibles para mostrar.")

df_seleccionado_periodo = df_seleccionado[df_seleccionado['date'].dt.year.between(año_inicio, año_fin)]
#%%
# Creación de gráficos con Plotly
#%%
# Gráfico de temperaturas máximas y total de defunciones
st.write("## Gráfico de temperaturas máximas y total de defunciones")
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
fig.update_layout(title_text=f"Temperaturas Máximas y Total de Defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
st.plotly_chart(fig)
#%%
# Gráfico de días con temperaturas sobre y bajo 35°C
color_map_sobre_35 = {
    'Sobre 35': 'red',  # Rojo para días con temperaturas sobre 35°C
    'Bajo 35': 'blue',  # Azul para días con temperaturas bajo 35°C
}

fig_sobre_35 = make_subplots(specs=[[{"secondary_y": True}]])

fig_sobre_35.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)

for alerta, color in color_map_sobre_35.items():
    df_alerta = df_seleccionado_periodo[df_seleccionado_periodo['sobre_35'] == alerta]
    fig_sobre_35.add_trace(
        go.Scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color)),
        secondary_y=False,
    )

fig_sobre_35.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
fig_sobre_35.update_layout(title_text=f"Días con Temperaturas Sobre y Bajo 35°C y total de defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig_sobre_35.update_xaxes(title_text="Fecha")
fig_sobre_35.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig_sobre_35.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
st.plotly_chart(fig_sobre_35)
#%%
# Gráfico de tipo de alerta meteorológica
color_map_alertas = {
    'Sin Alerta': 'blue',  # Azul para días sin alerta
    'Alerta temprana preventiva': 'green',  # Verde para Alerta Temprana Preventiva
    'Alerta Amarilla': 'yellow',  # Amarillo para Alerta Amarilla
    'Alerta Roja': 'red'  # Rojo para Alerta Roja
}

fig_alertas = make_subplots(specs=[[{"secondary_y": True}]])
fig_alertas.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
fig_alertas.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
for alerta, color in color_map_alertas.items():
    df_alerta = df_seleccionado_periodo[df_seleccionado_periodo['alerta'] == alerta]
    fig_alertas.add_trace(
        go.Scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color)),
        secondary_y=False,
    )

fig_alertas.update_layout(title_text=f"Alertas Meteorológicas para {nombre_estacion_seleccionada}")
fig_alertas.update_xaxes(title_text="Fecha")
fig_alertas.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
st.plotly_chart(fig_alertas)
#%%
st.write('## Gráfico de boxplots de temperaturas máximas y total de defunciones por mes de un año en especifico')
# Gráfico de boxplots de temperaturas máximas y total de defunciones por mes de un año en especifico
df_seleccionado['mes'] = df_seleccionado['date'].dt.month_name()
años_disponibles = sorted(df_seleccionado['date'].dt.year.unique())
indice_2024 = años_disponibles.index(2024) if 2024 in años_disponibles else 0
año_seleccionado = st.selectbox('Selecciona un año:', años_disponibles, index=indice_2024)
df_filtrado_por_año = df_seleccionado[df_seleccionado['date'].dt.year == año_seleccionado]
df_filtrado_por_año['mes'] = df_seleccionado['date'].dt.month_name()

fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas por Mes', 'Total de Defunciones por Mes'))
fig.add_trace(
    go.Box(x=df_filtrado_por_año['mes'], y=df_filtrado_por_año['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)
fig.add_trace(
    go.Box(x=df_filtrado_por_año['mes'], y=df_filtrado_por_año['total_defunciones'], name='Total de Defunciones', marker=dict(color='red')),
    row=1, col=2
)
fig.update_layout(height=600, width=800, title_text=f"Boxplots de Temperaturas Máximas y Total de Defunciones por Mes del año {año_seleccionado}")
fig.update_xaxes(title_text="Mes", row=1, col=1)
fig.update_yaxes(title_text="Temperatura Máxima (°C)", row=1, col=1)
fig.update_xaxes(title_text="Mes", row=1, col=2)
fig.update_yaxes(title_text="Total de Defunciones", row=1, col=2)
st.plotly_chart(fig)
