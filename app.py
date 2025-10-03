import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Vehículos - TripleTen",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- FUNCIÓN DE CARGA Y PREPROCESAMIENTO DE DATOS ---

@st.cache_data
def load_data(file_path):
    """Carga los datos y realiza un preprocesamiento básico."""
    df = pd.read_csv(file_path)

    # Limpieza de datos básica
    # Rellenar valores nulos en 'model_year' con la mediana
    df['model_year'] = df['model_year'].fillna(df['model_year'].median())
    df['model_year'] = df['model_year'].astype(int)

    # Rellenar valores nulos en 'odometer' con la mediana
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())

    # Crear una lista de fabricantes
    df['manufacturer'] = df['model'].apply(lambda x: x.split(' ')[0].lower())

    return df

# Cargar los datos
df = load_data('vehicles_us.csv')

# Filtrar fabricantes con menos de 1000 anuncios (cálculo de ejemplo)
manufacturer_counts = df['manufacturer'].value_counts()
small_manufacturers = manufacturer_counts[manufacturer_counts < 1000].index

# ----------------------------------------------------------------------
st.title("Aplicación Web Final - Análisis de Anuncios de Vehículos")
st.markdown("---")
# ----------------------------------------------------------------------

## 1. Data Viewer
# ----------------------------------------------------------------------
st.header("Data viewer")

# Checkbox de filtro (controla si se incluyen fabricantes pequeños)
include_small_mfrs = st.checkbox(
    "Include manufacturers with less than 1000 ads",
    value=True # Por defecto está marcado en el video
)

# Aplicar filtro
if not include_small_mfrs:
    df_filtered = df[~df['manufacturer'].isin(small_manufacturers)]
else:
    df_filtered = df

# Mostrar tabla de datos
st.dataframe(df_filtered.head(100), use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
## 2. Vehicle types by manufacturer
# ----------------------------------------------------------------------
st.header("Vehicle types by manufacturer")

# Agrupar datos para el gráfico de barras apiladas
df_type_mfr = df_filtered.groupby(['manufacturer', 'type']).size().reset_index(name='count')

# Crear gráfico interactivo con Plotly Express
fig_type_mfr = px.bar(
    df_type_mfr,
    x='manufacturer',
    y='count',
    color='type', # El color segmenta por tipo de vehículo
    title='Conteo de Tipos de Vehículos por Fabricante',
    labels={'count': 'Count', 'manufacturer': 'Manufacturer', 'type': 'Type'}
)
fig_type_mfr.update_layout(xaxis={'categoryorder':'total descending'}) # Ordenar fabricantes
st.plotly_chart(fig_type_mfr, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
## 3. Histogram of condition vs model_year
# ----------------------------------------------------------------------
st.header("Histogram of condition vs model_year")

# Crear histograma apilado de 'model_year' segmentado por 'condition'
fig_hist_condition = px.histogram(
    df_filtered,
    x='model_year',
    color='condition', # El color segmenta por condición
    title='Histograma de Condición vs. Año del Modelo',
    nbins=50, # Número de bins para el eje X
    histfunc='count',
    labels={'model_year': 'Model Year', 'count': 'Count'}
)
fig_hist_condition.update_layout(bargap=0) # Eliminar espacio entre barras
st.plotly_chart(fig_hist_condition, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------
## 4. Compare price distribution between manufacturers
# ----------------------------------------------------------------------
st.header("Compare price distribution between manufacturers")

# Obtener la lista única de fabricantes para los selectboxes
all_manufacturers = sorted(df_filtered['manufacturer'].unique().tolist())

col_mfr1, col_mfr2 = st.columns(2)

# Selectbox para el fabricante 1
with col_mfr1:
    manufacturer_1 = st.selectbox(
        "Select manufacturer 1",
        options=all_manufacturers,
        index=all_manufacturers.index('chevrolet') if 'chevrolet' in all_manufacturers else 0,
        key='manufacturer_1'
    )

# Selectbox para el fabricante 2
with col_mfr2:
    manufacturer_2 = st.selectbox(
        "Select manufacturer 2",
        options=all_manufacturers,
        index=all_manufacturers.index('bmw') if 'bmw' in all_manufacturers else 0,
        key='manufacturer_2'
    )

# Checkbox para normalizar el gráfico
normalize = st.checkbox("Normalize histogram", value=True)

# Filtrar datos para los dos fabricantes seleccionados
df_comparison = df_filtered[
    df_filtered['manufacturer'].isin([manufacturer_1, manufacturer_2])
]

# Definir la propiedad de normalización
histnorm_value = 'percent' if normalize else 'count'

# Crear el histograma de comparación de precios
fig_price_comp = px.histogram(
    df_comparison,
    x='price',
    color='manufacturer',
    histnorm=histnorm_value, # Normaliza a porcentaje si está marcada la casilla
    opacity=0.6,
    barmode='overlay', # Superponer las barras
    title=f'Distribución de Precios: {manufacturer_1.title()} vs {manufacturer_2.title()}',
    labels={'price': 'Price', histnorm_value: histnorm_value.title()}
)

# Ajustar diseño
fig_price_comp.update_layout(xaxis_title="Price (USD)", yaxis_title=histnorm_value.title())

st.plotly_chart(fig_price_comp, use_container_width=True)

# ----------------------------------------------------------------------

