import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import numpy as np
import shapely

from joblib import load

DADOS_LIMPOS = 'bases/housing_clean.parquet'
DADOS_GEO_MEDIAN =  'bases/gdf_counties.parquet'
MODELO_FINAL = 'modelos/ridge_polyfeat_target_quantile.joblib'

st.title('''Previsão de Imóveis''')
st.write('''Painel interativo criado para o usuário prever o valor de um imóvel da região da Califórnia. 
        Caso queira conferir algumas análises desse projeto e construção do modelo
        a partir de dados do senso desse estado
         clique no botão abaixo: ''')
st.link_button('Análise no GitHub', 'https://github.com/SamuelRibeiro9/02_house_prices.git')

@st.cache_data
def carregar_dados_limpos():
    return pd.read_parquet(DADOS_LIMPOS)

@st.cache_data
def carregar_dados_geo():
    gdf_geo = gpd.read_parquet(DADOS_GEO_MEDIAN)
    gdf_geo = gdf_geo.explode(ignore_index=True) #Explodir multipoligonos em individuais
    #Corrigir os dados de geometrias para aplicação no gráfico de mapa
    def fix_and_orient_geometry(geometry):
        if not geometry.is_valid:
            geometry = geometry.buffer(0) #Fixar geometria inválida
        #Orientar o poligono para o sentido anti-horário
        if isinstance(
            geometry, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)
        ):
            geometry = shapely.geometry.polygon.orient(geometry, sign=1.0)
        return geometry
    #Aplicar a função de fixar e orientar as geometrias
    gdf_geo['geometry'] = gdf_geo['geometry'].apply(fix_and_orient_geometry)

    #Extrair as coordenadas dos polígonos
    def get_polygon_coordinates(geometry):
        return (
            [[[x, y] for x, y in geometry.exterior.coords]]
            if isinstance(geometry, shapely.geometry.Polygon)
            else[
                [[x, y] for x, y in polygon.exterior.coord]
                for polygon in geometry.geoms
            ]
        )
    #Aplicando a conversão de coordenada e sobrescrevendo o valor     
    gdf_geo['geometry'] = gdf_geo['geometry'].apply(get_polygon_coordinates)
        
    return gdf_geo

@st.cache_resource
def carregar_modelo():
    return load(MODELO_FINAL)

df = carregar_dados_limpos()
gdf_geo = carregar_dados_geo()
modelo = carregar_modelo()

col1, col2 = st.columns(2)

with col1:

    with st.form(key='form'):
        condados = sorted(gdf_geo['name'].unique())
        selecionar_condado = st.selectbox('Condados', condados)

        longitude = gdf_geo.query('name == @selecionar_condado')['longitude'].values
        latitude = gdf_geo.query('name == @selecionar_condado')['latitude'].values
        housing_median_age = st.number_input('Idade do Imóvel', min_value=1, max_value=50, value=10)
        total_rooms = gdf_geo.query('name == @selecionar_condado')['total_rooms'].values
        total_bedrooms = gdf_geo.query('name == @selecionar_condado')['total_bedrooms'].values
        population = gdf_geo.query('name == @selecionar_condado')['population'].values
        households = gdf_geo.query('name == @selecionar_condado')['households'].values
        median_income = st.slider('Renda média (milhares US$k)', 5.0, 100.0, value=70.0, step=5.0)
        ocean_proximity = gdf_geo.query('name == @selecionar_condado')['ocean_proximity'].values
        bins_income = [0, 1.5, 3, 4.5, 6, np.inf]
        median_income_cat = np.digitize(median_income / 10, bins=bins_income)
        rooms_per_households = gdf_geo.query('name == @selecionar_condado')['rooms_per_households'].values
        bedrooms_per_room = gdf_geo.query('name == @selecionar_condado')['bedrooms_per_room'].values
        population_per_households = gdf_geo.query('name == @selecionar_condado')['population_per_households'].values

        entrada_modelo = {
            'longitude': longitude,
            'latitude': latitude,
            'housing_median_age': housing_median_age,
            'total_rooms': total_rooms,
            'total_bedrooms': total_bedrooms,
            'population': population,
            'households': households,
            'median_income': median_income / 10,
            'ocean_proximity': ocean_proximity,
            'median_income_cat': median_income_cat,
            'rooms_per_households': rooms_per_households,
            'bedrooms_per_room': bedrooms_per_room,
            'population_per_households': population_per_households,
        }

        df_entrada_modelo = pd.DataFrame(entrada_modelo)

        botao_previsao = st.form_submit_button('Executar previsão')

        if botao_previsao:
            preco = modelo.predict(df_entrada_modelo)
            st.metric(label='Preço previsto:', value=f'US$ {preco[0][0]:.2f}')

with col2: 
    view_state = pdk.ViewState(
        latitude= float(latitude[0]),
        longitude= float(longitude[0]),
        zoom= 5,
        min_zoom= 5,
        max_zoom= 15, 
    )

    polygon_layer = pdk.Layer(
        'PolygonLayer',
        data= gdf_geo[['name', 'geometry']],
        get_polygon= 'geometry',
        get_fill_color=[0, 0, 255, 25],
        get_line_color=[255, 255, 255],
        get_line_width= 250,
        pickable=True,
        auto_highlight= True,
    )

    condado_selecionado = gdf_geo.query('name == @selecionar_condado')
    highlight_layer = pdk.Layer(
        'PolygonLayer',
        data= condado_selecionado[['name', 'geometry']],
        get_polygon='geometry',
        get_fill_color=[255, 0, 0, 100],
        get_line_color=[0, 0, 0],
        get_line_width= 500,
        pickable=True,
        auto_highlight= True,
    ) 

    tooltip = {
        'html': '<b>Condado:</b> {name}',
        'style': {'backgroundColor': 'steelblue', 'color': 'white', 'fontsize': '10px'},
    }

    mapa = pdk.Deck(
        initial_view_state=view_state,
        layers=[polygon_layer, highlight_layer],
        tooltip=tooltip,
    )

    st.pydeck_chart(mapa)