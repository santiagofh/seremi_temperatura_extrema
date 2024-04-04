#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import plotly.graph_objs as go
#%%
st.set_page_config(
    page_title="Temperatura Extrema",
    page_icon="🌡",
)

# Cargar los datos (Asumiendo que ya has cargado y preparado 'df' y 'df_est' como antes)
df = pd.read_csv("data/tmm_historico_2013_2024.csv")
df_est = pd.read_excel("data/est_meteo.xlsx")
df_def_17 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2017", skiprows=3, usecols="B:I")
df_def_18 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2018", skiprows=3, usecols="B:I")
df_def_19 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2019", skiprows=3, usecols="B:I")
df_def_20 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2020", skiprows=3, usecols="B:I")
df_def_21 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2021", skiprows=3, usecols="B:I")
df_def_22 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2022", skiprows=3, usecols="B:I")
df_def_23 = pd.read_excel("data/Defunciones totales 2017 a 2024.xlsx", sheet_name="2023-2024", skiprows=3, usecols="B:I")
#%%
# Lista de DataFrames
ls_df_def = [
    df_def_17,
    df_def_18,
    df_def_19,
    df_def_20,
    df_def_21,
    df_def_22,
    df_def_23.rename(columns={'Unnamed: 1': 'FECHADEF'})  # Asumiendo que solo el último necesita renombrar esta columna
]

# Concatenar todos los DataFrames en uno
df_def = pd.concat(ls_df_def)

# Renombrar columna de fecha para uniformidad
df_def.rename(columns={'FECHADEF': 'fecha'}, inplace=True)

# Convertir la columna 'fecha' a datetime
df_def = df_def.dropna()
df_def['fecha'] = pd.to_datetime(df_def['fecha'])

# Calcular el total de defunciones para cada fecha
df_def['total_defunciones'] = df_def.iloc[:, 1:].sum(axis=1)
#%%
# Funciones
def evaluar_alertas(df):
    df['alerta'] = 'Sin Alerta' 
    df['mes'] = df['date'].dt.month
    df.loc[df['mes'].isin([11, 12, 1, 2, 3]), 'alerta'] = 'Alerta temprana preventiva'
    df.loc[df['t_max'] >= 40, 'alerta'] = 'Alerta Roja'
    df['alerta_temporal'] = df['t_max'] >= 34
    df['alerta_consecutiva'] = df['alerta_temporal'].rolling(window=2).sum()
    df.loc[df['alerta_consecutiva'] >= 2, 'alerta'] = 'Alerta Amarilla'
    df['alerta_consecutiva_3'] = df['alerta_temporal'].rolling(window=3).sum()
    df.loc[df['alerta_consecutiva_3'] >= 3, 'alerta'] = 'Alerta Roja'
    return df
def evaluar_sobre35(df):
    df['sobre_35'] = 'Bajo 35' 
    df.loc[df['t_max'] >= 35, 'sobre_35'] = 'Sobre 35'
    return df
def agregar_defunciones_a_grafico(fig, df):
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['total_defunciones'],
            name='Defunciones Totales',
            yaxis='y2',
            marker=dict(
                color='purple'
            )
        )
    )
    fig.update_layout(
        yaxis2=dict(
            title='Defunciones Totales',
            overlaying='y',
            side='right'
        )
    )
    return fig
#%%
# Preparar los datos de fecha y códigos de estaciones, si aún no se ha hecho
if not pd.api.types.is_datetime64_any_dtype(df['date']):
    df['date'] = pd.to_datetime(df['date'])

# Asegurarse de que los códigos de las estaciones estén en el formato correcto
df['est'] = df['est'].astype(str)
df_est['CODIGO'] = df_est['CODIGO'].astype(str)


df = pd.merge(df, df_def, left_on='date', right_on='fecha', how='left')


#%%

# TITULO
st.write("# SEREMI RM - Analisis exploratorio de datos - Temperaturas extremas")

## Mapa

## Selección de 

# Encontrar el código de la estación basado en el nombre seleccionado
# Crear un selectbox para seleccionar la estación
estaciones = df_est['NOMBRE'].tolist()  # Asume que df_est tiene una columna 'NOMBRE' para los nombres de las estaciones
indice_quinta_normal = estaciones.index('Quinta Normal') if 'Quinta Normal' in estaciones else 0
nombre_estacion_seleccionada = st.selectbox('Selecciona una estación:', estaciones,index=indice_quinta_normal)
codigo_estacion_seleccionada = df_est[df_est['NOMBRE'] == nombre_estacion_seleccionada]['CODIGO'].iloc[0]


# Filtrar los datos para la estación seleccionada
df_seleccionado = df[df.est == codigo_estacion_seleccionada]
df_est = df_est[df_est.CODIGO==codigo_estacion_seleccionada]
st.title("Mapa de Estaciones")
st.map(df_est, latitude="lat", longitude="long", color="#0000ff", size=100 ,zoom=10)

