#%%
import pandas as pd
import plotly.express as px
import pydeck as pdk
import plotly.graph_objs as go

#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import plotly.graph_objs as go
#%%
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
df_def = pd.concat(ls_df_def)
df_def.rename(columns={'FECHADEF': 'fecha'}, inplace=True)
df_def['total_defunciones'] = df_def.iloc[:, 1:].sum(axis=1)
df_def.dropna(subset=['fecha'])
df_def.to_excel("df_def['total_defunciones'].xlsx")
df_def = df_def.reset_index(drop=True)
#%%
df['date'] = pd.to_datetime(df['date'])
df_def['fecha'] = pd.to_datetime(df_def['fecha'], errors='coerce')
# %%
## FUNCIONES DE EVALUACION DE ALERTAS 
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
#%%
df = evaluar_alertas(df)
df = evaluar_sobre35(df)

# %%
df.to_csv("data/datos_meteo.csv")
df_est.to_csv("data/datos_est.csv")
df_def.to_csv("data/datos_def.csv")
# %%
