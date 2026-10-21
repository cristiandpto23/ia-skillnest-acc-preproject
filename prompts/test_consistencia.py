import json
import time

from banco import BANCO_DE_PROMPTS
from termcolor import cprint

from consumir_gemini import (
	armar_peticion,
	enviar_peticion,
	extraer_texto,
	parsear_respuesta_json,
)

registro = {}

for prompt in BANCO_DE_PROMPTS:
    exitos = 0
    intentos = 3
    for intento in range(intentos):
        url, body = armar_peticion(
            prompt["ejemplo_usuario"],
            prompt["system_instruction"],
            prompt.get("response_schema"),
        )
        respuesta = enviar_peticion(url, body)
        texto = extraer_texto(respuesta)
        try:
            datos = parsear_respuesta_json(texto)
            if all(clave in datos for clave in prompt["claves_esperadas"]):
                exitos += 1
        except ValueError as error:
            print(f"  intento {intento + 1} falló: {error}")
        time.sleep(1)
    

    
    if exitos == intentos:
        estado = "✅"
    else:
        estado = "⚠️"
        
    print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas {estado}")
    fallos = intentos - exitos
    registro[prompt["nombre"]] = {
        "exitos": exitos,
        "fallos": fallos,
        "intentos": intentos,
    }
    
    cprint(f"Respuesta parseada: {datos}", "yellow", force_color=True)
    cprint("------------------------------", "yellow", force_color=True)


with open("prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
    json.dump(registro, archivo, indent=2, ensure_ascii=False)