# Figura 1
st.write(f"## Temperaturas máximas para la estación {nombre_estacion_seleccionada} desde el año 2013")
fig = px.line(df_seleccionado, x='date', y='t_max', title=f'Temperaturas Máximas para {nombre_estacion_seleccionada}')
fig.add_hline(y=34, line_dash="dot", line_color="yellow", annotation_text="34°C", annotation_position="bottom right")
fig.add_hline(y=40, line_dash="dot", line_color="red", annotation_text="40°C", annotation_position="bottom right")
fig.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="30°C", annotation_position="bottom right")
st.plotly_chart(fig, use_container_width=True)
# Figura 2
st.write(f"## Temperaturas máximas para la estación {nombre_estacion_seleccionada} desde el año 2023")
df_seleccionado_2023 = df_seleccionado[df_seleccionado['date'] >= '2023-01-01']
fig2 = px.line(df_seleccionado_2023, x='date', y='t_max', title=f'Temperaturas Máximas desde el año 2023 para {nombre_estacion_seleccionada}')
fig2.add_hline(y=34, line_dash="dot", line_color="yellow", annotation_text="34°C", annotation_position="bottom right")
fig2.add_hline(y=40, line_dash="dot", line_color="red", annotation_text="40°C", annotation_position="bottom right")
fig2.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="30°C", annotation_position="bottom right")

st.plotly_chart(fig2, use_container_width=True)
#%%
st.write(f"## Tipos de alerta para la estación {nombre_estacion_seleccionada} desde el año 2023")
def visualizar_alertas_con_marcadores(df):
    df=evaluar_alertas(df)
    # Mapeo de colores para cada tipo de alerta
    color_map = {
        'Sin Alerta': 'blue',  # Azul para días sin alerta
        'Alerta temprana preventiva': 'green',        # Verde para Alerta Temprana Preventiva
        'Alerta Amarilla': 'yellow',  # Amarillo para Alerta Amarilla
        'Alerta Roja': 'red'   # Rojo para Alerta Roja
    }
    
    # Crear la figura
    fig = px.line(df, x='date', y='t_max', title=f'Temperaturas Máximas y Alertas para {nombre_estacion_seleccionada}', color_discrete_sequence=['grey'])

    # Agregar marcadores de colores
    for alerta, color in color_map.items():
        df_alerta = df[df['alerta'] == alerta]
        fig.add_scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color),)

    return fig

# Usar la función actualizada para generar y mostrar el gráfico
fig_con_alertas_con_marcadores = visualizar_alertas_con_marcadores(df_seleccionado_2023)
fig_con_alertas_con_marcadores = agregar_defunciones_a_grafico(fig_con_alertas_con_marcadores,df_seleccionado_2023)
st.plotly_chart(fig_con_alertas_con_marcadores, use_container_width=True)

# %%
def listar_eventos_alerta_con_temp(df):
    # Filtrar solo Alertas Amarillas y Rojas
    df_alertas = df[df['alerta'].isin(['Alerta Amarilla', 'Alerta Roja'])]

    # Ordenar por fecha
    df_alertas = df_alertas.sort_values(by='date')

    # Seleccionar las columnas relevantes, incluyendo la temperatura máxima
    eventos_alerta = df_alertas[['date', 'alerta', 't_max']].reset_index(drop=True)
    eventos_alerta.columns = ['Fecha', 'Tipo de Alerta', 'Temperatura Máxima']

    return eventos_alerta

# Aplicar la función y obtener la lista de eventos de alerta con temperatura
eventos_alerta_df_con_temp = listar_eventos_alerta_con_temp(df_seleccionado_2023)

# Mostrar los eventos de alerta con temperatura en el dashboard

st.write("## Eventos de Alertas Amarillas y Rojas con Temperatura Máxima")
st.table(eventos_alerta_df_con_temp)
def visualizar_sobre35_con_marcadores(df):
    df=evaluar_sobre35(df)
    # Mapeo de colores para cada tipo de alerta
    color_map = {
        'Sobre 35': 'red',  # Azul para días sin alerta
        'Bajo 35': 'blue',  # Azul para días sin alerta
    }
    
    # Crear la figura
    fig = px.line(df, x='date', y='t_max', title=f'Temperaturas Máximas y Alertas para {nombre_estacion_seleccionada}', color_discrete_sequence=['grey'])

    # Agregar marcadores de colores
    for alerta, color in color_map.items():
        df_alerta = df[df['sobre_35'] == alerta]
        fig.add_scatter(x=df_alerta['date'], y=df_alerta['t_max'], mode='markers', name=alerta, marker=dict(color=color),)

    return fig
def listar_eventos_alerta35_con_temp(df):
    # Filtrar solo Alertas Amarillas y Rojas
    df_alertas = df[df['sobre_35'].isin(['Sobre 35'])]

    # Ordenar por fecha
    df_alertas = df_alertas.sort_values(by='date')

    # Seleccionar las columnas relevantes, incluyendo la temperatura máxima
    eventos_alerta = df_alertas[['date', 'sobre_35', 't_max']].reset_index(drop=True)
    eventos_alerta.columns = ['Fecha', 'Alerta', 'Temperatura Máxima']

    return eventos_alerta
fig_con_alertas35_con_marcadores = visualizar_sobre35_con_marcadores(df_seleccionado_2023)
agregar_defunciones_a_grafico(fig_con_alertas35_con_marcadores,df_seleccionado_2023)
eventos_alerta_df_con_temp35 = listar_eventos_alerta35_con_temp(df_seleccionado_2023)
st.write(f"## Eventos sobre 35 grados en la estación {nombre_estacion_seleccionada}")
st.plotly_chart(fig_con_alertas35_con_marcadores, use_container_width=True)
st.table(eventos_alerta_df_con_temp35)
# %%