import pandas as pd
import streamlit as st # type ignored
import plotly.graph_objects as go  # Cambiamos a go para crear áreas rellenas
import os

from functions import load_data, log_interaction_with_dates, generar_comentario, obtener_comentario_experto  # Importar las funciones desde functions.py

# Configura el título de la página y el icono de la pestaña
st.set_page_config(page_title="Gigantes Tecnológicos", page_icon=":chart_with_upwards_trend:")
# Título de la app
st.title('Gigantes Tecnológicos - Predicciones hasta 2030')
st.write("""
         Bienvenido a la aplicación de predicciones de los Gigantes Tecnológicos.
         Selecciona una compañía y visualiza las predicciones de precios de acciones 
         hasta el año 2030, junto con intervalos de confianza.
         """)
# Disclaimer para los usuarios
st.warning("""
    **Disclaimer:** Las predicciones mostradas en esta aplicación están basadas en análisis de datos históricos y modelos de predicción.
    No deben ser interpretadas como consejos financieros o recomendaciones de inversión. 
    Las predicciones son aproximadas y pueden no reflejar resultados futuros reales. 
    Invierta bajo su propio riesgo y consulte a un asesor financiero antes de tomar cualquier decisión.
""")


# Diccionario con las URLs crudas de los CSV
file_paths = {
    'Apple': 'https://raw.githubusercontent.com/cohet3/Technological_giants/main/data/AAPL_forecast.csv',
    'Microsoft': 'https://raw.githubusercontent.com/cohet3/Technological_giants/main/data/MSFT_forecast.csv',
    'Amazon': 'https://raw.githubusercontent.com/cohet3/Technological_giants/main/data/AMZN_forecast.csv',
    'Alphabet': 'https://raw.githubusercontent.com/cohet3/Technological_giants/main/data/GOOGL_forecast.csv',
    'NVIDIA': 'https://raw.githubusercontent.com/cohet3/Technological_giants/main/data/NVDA_forecast.csv'
}

# Selección de la compañía
selected_company = st.selectbox('Selecciona una compañía', list(file_paths.keys()))

# Cargar los datos desde GitHub (usando la URL cruda)
@st.cache_data  # Cachear la función para no volver a cargar los datos innecesariamente
def load_company_data(selected_company):
    return load_data(file_paths[selected_company])

# Cargar el archivo CSV correspondiente
data = load_company_data(selected_company)

# Mostrar los datos
st.write(f'Predicciones de {selected_company}')
st.write(data.head())  # Mostrar las primeras filas del DataFrame con los nuevos nombres de columna


# Crear un gráfico de líneas con bandas de confianza
fig = go.Figure()

# Añadir la línea de la predicción
fig.add_trace(go.Scatter(
    x=data['Fecha'], 
    y=data['Predicción'], 
    mode='lines', 
    name='Predicción'
))

# Añadir las bandas de confianza como áreas rellenas
fig.add_trace(go.Scatter(
    x=data['Fecha'], 
    y=data['Intervalo de Confianza Superior'], 
    fill=None,
    mode='lines',
    line_color='lightgrey',
    name='Intervalo de Confianza Superior'
))

fig.add_trace(go.Scatter(
    x=data['Fecha'], 
    y=data['Intervalo de Confianza Inferior'], 
    fill='tonexty',  # Relleno entre la línea anterior
    mode='lines',
    line_color='lightgrey',
    name='Intervalo de Confianza Inferior'
))

# Configuración del gráfico
fig.update_layout(
    title=f'Predicciones para {selected_company} con Intervalos de Confianza',
    xaxis_title='Fecha',
    yaxis_title='Predicción',
    showlegend=True
)

# Mostrar la gráfica en Streamlit con un key único para evitar conflictos
st.plotly_chart(fig, key=f'{selected_company}_pred_chart')

st.write("""
         Usa los selectores de fecha para filtrar las predicciones dentro de un rango de tiempo específico.
         Esto te permitirá ver cómo evolucionan las predicciones en el tiempo.
         """)
# Filtro por fechas
start_date = st.date_input('Fecha de inicio', value=pd.to_datetime('2023-01-01'))
end_date = st.date_input('Fecha de fin', value=pd.to_datetime('2030-01-01'))

# Filtrar los datos según el rango de fechas seleccionado
filtered_data = data[(data['Fecha'] >= str(start_date)) & (data['Fecha'] <= str(end_date))]

# Crear un gráfico de líneas con bandas de confianza para los datos filtrados
fig_filtered = go.Figure()

# Añadir la línea de la predicción para los datos filtrados
fig_filtered.add_trace(go.Scatter(
    x=filtered_data['Fecha'], 
    y=filtered_data['Predicción'], 
    mode='lines', 
    name='Predicción'
))

# Añadir las bandas de confianza como áreas rellenas para los datos filtrados
fig_filtered.add_trace(go.Scatter(
    x=filtered_data['Fecha'], 
    y=filtered_data['Intervalo de Confianza Superior'], 
    fill=None,
    mode='lines',
    line_color='lightgrey',
    name='Intervalo de Confianza Superior'
))

fig_filtered.add_trace(go.Scatter(
    x=filtered_data['Fecha'], 
    y=filtered_data['Intervalo de Confianza Inferior'], 
    fill='tonexty',  # Relleno entre la línea anterior
    mode='lines',
    line_color='lightgrey',
    name='Intervalo de Confianza Inferior'
))

# Configuración del gráfico filtrado
fig_filtered.update_layout(
    title=f'Predicciones para {selected_company} (Filtrado por Fecha)',
    xaxis_title='Fecha',
    yaxis_title='Predicción',
    showlegend=True
)

# Mostrar el gráfico filtrado en Streamlit
st.plotly_chart(fig_filtered, use_container_width=True, key=f'{selected_company}_filtered_pred_chart')


# Mostrar comentario generado
st.subheader("Comentario del experto:")
#st.write(generar_comentario(filtered_data))
# Mostrar el comentario generado por el "experto" API de pago GPT


st.write(obtener_comentario_experto(filtered_data))



# Diccionario de colores para cada compañía (puedes ajustar los colores)
colors = {
    'Apple': 'blue',
    'Microsoft': 'green',
    'Amazon': 'red',
    'Alphabet': 'purple',
    'NVIDIA': 'orange'
}

# Crear una nueva figura para la comparativa
fig_comparativa = go.Figure()

# Iterar sobre cada compañía y agregar sus datos al gráfico de comparativa
for company, url in file_paths.items():
    # Cargar los datos de la compañía
    data_company = load_data(url)
    
    # Añadir la predicción de cada compañía al gráfico de comparativa
    fig_comparativa.add_trace(go.Scatter(
        x=data_company['Fecha'], 
        y=data_company['Predicción'], 
        mode='lines', 
        name=f'Predicción {company}',
        line=dict(color=colors[company], width=2)
    ))

# Configuración del gráfico de comparativa
fig_comparativa.update_layout(
    title="Comparativa de Predicciones de Gigantes Tecnológicos hasta 2030",
    xaxis_title='Fecha',
    yaxis_title='Predicción de Cierre Ajustado (USD)',
    showlegend=True,
    plot_bgcolor='black',  # Fondo blanco
    paper_bgcolor='black',  # Fondo blanco
    font=dict(family="Arial", size=12),
    legend=dict(
        yanchor="top",
        y=1.02,
        xanchor="left",
        x=0.01
    )
)

# Mostrar el gráfico comparativo en Streamlit
st.plotly_chart(fig_comparativa, use_container_width=True)

# Registrar la interacción del usuario junto con el rango de fechas
log_interaction_with_dates(selected_company, start_date, end_date)



