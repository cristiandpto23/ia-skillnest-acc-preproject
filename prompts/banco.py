BANCO_DE_PROMPTS = [
	{
    	"nombre": "clasificar_sentimiento",
    	"system_instruction": (
        	"Responde únicamente con un JSON con las claves 'sentimiento' "
        	"('positivo', 'negativo' o 'neutro') y 'confianza' (0 a 1)."
    	),
    	"ejemplo_usuario": "El servicio llegó tarde pero el producto está perfecto.",
    	"claves_esperadas": ["sentimiento", "confianza"],
    	"response_schema": {
        	"type": "OBJECT",
        	"properties": {
            	"sentimiento": { "type": "STRING" },
            	"confianza": { "type": "NUMBER" }
        	},
        	"required": ["sentimiento", "confianza"]
    	},
	},
    {
        "nombre": "extraer_evento",
        "system_instruction": (
            "Extrae el evento y su fecha. "
            "Responde únicamente con un JSON con 'evento' (string) y 'fecha' (string). "
            "Si no aparece una fecha, usa una cadena vacía."
        ),
        "ejemplo_usuario": "El concierto es el 15 de octubre en el estadio.",
        "claves_esperadas": ["evento", "fecha"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "evento": { "type": "STRING" },
                "fecha": { "type": "STRING" }
            },
            "required": ["evento", "fecha"]
        }
    },
    {
        "nombre": "clasificar_consulta",
        "system_instruction": (
            "Clasifica la consulta como 'devolución', 'envío' u 'otro'. "
            "Responde únicamente con un JSON con 'categoría' (string) y 'requiere_acción' (boolean)." 
        ),
        "ejemplo_usuario": "Quiero saber cuándo llegará el paquete que compré ayer.",
        "claves_esperadas": ["categoría", "requiere_acción"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoría": { "type": "STRING" },
                "requiere_acción": { "type": "BOOLEAN" }
            },
            "required": ["categoría", "requiere_acción"]
        }
    }
    ]