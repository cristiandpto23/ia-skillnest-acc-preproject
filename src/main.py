import consumir_gemini

# ValueError: La pregunta no puede estar vacía.
# print(consumir_gemini.obtener_dato_de_prueba(" "))

print(consumir_gemini.obtener_dato_de_prueba("¿Cuál es la capital de Francia?"))
print(consumir_gemini.obtener_dato_de_prueba("¿Cuántos dientes tiene un adulto?"))

"""
RuntimeError: La respuesta no trae el texto generado en el lugar esperado.
print(consumir_gemini.extraer_texto({}))
"""