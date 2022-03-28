from curses.panel import bottom_panel
from tkinter import W
import streamlit as st
import requests
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import pydeck as pdk
import datetime
import matplotlib.pyplot as plt

def classe_chuva(precipitacao):
        mm=precipitacao
        if np.isnan(mm):
            chuva = "NaN"
        if mm == 0:
            chuva = 0 #'nao chove'
        elif mm >0 and mm <=5.0:
            chuva = 1 #'fraca'
        elif mm >5.0 and mm<=25.0:
            chuva = 'moderada'
        elif mm >25.0 and mm<=50.0:
            chuva = 'forte'
        else:
            chuva = 'muito forte'
        return chuva

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Alerta Chuva SP')

st.write("### Atenção :warning:")

original_title = '<p style="color:Red; font-size: 16px">Chuva forte ou muito forte paras as seguintes localidades:</p>'
st.write(original_title, unsafe_allow_html=True)

# st.write("Chuva forte ou muito forte paras as seguintes localidades: ")

dia0 = datetime.date.today()  #dia corrente
delta = datetime.timedelta(days=1)  #espaço de tempo
dia1 = dia0 + delta  #dia para mais 24h

st.write("### Previsão de chuva para as próximas 24h")


# d1 = st.date_input("Previsão para:", dia0, max_value = dia1, min_value=dia0)
# # t1 = st.time_input('Hora', datetime.time(0, 0))

url = 'https://apirpm-2pjnslwdia-uc.a.run.app/bucket'
dado = requests.get(url).json()
df_previsoes = pd.DataFrame(dado['Previsao'])

# df_previsoes=pd.read_csv('exemplo_nat_all.csv')

# c2.write('##### Hora:')
hora = st.slider('', 0, 23)
hora = str(hora)


r, b, g = [], [], []
print(df_previsoes[hora])

for mm in df_previsoes[hora].tolist():
    mm = float(mm)
    if mm < 1:
        cor = [0, 0, 0]
    elif mm >= 1 and mm <= 5.0:
        cor = [128, 255, 0]
    elif mm > 5.0 and mm <= 25.0:
        cor = [0, 191, 255]
    elif mm > 25.0 and mm <= 50.0:
        cor = [191, 0, 255]
    else:
        cor = [255, 0, 0]
    r.append(cor[0])
    b.append(cor[1])
    g.append(cor[2])

df_previsoes['r'] = r
df_previsoes['b'] = b
df_previsoes['g'] = g
'''

'''

# Define a layer to display on a map
layer = pdk.Layer('ScatterplotLayer',
                  df_previsoes,
                  pickable=False,
                  opacity=0.3,
                  stroked=True,
                  filled=True,
                  radius_scale=1000,
                  radius_min_pixels=5,
                  radius_max_pixels=100,
                  line_width_min_pixels=1,
                  get_position=['Longitude', 'Latitude'],
                  get_radius=[hora],
                  get_fill_color=['r', 'b', 'g'],
                  get_line_color=['r', 'b', 'g'])
'''

'''
# Set the viewport location
view_state = pdk.ViewState(latitude=-21.980353, longitude=-47.883927, zoom=5)
# st.subheader(f'Previsão de Chuva para SP em {dia0}')
st.pydeck_chart(
    pdk.Deck(layers=[layer],
             initial_view_state=view_state,
             map_style="mapbox://styles/mapbox/light-v10"))


st.sidebar.write('### Tempo agora')

df = pd.DataFrame(dado['Passado'])

option = st.sidebar.selectbox(
    'Escolha uma estação meteorológica',df.dc_nome.unique())

df = df[df['dc_nome']==option]

if df.Chuva.iloc[-1] < 1:
    st.sidebar.write(f'#### Chuva:    {classe_chuva(df.Chuva.iloc[-1])}.')
if df.Chuva.iloc[-1] > 0 and df.Chuva.iloc[-1] < 25:
    st.sidebar.write(f'#### Chuva:    {classe_chuva(df.Chuva.iloc[-1])} ☔')
else:
    st.sidebar.write(f'#### Chuva:    {classe_chuva(df.Chuva.iloc[-1])} ⛈️')


col1, col2 = st.sidebar.columns(2)

col1.metric("Temperatura", f'{df.Temp.iloc[-1]} °C',
            f'{round(df.Temp.iloc[-1]-df.Temp.iloc[-24],ndigits=1)} °C')
col2.metric(
    "Vento", f'{round(df.Vel_vento.iloc[-1],ndigits=1)} m/s',
    f'{round(df.Vel_vento.iloc[-1]-df.Vel_vento.iloc[-24],ndigits=1)} m/s')
col1.metric("Umidade", f'{df.Umid.iloc[-1]} %',
            f'{round(df.Umid.iloc[-1]-df.Umid.iloc[-24],ndigits=1)} %')
col2.metric("Precipitação", f'{round(df.Chuva.iloc[-1],ndigits=1)} mm',
            f'{round(df.Chuva.iloc[-1]-df.Chuva.iloc[-24],ndigits=1)} mm')

st.write('#### ')
st.write('#### Temperatura °C, Vento m/s e Umidade Relativa % nas últimas 72h')
st.write('#### ')

hora_now = datetime.datetime.now()
dia_atual = hora_now.strftime("%Y-%m-%d")
dia_pas = (hora_now - datetime.timedelta(days=3)).strftime("%d-%HH")
df['datahora'] = dia_pas


def plot_temp(min_t, max_t):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(max_t,
             color='green',
             linestyle='dashdot',
             linewidth=1,
             marker='o',
             markerfacecolor='red',
             markersize=7)
    plt.plot(min_t,
             color='orange',
             linestyle='dashdot',
             linewidth=1,
             marker='o',
             markerfacecolor='blue',
             markersize=7)
    plt.ylim(min(min_t) - 2, max(max_t) + 2)
    # plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True, color='brown')
    plt.legend(["Temperatura Máxima", "Temperatura Mínima"],
               loc=0,
               fontsize=20)
    # plt.xlabel('Data(mm/dd)')
    plt.ylabel('Temperatura °C', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Temperatura do ar (°C) nos útimos sete dias')
plot_temp(df.Temp_min, df.Temp_max)
'''


'''
def plot_vento(days, vel_vento):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(days[-24 * 7:],
             vel_vento[-24 * 7:],
             color='blue',
             linestyle='-',
             linewidth=1,
             marker='o',
             markerfacecolor='blue',
             markersize=7)
    plt.ylim(0, max(vel_vento) + 1)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True, color='brown')
    plt.legend(["Intensidade do vento"], loc=0, fontsize=20)
    # plt.xlabel('Data(mm/dd)')
    plt.ylabel('Vento m/s', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Intensidade do vento (m/s) nos útimos sete dias')
plot_vento(df.datahora, df.Vel_vento)
'''


'''


def plot_umi(days, umidade):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(days[-24 * 7:],
             umidade[-24 * 7:],
             color='green',
             linestyle='-',
             linewidth=1,
             marker='o',
             markerfacecolor='green',
             markersize=7)
    plt.ylim(0, 110)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(True, color='brown')
    plt.legend(["Umidade Relativa %"], loc=0, fontsize=20)
    # plt.xlabel('Data(mm/dd)')
    plt.ylabel('Umidade Relativa %', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Umidade Relativa % nos útimos sete dias')
plot_umi(df.datahora, df.Umid)
