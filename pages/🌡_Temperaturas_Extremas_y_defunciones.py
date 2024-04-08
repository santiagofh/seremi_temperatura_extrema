#%%
# Importación de bibliotecas necesarias
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

#%%
# Carga de datos
df = pd.read_csv("data/datos_meteo.csv")
df_est = pd.read_csv("data/datos_est.csv")
df_def = pd.read_csv("data/datos_def.csv")
df_def['fecha'] = pd.to_datetime(df_def['fecha'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
#%%
# Configuración inicial de Streamlit (título de la aplicación)
st.write("# SEREMI RM - Análisis exploratorio de datos - Temperaturas extremas")

#%%
# Selección de estaciones mediante un widget de selección
estaciones = df_est['NOMBRE'].tolist()
indice_quinta_normal = estaciones.index('Quinta Normal') if 'Quinta Normal' in estaciones else 0
nombre_estacion_seleccionada = st.selectbox('Selecciona una estación:', estaciones, index=indice_quinta_normal)
codigo_estacion_seleccionada = df_est[df_est['NOMBRE'] == nombre_estacion_seleccionada]['CODIGO'].iloc[0]
df_selec = df[df['est'] == codigo_estacion_seleccionada]
df_selec_est_def=df_selec.merge(df_def, how='left', left_on='date', right_on='fecha')

#%%
# Mapa de estaciones
st.title("Mapa de Estaciones")
df_est['LATITUD'] = df_est['lat']
df_est['LONGITUDE'] = df_est['long']
df_est_mapa = df_est[df_est['CODIGO'] == codigo_estacion_seleccionada]
st.map(df_est_mapa)
#%%
# Preparación de los datos para análisis
df_selec_est_def['date'] = pd.to_datetime(df_selec_est_def['date'])
df_selec_est_def['fecha'] = pd.to_datetime(df_selec_est_def['fecha'])
df_selec_est_def.dropna(subset=['date'], inplace=True)
años_disponibles = df_selec_est_def['date'].dt.year.unique()

# Selección del rango de años para el análisis
if len(años_disponibles) > 0:
    año_inicio, año_fin = st.select_slider(
        'Selecciona el rango de años:',
        options=sorted(años_disponibles),
        value=(min(años_disponibles), max(años_disponibles))
    )
else:
    st.error("No hay datos disponibles para mostrar.")

df_selec_est_def_period = df_selec_est_def[df_selec_est_def['date'].dt.year.between(año_inicio, año_fin)]
#%%
# Creación de gráficos con Plotly
#%%
# Gráfico de temperaturas máximas y total de defunciones



st.write("## Gráfico de temperaturas máximas y total de defunciones con distintos criterios")

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
fig.update_layout(title_text=f"Temperaturas Máximas y Total de Defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig.update_xaxes(title_text="Fecha")
fig.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
st.plotly_chart(fig)
#%%


st.markdown('''
            ### **Evaluacion de alerta temperaturas sobre 35º**
            - Se establece un indicador si la temperatura supera los 35 grados en un dia especifico
''')


# Gráfico de días con temperaturas sobre y bajo 35°C
color_map_sobre_35_alerta = {
    'Sobre 35': 'red',  # Rojo para días con temperaturas sobre 35°C
    'Bajo 35': 'blue',  # Azul para días con temperaturas bajo 35°C
}

fig_sobre_35_alerta = make_subplots(specs=[[{"secondary_y": True}]])

fig_sobre_35_alerta.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)

for alerta, color in color_map_sobre_35_alerta.items():
    df_alerta = df_selec_est_def_period[df_selec_est_def_period['sobre_35_alerta'] == alerta]
    fig_sobre_35_alerta.add_trace(
        go.Scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color)),
        secondary_y=False,
    )

