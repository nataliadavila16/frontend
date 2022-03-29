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
            chuva = 'nao chove'
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

url = 'https://apirpm-2pjnslwdia-uc.a.run.app/bucket'
dado = requests.get(url).json()
df_previsoes = pd.DataFrame(dado['Previsao'])

original_title = '<p style="color:Red; font-size: 16px">Chuva muito forte para as seguintes localidades:</p>'
st.write(original_title, unsafe_allow_html=True)

df = pd.DataFrame(dado['Passado'])

dia0 = datetime.date.today()  #dia corrente
delta = datetime.timedelta(days=1)  #espaço de tempo
dia1 = dia0 + delta  #dia para mais 24h

st.write("### Previsão de chuva para as próximas 24h")


# c2.write('##### Hora:')
hora = st.slider('', 1, 24)
hora = str(hora)


r, b, g = [], [], []
print(df_previsoes[hora])

for mm in df_previsoes[hora].tolist():
    mm = float(mm)
    if mm < 1:
        cor = [0, 0, 0]
    elif mm >= 1 and mm <= 5.0:
        cor = [127,255,0]
    elif mm > 5.0 and mm <= 25.0:
        cor = [30,144,255]
    elif mm > 25.0 and mm <= 50.0:
        cor = [139,10,80]
    else:
        cor = [220,20,60]
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

a,b,c,d,e =st.columns(5)
original_title3 = '<p style="color:black; font-size: 14px">Não chove</p>'
original_title4 = '<p style="color:#7FFF00; font-size: 14px">Chuva fraca:<br /> até 5 mm</p>'
original_title5 = '<p style="color:	#1E90FF; font-size: 14px">Chuva moderada:<br /> 5 a 25 mm</p>'
original_title6 = '<p style="color:#8B0A50; font-size: 14px">Chuva forte:<br /> 25 a 50 mm</p>'
original_title7 = '<p style="color:#DC143C; font-size: 14px">Chuva muito forte:<br /> acima de 50 mm</p>'

A=a.write(original_title3, unsafe_allow_html=True)
B=b.write(original_title4, unsafe_allow_html=True)
C=c.write(original_title5, unsafe_allow_html=True)
D=d.write(original_title6, unsafe_allow_html=True)
E=e.write(original_title7, unsafe_allow_html=True)

t= datetime.datetime.now()
t=t.strftime("%Y-%m-%d  %H")
original_title2 = f'<p style="font-size: 28px">Tempo agora</p>'
st.sidebar.write(original_title2, unsafe_allow_html=True)
st.sidebar.write(f'{t}h')
option = st.sidebar.selectbox(
    'Escolha uma estação meteorológica',df.dc_nome.unique())

df = df[df['dc_nome']==option]

if df.Chuva.iloc[-1] < 1:
    st.sidebar.write(f'#### Chuva:    {classe_chuva(df.Chuva.iloc[-1])} 😀')

if df.Chuva.iloc[-1] >=1 and df.Chuva.iloc[-1] <= 25:
    st.sidebar.write(f'#### Chuva:    {classe_chuva(df.Chuva.iloc[-1])} ☔')

if df.Chuva.iloc[-1] > 25:
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
st.write('#### Temperatura °C, Vento m/s, Umidade Relativa % e Chuma mm, nas últimas 48h')
st.write('#### ')

x=np.arange(-48, 0)

def plot_temp(x,min_t, max_t):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(x,max_t,
             color='green',
             linestyle='dashdot',
             linewidth=1,
             marker='o',
             markerfacecolor='red',
             markersize=7)
    plt.plot(x,min_t,
             color='orange',
             linestyle='dashdot',
             linewidth=1,
             marker='o',
             markerfacecolor='blue',
             markersize=7)
    plt.ylim(min(min_t) - 2, max(max_t) + 2)
    plt.xlim(-48, 0)
    plt.xticks(x,fontsize=10)
    plt.yticks(fontsize=20)
    plt.grid(True, color='brown')
    plt.legend(["Temperatura Máxima", "Temperatura Mínima"],
               loc=0,
               fontsize=20)
    plt.xlabel('Horas passadas',fontsize=20)
    plt.ylabel('Temperatura °C', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Temperatura do ar (°C) nos útimos sete dias')
plot_temp(x,df.Temp_min, df.Temp_max)

# breakpoint()

'''


'''
def plot_vento(x,vel_vento):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(x,vel_vento,
             color='red',
             linestyle='-',
             linewidth=1,
             marker='o',
             markerfacecolor='blue',
             markersize=7)
    plt.ylim(0, max(vel_vento) + 1)
    plt.yticks(fontsize=20)
    plt.xlim(-48, 0)
    plt.xticks(x,fontsize=10)
    plt.grid(True, color='brown')
    plt.legend(["Intensidade do vento"], loc=0, fontsize=20)
    plt.xlabel('Horas Passadas', fontsize=20)
    plt.ylabel('Vento m/s', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Intensidade do vento (m/s) nos útimos sete dias')
plot_vento(x,df.Vel_vento)
'''


'''


def plot_umi(x,umidade):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(x,umidade,
             color='green',
             linestyle='-',
             linewidth=1,
             marker='o',
             markerfacecolor='green',
             markersize=7)
    plt.ylim(0, 110)
    plt.yticks(fontsize=20)
    plt.xlim(-48, 0)
    plt.xticks(x,fontsize=10)
    plt.grid(True, color='brown')
    plt.legend(["Umidade Relativa %"], loc=0, fontsize=20)
    # plt.xlabel('Data(mm/dd)')
    plt.ylabel('Umidade Relativa %', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Umidade Relativa % nos útimos sete dias')
plot_umi(x,df.Umid)

def plot_chuva(x,chuva):
    fig = plt.figure(figsize=(20, 8))
    plt.plot(x,chuva,
             color='blue',
             linestyle='-',
             linewidth=1,
             marker='o',
             markerfacecolor='blue',
             markersize=7)
    plt.ylim(0, max(chuva))
    plt.yticks(fontsize=20)
    plt.xlim(-48, 0)
    plt.xticks(x,fontsize=10)
    plt.grid(True, color='brown')
    plt.legend(["Precipitação %"], loc=0, fontsize=20)
    # plt.xlabel('Data(mm/dd)')
    plt.ylabel('Precipitação %', fontsize=25)
    # plt.title('6-Day Weather Forecast')
    st.pyplot(fig)
    # return fig


# st.subheader('Umidade Relativa % nos útimos sete dias')
plot_chuva(x,df.Chuva)
