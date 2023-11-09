# Trabajo Final Grupo 1
# USIL - CPEL 2023-2 
#Integrantes:
#•	Enrique Eduardo Rivera Morillo
#•	Guillermo Giovanni Rodríguez Bernuy
#•	Claudia Alexandra Rosales Glave
#•	Jamil Alberto Solorzano Peralta
#•	German Ricardo Tantalean Cardoza
#•	Timoteo Saavedra Mirtha Amelia

# Se instala las Librerias necesarias

import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Incidencias SETIEMBRE 2023") # Nombre para configurar paginma WEB
st.header('Resultados Incidencias  Setiembre 2023') # Titulo de la pagina
st.subheader('¿Que incidencias se presentaron en Setiembre 2023?') #Subtitulo
excel_file = '2023_Setiembre_Incidencias_SegCiudadana.xlsx' #Nombre archivo Excel a importar
sheet_name = 'Data' # Hoja de Excel a importar

df= pd.read_excel(excel_file, #importo archivo excel
                   sheet_name=sheet_name,#Le digo cual hoja necesito
                   usecols='B:M', # columnas ha usar
                   header=0) # desde que fila debe empezar a tomarse la información *empieza en cero*
df_incidencias = df.groupby(['TURNO'],as_index=False)['INCIDENCIAS'].count() # Se agrupa datos como una TABLA DINAMICA. para agrupar datos. Por cada Turno cuenta Incidencias

df_incidencias2 = df_incidencias
st.dataframe(df) # Se muestra dataframe de streamlim
st.write(df_incidencias2)

# Se crear un grafico de pie chart

pie_chart=px.pie(df_incidencias2, # Se toma el dataframe2
                 title = 'Cantidad de Incidencias por Turno Set 2023', # Titulo
                 values = 'INCIDENCIAS', # columna
                 names = 'TURNO') # para verlo por Turno --> colores

st.plotly_chart(pie_chart) # se muestra el dataframe en streamlit

# crear una lista con los parametros de la columna

turno = df['TURNO'].unique().tolist() # se crea una lista con columna Turno
semana = df['SEMANA'].unique().tolist() # se crea una lista con columna Semana
incidencia = df['INCIDENCIAS'].unique().tolist() # se crea una lista con columna Incidencia

# Se crea slicer de Semana de Incidencia

semana_selector = st.slider('Semana de la incidencia :',
                    min_value = min(semana), # Valor minimo de columna Semana
                    max_value = max(semana), # Valor maximo de columna Semana
                    value = (min(semana),max(semana))) # que tome desde el minimo al maximo

# crear multisectores

turno_selector = st.multiselect('Turno:',
                turno,
                default = turno)

incidencia_selector = st.multiselect('Incidencia:',
                                      incidencia,
                                      default = incidencia)

# Se utiliza selectores y slider para que se filtre informacion

mask=(df['SEMANA'].between(*semana_selector))&(df['INCIDENCIAS'].isin(incidencia_selector))&(df['TURNO'].isin(turno_selector))

numero_resultados = df[mask].shape[0] ##numero de filas disponibles
st.markdown(f'*Resultados Disponibles:{numero_resultados}*') ## sale como un titulo

#nueva agrupacion

df_agrupado = df[mask].groupby(by=['TURNO']).count()[['INCIDENCIAS']] #que agrupe por Turno e incidencias

#datos de Semana

df_agrupado=df_agrupado.rename(columns={'Incidencia': 'Semana'})
df_agrupado=df_agrupado.reset_index()

#Se crea y muestra grafico de barras

bar_chart = px.bar(df_agrupado,
            x='TURNO',
            y='INCIDENCIAS',
            text= 'INCIDENCIAS',
            color_discrete_sequence = ['#f5b632']*len(df_agrupado),
            template = 'plotly_white')

st.plotly_chart(bar_chart) # mostrar grafico
