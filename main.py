import streamlit as st
import pandas as pd

#Configurações das páginas

sobre_mim = st.Page(page='views/sobre_mim.py', title='Sobre Mim', icon=':material/function:' , default=True)

formula1 = st.Page(page='views/formula_1.py', title='🏎️ F1 Dashboard')
st.set_page_config(layout='wide')

energy = st.Page(page='views/energy_case.py', title='💡 Demanda de energia')

house_prices = st.Page(page='views/house_prices.py', title='🏠 Previsão de Imóveis')

#Criando Navegação 

pg = st.navigation(
    {
        'Informações': [sobre_mim],
        'Projetos': [formula1, energy, house_prices],
    })

pg.run()