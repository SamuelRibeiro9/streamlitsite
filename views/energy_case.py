import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Demanda de energia no :green[Brasil]')
st.write('''Dashboard de acompanhamento e análise comparativa durante períodos.
 Essas informações foram retiradas a partir de uma análise exploratória feita utilizando uma base kaggle, para mais informações acesse o link abaixo:''')
st.link_button('Análise no GitHub', 'https://github.com/SamuelRibeiro9/demandaenergiabrasil')
st.divider()

@st.cache_data
def carregar_dados():
    arquivo = pd.read_csv('bases/f1_dados_tratados.csv', sep=';')
    return arquivo

df = carregar_dados()
container = st.container(border=True)

data_inicial, data_final = container.select_slider('Selecione o ano que deseja filtrar', options=df.year.unique(), value=(2021, 2022))
df = df.loc[(df['year'] >= data_inicial) & (df['year'] <= data_final)]

st.write('')
col_esquerda, col_direita = st.columns(2)


col_esquerda.bar_chart(df, x='year', y='hourly_demand', x_label='Ano', stack=False, y_label='Demanda por hora', color='#bcbd22')
col_direita.bar_chart(df, x='hour', y='hourly_demand', x_label='Hora', stack=False, y_label='Demanda por hora', color='#2ca02c')

fig = px.box(df, x='day_of_week', y='hourly_demand', labels={'hourly_demand':'Demanda por hora','day_of_week': 'Dia da semana'}, color='day_of_week')
fig.update_xaxes(tickvals=[0,1,2,3,4,5,6], ticktext=['Segunda','Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])
boxplot1 = col_esquerda.plotly_chart(fig, on_select='rerun')

fig = px.box(df, x='season', y='hourly_demand', labels={'hourly_demand':'Demanda por hora','season': 'Estação do ano'}, color='season')
boxplot2 = col_direita.plotly_chart(fig, on_select='rerun')



