import streamlit as st
import pandas as pd 

st.title(''':red[Fórmula 1] :grey[Dashboard]''')
st.write('''Painel interativo criado a apartir do tratamento de dados das bases das corridas de fórmula 1 de 1950 a 2024. Caso queira conferir algumas análises desse projeto
         clique no botão abaixo: ''')
st.link_button('Análise no GitHub', 'https://github.com/SamuelRibeiro9/formula1stats')

#Função para carregar a base de dados
@st.cache_data
def carregar_dados():
    arquivo = pd.read_csv('bases/f1_dados_tratados.csv', sep=';')
    return arquivo

df = carregar_dados()
st.divider()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Pilots
st.header(':green[Pilotos]')

driver = st.selectbox('Selecione um piloto para verificar as estatísticas:' , sorted(df['driver_name'].unique()), index=62, placeholder="Pilotos")
df_filtrado = df.loc[df['driver_name'] == driver, :]
df_agrupado = df_filtrado.groupby(['driver_name', 'year'], as_index=False).sum()

#Estatísticas de piloto
    #Quantidade de pontos conquistados
container = st.container(border=True)
container.write('Pontos conquistados')
container.bar_chart(df_agrupado , x='year' , y= 'points', stack=False, x_label='Ano', y_label='Pontos por temporada', color=['#FF0000'], use_container_width=True)

col_esquerda, col_meio ,col_direita = st.columns(3, gap='medium', vertical_alignment= 'center')

with col_esquerda:
    #Quantidade de prêmios disputados
    st.metric('Quantidade de corridas disputadas', df_filtrado['circuit_name'].count())

with col_meio:
    #Média de pontos por corrida
    st.metric('Média de pontos por corrida', round(df_filtrado['points'].sum() / df_filtrado['circuit_name'].count(), 1))

with col_direita:
    #Quantidade de vitórias
    st.metric('Quantidade de vitórias', df_filtrado['wins'].sum())

st.subheader('Circuitos vencidos')
    #Mapa da localização dos prêmios em que venceu
st.map(df_filtrado.loc[df_filtrado['wins'] == 1], latitude= 'lat', longitude='lng')

st.divider()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Equipes
st.header(':green[Construtores]')
equipe = st.selectbox('Selecione uma equipe para verificar as estatísticas:', sorted(df['team_name'].unique()), index=134, placeholder="Construtores")
#st.dataframe(df.loc[df['team_name'] == equipe, :])

df_filtrado = df.loc[df['team_name'] == equipe, :]
df_agrupado = df_filtrado.groupby(['team_name', 'year'], as_index=False).sum()

#Estatísticas de construtores
    #Quantidade de pontos conquistados
container = st.container(border=True)
container.write('Pontos conquistados')
container.bar_chart(df_agrupado , x='year' , y= 'points', stack=False, x_label='Ano', y_label='Pontos por temporada', color=['#00b400'], use_container_width=True)

col_esquerda, col_meio ,col_direita = st.columns(3, gap='medium', vertical_alignment= 'center')

with col_esquerda:
    #Quantidade de prêmios disputados
    st.metric('Quantidade de corridas disputadas', df_filtrado['circuit_name'].count())

with col_meio:
    #Média de pontos por corrida
    st.metric('Média de pontos por corrida', round(df_filtrado['points'].sum() / df_filtrado['circuit_name'].count(), 1))

with col_direita:
    #Quantidade de vitórias
    st.metric('Quantidade de vitórias', df_filtrado['wins'].sum())
