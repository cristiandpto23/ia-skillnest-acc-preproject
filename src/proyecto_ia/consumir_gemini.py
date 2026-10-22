import json
import os
import re

import requests
from dotenv import load_dotenv
from termcolor import cprint

load_dotenv()

SYSTEM_INSTRUCTION_DEFAULT = (
    "Responde únicamente con un objeto JSON válido, sin texto adicional "
    "y sin usar bloques de markdown. El JSON debe tener exactamente estas "
    "claves: 'categoria' (string), 'confianza' (número entre 0 y 1), 'respuesta' (string). "
    "respuesta: (string) en solo 1 a 5 palabras, sin saltos de línea ni comillas dobles."
)

response_schema = {
    "type": "OBJECT",
    "properties": {
        "categoria": { "type": "STRING" },
        "confianza": { "type": "NUMBER" },
        "respuesta": { "type": "STRING" }
    },
    "required": ["categoria", "confianza"]
}

def armar_peticion(pregunta: str, system_instruction: str| None = None, response_schema=None):
    if system_instruction is None:
        system_instruction = SYSTEM_INSTRUCTION_DEFAULT
    
    pregunta = pregunta.strip()
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
    body = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"parts": [{"text": pregunta}]}]
    }
    
    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
     
    return url, body

def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servvicio. Intenta de nuevo en unos segundos.")

    try:
        return respuesta.json()    
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no trae el texto generado en el lugar esperado.")

def parsear_respuesta_json(texto):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
 
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("El texto no es un JSON válido.")

    """
    if "categoria" not in datos or "confianza" not in datos:
        raise ValueError("El JSON no contiene las claves requeridas 'categoria' y 'confianza'.")
    """

    return datos
 
def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.0000003, 0.0000025)
    cprint(f"Costo: ${costo:.8f}", "green", force_color=True)
    texto = extraer_texto(datos)
    return parsear_respuesta_json(texto)


def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos.get("usageMetadata", {})
    tokens_entrada = uso.get("promptTokenCount", 0)
    tokens_salida = uso.get("candidatesTokenCount", 0)
    return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)