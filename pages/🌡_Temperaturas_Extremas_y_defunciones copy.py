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
df_seleccionado['date'] = pd.to_datetime(df_seleccionado['date'])
df_seleccionado['fecha'] = pd.to_datetime(df_seleccionado['fecha'])
df_seleccionado.dropna(subset=['date'], inplace=True)
años_disponibles = df_seleccionado['date'].dt.year.unique()
#%%
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
df_seleccionado_periodo = df_seleccionado[df_seleccionado['date'].dt.year.between(año_inicio, año_fin)]

# Crear un gráfico combinado
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Agregar las temperaturas máximas al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)

# Agregar el total de defunciones al gráfico
# Asegúrate de que 'total_defunciones' es el nombre correcto de tu columna. Si no, ajusta según tu DataFrame.
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='red')),
    secondary_y=True,
)

# Añadir títulos al gráfico y a los ejes
fig.update_layout(title_text=f"Temperaturas Máximas y Total de Defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# %%
# Crear un gráfico combinado con dos subplots lado a lado
fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas por Mes', 'Total de Defunciones por Mes'))
# Agregar el boxplot de temperaturas máximas
fig.add_trace(
    go.Box(x=df_seleccionado_periodo['mes'], y=df_seleccionado_periodo['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Agregar las temperaturas máximas al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
# Agregar el total de defunciones al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='red')),
    secondary_y=True,
)
color_map = {
    'Sin Alerta': 'blue',  # Azul para días sin alerta
    'Alerta temprana preventiva': 'green',  # Verde para Alerta Temprana Preventiva
    'Alerta Amarilla': 'yellow',  # Amarillo para Alerta Amarilla
    'Alerta Roja': 'red'  # Rojo para Alerta Roja
}
# Agregar marcadores de colores para cada tipo de alerta en el gráfico
for alerta, color in color_map.items():
    df_alerta = df_seleccionado_periodo[df_seleccionado_periodo['alerta'] == alerta]
    fig.add_trace(
        go.Scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color)),
        secondary_y=False,  # Asumiendo que quieres que las alertas se muestren en relación con las temperaturas máximas
    )
# Añadir títulos al gráfico y a los ejes (ajusta según sea necesario)
fig.update_layout(title_text=f"Temperaturas Máximas, Total de Defunciones y Alertas para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C) / Alertas", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
#%%
# Crear un gráfico combinado con dos subplots lado a lado
fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas por Mes', 'Total de Defunciones por Mes'))
# Agregar el boxplot de temperaturas máximas
fig.add_trace(
    go.Box(x=df_seleccionado_periodo['mes'], y=df_seleccionado_periodo['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Agregar las temperaturas máximas al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
# Agregar el total de defunciones al gráfico
fig.add_trace(
    go.Scatter(x=df_seleccionado_periodo['date'], y=df_seleccionado_periodo['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='red')),
    secondary_y=True,
)
color_map = {
        'Sobre 35': 'red',  # Azul para días sin alerta
        'Bajo 35': 'blue',  # Azul para días sin alerta
    }
# Agregar marcadores de colores para cada tipo de alerta en el gráfico
for alerta, color in color_map.items():
        df_alerta = df_seleccionado_periodo[df_seleccionado_periodo['sobre_35'] == alerta]
        fig.add_scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color),)

# Añadir títulos al gráfico y a los ejes (ajusta según sea necesario)
fig.update_layout(title_text=f"Temperaturas Máximas, Total de Defunciones y Alertas para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C) / Alertas", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
# %%
# Asegurarse de que 'date' y 't_max' están en el formato correcto
df_seleccionado['date'] = pd.to_datetime(df_seleccionado['date'])
df_seleccionado['mes'] = df_seleccionado['date'].dt.month_name()

años_disponibles = sorted(df_seleccionado['date'].dt.year.unique())
indice_2024 = años_disponibles.index(2024) if 2024 in años_disponibles else 0
año_seleccionado = st.selectbox('Selecciona un año:', años_disponibles,index=indice_2024)
df_filtrado_por_año = df_seleccionado[df_seleccionado['date'].dt.year == año_seleccionado]
df_filtrado_por_año['mes'] = df_seleccionado['date'].dt.month_name()


# Crear un gráfico combinado con dos subplots lado a lado
fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas por Mes', 'Total de Defunciones por Mes'))

# Agregar el boxplot de temperaturas máximas
fig.add_trace(
    go.Box(x=df_filtrado_por_año['mes'], y=df_filtrado_por_año['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)

# Agregar el boxplot del total de defunciones
# Asegúrate de que 'total_defunciones' es el nombre correcto de tu columna. Si no, ajusta según tu DataFrame.
fig.add_trace(
    go.Box(x=df_filtrado_por_año['mes'], y=df_filtrado_por_año['total_defunciones'], name='Total de Defunciones', marker=dict(color='red')),
    row=1, col=2
)

# Ajustar el layout para mejorar la visualización
fig.update_layout(height=600, width=800, title_text="Boxplots de Temperaturas Máximas y Total de Defunciones por Mes")
fig.update_xaxes(title_text="Mes", row=1, col=1)
fig.update_yaxes(title_text="Temperatura Máxima (°C)", row=1, col=1)
fig.update_xaxes(title_text="Mes", row=1, col=2)
fig.update_yaxes(title_text="Total de Defunciones", row=1, col=2)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# %%