fig_sobre_35_alerta.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
fig_sobre_35_alerta.update_layout(title_text=f"Días con Temperaturas Sobre y Bajo 35°C y total de defunciones para {nombre_estacion_seleccionada} desde {año_inicio} hasta {año_fin}")
fig_sobre_35_alerta.update_xaxes(title_text="Fecha")
fig_sobre_35_alerta.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
fig_sobre_35_alerta.update_yaxes(title_text="Total de Defunciones", secondary_y=True)
st.plotly_chart(fig_sobre_35_alerta)
#%%



st.markdown('''
            ### **Evaluacion de alerta SENAPRED, ORD 4877 emitido el dia 01-12-2023**

            - Fuente: https://previsionsocial.gob.cl/wp-content/uploads/2023/12/ORD-4877-01-12-2023.pdf
            - Siguiendo la ORD 4877 emitida el 1 de diciembre de 2023, se establecen los siguientes criterios para la activación de alertas:
                - **Alerta Temprana Preventiva (ATP)**: 
                        -   Se declara al momento de la activación del Anexo por Amenaza Calor Extremo.
                        -   Vigente durante todo el periodo de acrivacion desde el mes de noviembre al mes de marzo de cada año, para todo el territorio nacional.
                - **Alerta Amarilla (AA)**:
                    - Pronóstico meteorológico de la Dirección Meteorológica de Chile (DMC) con temperaturas máximas diarias de 34°C o más por al menos 2 días.
                - **Alerta Roja (AR)**:
                    - Pronóstico meteorológico de la DMC con temperaturas máximas diarias de 40°C o más por un día o más.
                    - Pronóstico meteorológico de la DMC con temperaturas máximas diarias de 34°C o más por al menos 3 días.
''')
# Gráfico de tipo de alerta meteorológica
color_map_alertas = {
    'Sin Alerta': 'blue',  # Azul para días sin alerta
    'Alerta Temprana Preventiva': 'green',  # Verde para Alerta Temprana Preventiva
    'Alerta Amarilla': 'yellow',  # Amarillo para Alerta Amarilla
    'Alerta Roja': 'red'  # Rojo para Alerta Roja
}

fig_alertas = make_subplots(specs=[[{"secondary_y": True}]])
fig_alertas.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
fig_alertas.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
for alerta, color in color_map_alertas.items():
    df_alerta = df_selec_est_def_period[df_selec_est_def_period['senapred_alerta'] == alerta]
    fig_alertas.add_trace(
        go.Scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color)),
        secondary_y=False,
    )

fig_alertas.update_layout(title_text=f"Alertas Meteorológicas para {nombre_estacion_seleccionada}")
fig_alertas.update_xaxes(title_text="Fecha")
fig_alertas.update_yaxes(title_text="Temperatura Máxima (°C)", secondary_y=False)
st.plotly_chart(fig_alertas)

#%%


st.markdown('''
            ### **Protocolo de Activación Institucional por Calor Extremo SEREMI Salud RM  Versión 01 (16-01-2024)**
            - Se establecen los siguientes criterios para la activación de alertas:
            - Verde Temprana Preventiva: 
                - Temperatura de 30ºC o más
            - Alerta Amarilla: 
                - Temperaturas maximas diarias de 34ºC o más, por al menos 2 días.
            - Alerta Roja: 
                - Temperaturas máximas diarias de 40ºC o más, por un dia o más. 
                - Temepraturas máximas diarias sde 34ºC o más, por al menos 3 dias.
''')

# Gráfico de tipo de alerta meteorológica
color_map_alertas = {
    'Sin Alerta': 'blue',  # Azul para días sin alerta
    'Verde Temprana Preventiva': 'green',  # Verde para Alerta Temprana Preventiva
    'Alerta Amarilla': 'yellow',  # Amarillo para Alerta Amarilla
    'Alerta Roja': 'red'  # Rojo para Alerta Roja
}

