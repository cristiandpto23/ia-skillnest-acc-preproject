import os

import requests
from dotenv import load_dotenv

load_dotenv()

def obtener_datos_gemini(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
    body = {
        "contents": [
            {
                "parts": [{"text": pregunta}]
           
            }
        ]
    }
    
    respuesta = requests.post(url, json=body)
    datos = respuesta.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"]
    
print(obtener_datos_gemini("¿Cuál es la capital de Francia?"))
print(obtener_datos_gemini("¿Qué día es hoy?"))