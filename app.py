import pandas as pd
import streamlit as st
import plotly_express as px

car_data = pd.read_csv('vehicles_us.csv')
st.title('Análisis de anuncios de venta de coches en EE.UU.')
st.write('Este conjunto de datos contiene anuncios de venta de coches en EE.UU. y se puede utilizar para analizar tendencias en el mercado de coches usados.')
hist_button = st.button('Construit Histograma')
disp_button = st.button('Construit Diagrama de Dispersión')  

if hist_button: # al hacer clic en el botón
         # escribir un mensaje
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
         
         # crear un histograma
    fig = px.histogram(car_data, x="odometer")
     
         # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)
elif disp_button: # al hacer clic en el botón
         # escribir un mensaje
    st.write('Creación de un diagrama de dispersión para el conjunto de datos de anuncios de venta de coches')
         
         # crear un diagrama de dispersión
    fig = px.scatter(car_data, x="year", y="price")
     
         # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)