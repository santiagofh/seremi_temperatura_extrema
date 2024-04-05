#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from io import StringIO
import plotly.express as px
from io import BytesIO
import certifi
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request is being made')

#%%
## Temperatura Media Mensual
url_tmm = 'https://climatologia.meteochile.gob.cl/application/mensual/temperaturaMediaMensual'
est=[
'340045',
'330075',
'330160',
'330113',
'330030',
'330122',
'330077',
'330019',
'330020',
'330114',
'330021',
'330121',
'330118',
'330193',
'320019',
'320051',
'320063',
'320056',
'320041',
'320049'
]
#%%
## Funciones
def extraeTable(url):
    response = requests.get(url, timeout=360, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        string_io_table = StringIO(str(table))
        df = pd.read_html(string_io_table)[0]
        return df
    else:
        print(f'Error al realizar la solicitud: {response.status_code}')
        return None
def extraer_est_fecha_de_url(url):
    if pd.notnull(url):
        match = re.search(r'(\d{6})/(\d{4})/(\d{1,2})$', url)
        if match:
            est, año, dia = match.groups()
            return est, año, dia
    return None, None, None  # Retorna None para cada parte si la URL no es una cadena de texto o no coincide
def url_agregar_fecha(url,fechas):
    ls=[]
    for i in fechas:
        url_year_month=url+i
        ls.append(url_year_month)
    return ls

#%%
# Fechas y estaciones
inicio = datetime(2013, 1, 1)
fin = datetime.now()
fechas = []
while inicio <= fin:
    fecha_formateada = '/' + str(inicio.year) + '/' + str(inicio.month)
    fechas.append(fecha_formateada)
    if inicio.month == 12:
        inicio = inicio.replace(year=inicio.year + 1, month=1)
    else:
        inicio = inicio.replace(month=inicio.month + 1)
for fecha in fechas:
    print(fecha)
ls_est_fecha=[]
for i in est:
    for j in fechas:
        ls_est_fecha.append(i+j)
print(ls_est_fecha)

#%%
import time
ls_tmm = []
no_ls_tmm = []
indice_ultimo_intento = 0  # Guarda el índice del último intento
for i in ls_est_fecha[indice_ultimo_intento:]:
    url_est_fecha = url_tmm + '/' + i
    print(f"Intentando acceder a: {url_est_fecha}")
    try:
        df = extraeTable(url_est_fecha)
        df['url'] = i
        ls_tmm.append(df)
        indice_ultimo_intento += 1
    except ConnectionError as e:
        print(f"Error de conexión: {e}")
        no_ls_tmm.append(url_est_fecha)
        time.sleep(5*60) 
        continue 
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        no_ls_tmm.append(url_est_fecha)
        continue

#%%
        
tmm=pd.concat(ls_tmm)
# %%
if isinstance(tmm.columns, pd.MultiIndex):
    tmm.columns = ['_'.join(map(str, col)).strip() for col in tmm.columns.values]
tmm_reduced = tmm.iloc[1:].reset_index(drop=True)
tmm_reduced = tmm_reduced.iloc[:, [*range(11)]]
tmm_reduced = tmm_reduced.rename(columns={tmm_reduced.columns[0]: 'day',
                                          tmm_reduced.columns[1]: 't_min',
                                          tmm_reduced.columns[2]: 'ht_min',
                                          tmm_reduced.columns[3]: 't_max',
                                          tmm_reduced.columns[4]: 'ht_max',
                                          tmm_reduced.columns[5]: 'Climatologica',
                                          tmm_reduced.columns[6]: 'Aritmetica',
                                          tmm_reduced.columns[7]: 'col_7',
                                          tmm_reduced.columns[8]: 'col_8',
                                          tmm_reduced.columns[9]: 'col_9',
                                          tmm_reduced.columns[10]: 'url',
                                          })

tmm_reduced['t_max'] = pd.to_numeric(tmm_reduced['t_max'], errors='coerce')
tmm_reduced['t_min'] = pd.to_numeric(tmm_reduced['t_min'], errors='coerce')
tmm_reduced['day'] = pd.to_numeric(tmm_reduced['day'], errors='coerce')
tmm_reduced = tmm_reduced.dropna(subset=['t_max'])
tmm_reduced = tmm_reduced.dropna(subset=['day'])
#%%
# add Est, Year Month 
resultados = tmm_reduced['url'].apply(lambda x: extraer_est_fecha_de_url(x) if pd.notnull(x) else (None, None, None))
temp_df = pd.DataFrame(resultados.tolist(), columns=['est', 'year', 'month'], index=tmm_reduced.index)
#%%
tmm_reduced_date = pd.concat([tmm_reduced, temp_df], axis=1)
tmm_reduced_date['date'] = pd.to_datetime(tmm_reduced_date[['year', 'month', 'day']])
tmm_faltantes = pd.DataFrame(no_ls_tmm, columns=['url_faltantes'])
# %%
tmm_reduced_date.to_csv("data/tmm_historico_2013_2024.csv")
tmm_faltantes.to_csv("data/tmm_faltantes.csv") 