# functions.py
import pandas as pd
import os
import openai
import random
import streamlit as st

# Función para cargar los datos CSV
def load_data(url):
    data = pd.read_csv(url)
    # Renombrar las columnas para que sean más descriptivas
    data = data.rename(columns={
        'ds': 'Fecha',
        'yhat': 'Predicción',
        'yhat_lower': 'Intervalo de Confianza Inferior',
        'yhat_upper': 'Intervalo de Confianza Superior'
    })
    return data

# Función para registrar las interacciones del usuario
def log_interaction_with_dates(selected_company, start_date, end_date):
    interaction_data = {
        'company': selected_company,
        'start_date': start_date,
        'end_date': end_date,
        'timestamp': pd.Timestamp.now()
    }

    # Verificar si el archivo ya existe
    file_exists = os.path.isfile('interactions.csv')

    # Guardar la interacción en un CSV
    interaction_df = pd.DataFrame([interaction_data])
    interaction_df.to_csv('interactions.csv', mode='a', header=not file_exists, index=False)

# Diccionario de consejos financieros predefinidos
consejos_financieros = {
    "crecimiento": [
        "El mercado parece estar en una tendencia alcista. Puede ser un buen momento para considerar mantener o aumentar posiciones en esta empresa.",
        "Las predicciones muestran un crecimiento sostenido, lo cual es una señal positiva para los inversores a largo plazo.",
        "Con esta tendencia alcista, podrías considerar aprovechar oportunidades de crecimiento, pero ten en cuenta la volatilidad del mercado.",
        "Este crecimiento proyectado podría ser una oportunidad para diversificar tu portafolio manteniendo una parte importante en esta empresa.",
        "Dado que la tendencia es positiva, asegúrate de monitorear los resultados trimestrales para asegurar que se mantenga el crecimiento.",
        "Es probable que la empresa continúe en una trayectoria de crecimiento, lo que podría ser una buena oportunidad para aumentar posiciones gradualmente.",
        "La tendencia muestra un aumento continuo, pero siempre es prudente tener una estrategia de salida clara en caso de correcciones inesperadas."
    ],
    "caida": [
        "La predicción indica una caída general. Puede ser un buen momento para revisar tu estrategia de inversión y considerar opciones más seguras.",
        "Con una tendencia a la baja, es recomendable tener precaución antes de realizar nuevas inversiones en esta compañía.",
        "En tiempos de caídas, puede ser prudente diversificar en sectores más estables o buscar activos defensivos."
    ],
    "estable": [
        "Las predicciones no muestran grandes cambios. Este podría ser un buen momento para mantener posiciones y evitar movimientos bruscos.",
        "La estabilidad en las predicciones sugiere que podrías mantener tu inversión y observar cómo se desarrollan las tendencias.",
        "Dado que no hay grandes movimientos previstos, quizás sea prudente mantener posiciones o esperar a una mayor claridad en el mercado."
    ]
}

# Función para generar un comentario basado en la tendencia


def generar_comentario(data):
    tendencia = data['Predicción'].pct_change().mean()
    if tendencia > 0:
        comentario = random.choice(consejos_financieros["crecimiento"])
        return f"La predicción muestra una tendencia de crecimiento general. {comentario}"
    elif tendencia < 0:
        comentario = random.choice(consejos_financieros["caida"])
        return f"La predicción indica una caída general en el futuro. {comentario}"
    else:
        comentario = random.choice(consejos_financieros["estable"])
        return f"No se observa un cambio significativo en las predicciones. {comentario}"




# Configurar la API Key correctamente
openai.api_key = st.secrets["openai"]["api_key"]
# Función para obtener el comentario del "experto"
def obtener_comentario_experto(data):
    tendencia = data['Predicción'].pct_change().mean()

    # Crear el prompt
    prompt = f"La predicción para la empresa muestra una tendencia de {'crecimiento' if tendencia > 0 else 'caída' if tendencia < 0 else 'estabilidad'}. Dame un consejo financiero con base en esta tendencia."

    # Usar el cliente con la nueva API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Asegúrate de usar el modelo adecuado
        messages=[
            {"role": "system", "content": "Eres un asesor financiero experto."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extraer y devolver la respuesta
    return response.choices[0].message['content']