fig_alertas = make_subplots(specs=[[{"secondary_y": True}]])
fig_alertas.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['t_max'], name='Temperatura Máxima', mode='lines'),
    secondary_y=False,
)
fig_alertas.add_trace(
    go.Scatter(x=df_selec_est_def_period['date'], y=df_selec_est_def_period['total_defunciones'], name='Total de Defunciones', mode='lines', marker=dict(color='purple')),
    secondary_y=True,
)
for alerta, color in color_map_alertas.items():
    df_alerta = df_selec_est_def_period[df_selec_est_def_period['seremi_alerta'] == alerta]
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
df_selec_est_def['mes'] = df_selec_est_def['date'].dt.month_name()
años_disponibles = sorted(df_selec_est_def['date'].dt.year.unique())
indice_2024 = años_disponibles.index(2024) if 2024 in años_disponibles else 0
año_selec = st.selectbox('Selecciona un año:', años_disponibles, index=indice_2024)
df_filter_año = df_selec_est_def[df_selec_est_def['date'].dt.year == año_selec]
df_filter_año['mes'] = df_selec_est_def['date'].dt.month_name()

fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas por Mes', 'Total de Defunciones por Mes'))
fig.add_trace(
    go.Box(x=df_filter_año['mes'], y=df_filter_año['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)
fig.add_trace(
    go.Box(x=df_filter_año['mes'], y=df_filter_año['total_defunciones'], name='Total de Defunciones', marker=dict(color='red')),
    row=1, col=2
)
fig.update_layout(height=600, width=800, title_text=f"Boxplots de Temperaturas Máximas y Total de Defunciones por Mes del año {año_selec}")
fig.update_xaxes(title_text="Mes", row=1, col=1)
fig.update_yaxes(title_text="Temperatura Máxima (°C)", row=1, col=1)
fig.update_xaxes(title_text="Mes", row=1, col=2)
fig.update_yaxes(title_text="Total de Defunciones", row=1, col=2)
st.plotly_chart(fig)
#%%
# %%
st.write('## Gráfico de boxplots de temperaturas máximas y total de defunciones por mes específico a lo largo de los años')

# Asegúrate de que 'date' es una columna de tipo datetime
df_selec_est_def['date'] = pd.to_datetime(df_selec_est_def['date'])

# Extrae el nombre del mes y el año de la columna 'date'
df_selec_est_def['mes'] = df_selec_est_def['date'].dt.strftime('%B')
df_selec_est_def['year'] = df_selec_est_def['date'].dt.year

# Crea una lista de los nombres de los meses disponibles en los datos
meses_disponibles = df_selec_est_def['mes'].unique().tolist()
meses_disponibles.sort(key=lambda date: datetime.strptime(date, "%B"))

# Permite al usuario seleccionar un mes por nombre
mes_selec = st.selectbox('Selecciona un mes:', meses_disponibles)

# Filtra el dataframe para el mes seleccionado
df_filter_mes = df_selec_est_def[df_selec_est_def['mes'] == mes_selec]

# Crea boxplots para el mes seleccionado a lo largo de los años
fig = make_subplots(rows=1, cols=2, subplot_titles=('Temperaturas Máximas', 'Total de Defunciones'))

# Boxplot de temperaturas máximas por año para el mes seleccionado
fig.add_trace(
    go.Box(x=df_filter_mes['year'], y=df_filter_mes['t_max'], name='Temperaturas Máximas'),
    row=1, col=1
)

# Boxplot de total de defunciones por año para el mes seleccionado
fig.add_trace(
    go.Box(x=df_filter_mes['year'], y=df_filter_mes['total_defunciones'], name='Total de Defunciones', marker=dict(color='red')),
    row=1, col=2
)

# Actualiza el layout de la figura para incluir los nombres del mes y año en los títulos de los ejes
fig.update_layout(height=600, width=800, title_text=f"Boxplots de Temperaturas Máximas y Total de Defunciones por {mes_selec}")
fig.update_xaxes(title_text="Año", row=1, col=1)
fig.update_yaxes(title_text="Temperatura Máxima (°C)", row=1, col=1)
fig.update_xaxes(title_text="Año", row=1, col=2)
fig.update_yaxes(title_text="Total de Defunciones", row=1, col=2)

# Muestra el gráfico
st.plotly_chart(fig)
# %%
