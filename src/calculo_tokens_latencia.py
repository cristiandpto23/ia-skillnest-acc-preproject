import time

from consumir_gemini import armar_peticion, enviar_peticion


def calcular_costo(datos, precio_entrada, precio_salida):
	uso = datos["usageMetadata"]
	tokens_entrada = uso["promptTokenCount"]
	tokens_salida = uso["candidatesTokenCount"]
	return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)

def calcular_latencia(pregunta, modelo, precio_entrada, precio_salida):
    
    latencias = []
    respuesta_json = None
    
    for i in range(4):
        url, body = armar_peticion(pregunta, modelo)
        inicio = time.perf_counter()
        respuesta_json = enviar_peticion(url, body)
        fin = time.perf_counter()
        latencias.append(fin - inicio)
        print(f"Intento {i + 1}: {latencias[-1]:.2f} segundos")
    
    print("-----------------------------")
    print(f"Modelo: {modelo}")
    print("-----------------------------")
    latencia_promedio = sum(latencias) / len(latencias)
    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")
    
    #print(respuesta_json)
    uso = respuesta_json.get("usageMetadata")
    if not uso:
        raise RuntimeError("La respuesta no incluye usageMetadata para calcular el costo.")

    tokens_entrada = uso.get("promptTokenCount", 0)
    tokens_salida = uso.get("candidatesTokenCount", 0)

    costo_total = calcular_costo(respuesta_json, precio_entrada, precio_salida)
    print("-----------------------------")
    print(f"Respuesta: {respuesta_json['candidates'][0]['content']['parts'][0]['text']}")
    print("-----------------------------")
    print(f"Tokens de entrada: {tokens_entrada}")
    print(f"Tokens de salida: {tokens_salida}")
    print(f"Costo de la última petición: {costo_total}")
    print("-----------------------------")
    
    return {
        "modelo": modelo,
        "latencias": latencias,
        "latencia_promedio": latencia_promedio,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": tokens_salida,
        "costo": costo_total,
    }

# gemini-3.8-flash
## costo por entrada: 0.0001 USD por 1,000 tokens 


# calcular_latencia(pregunta, modelo, precio_entrada, precio_salida):
calcular_latencia("Cuál es la capital de Francia?", "gemini-3.8-flash", 0.00000075, 0.00000375)
calcular_latencia("Cuál es la capital de Francia?", "gemini-3.6-flash", 0.00000075, 0.00000375)
calcular_latencia("Cuál es la capital de Francia?", "gemini-3.5-flash-lite", 0.0000003, 0.0000025)