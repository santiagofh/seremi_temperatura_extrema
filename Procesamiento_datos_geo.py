#%%
import pandas as pd
df_met=pd.read_csv('data/datos_meteo.csv')
df_est=pd.read_csv('data/datos_est.csv')
# %%
selec_col_met=['est','day','month','year','date','t_min','t_max','Aritmetica','sobre_35_alerta','senapred_alerta']
selec_col_est=['CODIGO', 'NOMBRE','lat','long', 'X', 'y']
# %%
df_met_select=df_met[selec_col_met]
df_est_select=df_est[selec_col_est]
# %%
df_met_est = df_met_select.merge(df_est_select, how='left', left_on='est', right_on='CODIGO')
# %%
df_met_est['senapred_sin_alerta'] = df_met_est['senapred_alerta'].apply(lambda x: x == 'Sin Alerta')
df_met_est['senapred_alerta_temprana_preventiva'] = df_met_est['senapred_alerta'].apply(lambda x: x == 'Alerta Temprana Preventiva')
df_met_est['senapred_alerta_amarilla'] = df_met_est['senapred_alerta'].apply(lambda x: x == 'Alerta Amarilla')
df_met_est['senapred_alerta_roja'] = df_met_est['senapred_alerta'].apply(lambda x: x == 'Alerta Roja')
# %%
df_met_est.to_csv("data/datos_metereologicos_estaciones_2013_2024.csv")
df_met_est.to_excel("data/datos_metereologicos_estaciones_2013_2024.xlsx")
# %%
