from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from typing import Dict, List, Any
import random

load_dotenv()


api_key=os.environ.get("OPENAI_API_KEY")

#CREO CLIENTE
client = OpenAI(
    api_key=api_key
)


#==================================== DEFINICION DE DATOS ESTATICOS  ====================================


# Definición de los 7 tipos de desinformación de Claire Wardle
tipos_desinformacion = {
    1: "Satira",
    2: "Conexion falsa", 
    3: "contenido engañoso",
    4: "Contexto falso",
    5: "Contenido impostor",
    6: "Contenido manipulado",
    7: "Contenido fabricado"
}

# Personalidades para cada tipo de desinformación
personalidades = {
    "Satira": "un hombre irónico, burlón y exagerado. Ama el absurdo, los juegos de palabras. Tiene un tono juguetón, pero de vez en cuando deja caer verdades importantes.",
    "Conexion falsa": "una mujer exagerada, persuasiva y encantada de contar cómo manipular con titulares sin decir nada real",
    "contenido engañoso": "una mujer carismática, convincente y elegante. Habla con seguridad y parece confiable, pero enseña a distorsionar la verdad usando solo partes reales",
    "Contexto falso": "un profesor académico serio y meticuloso. Habla con autoridad sobre cómo el contexto puede cambiar completamente el significado de información verdadera. Es formal pero apasionado por la precisión histórica",
    "Contenido impostor": "un actor teatral dramático y grandilocuente. Le fascina el arte de la suplantación y habla como si estuviera interpretando diferentes personajes. Es elegante en su manera de explicar cómo engañar con identidades falsas",
    "Contenido manipulado": "un editor de video técnico y perfeccionista. Habla con precisión sobre las herramientas digitales y se enorgullece de explicar cómo alterar contenido manteniendo apariencia de autenticidad. Tono profesional pero con cierto aire de superioridad",
    "Contenido fabricado": "un escritor de ficción creativo y fantasioso. Habla como si estuviera narrando una historia épica. Le emociona crear mundos completamente falsos que parezcan reales. Tono narrativo y envolvente"
}


# Definición de niveles de dificultad
definicion_dificultad = """
Niveles de dificultad:
- fácil: la respuesta es evidente, sin necesidad de conocimientos previos.
- media: se necesita razonamiento básico o haber aprendido algo sobre desinformación.
- difícil: el estudiante debe aplicar juicio crítico y conocimientos más profundos sobre el tipo de desinformación.
"""

# Instrucciones del sistema
instruccion_sistema = (
    "Eres un asistente experto en generar actividades educativas sobre los 7 tipos de desinformación de Claire Wardle. "
    "Tu tarea es crear preguntas en JSON estructurado. Nunca repitas los ejemplos anteriores. "
    "Debes devolver únicamente el JSON de la actividad generada sin explicaciones adicionales.\n\n"
    + definicion_dificultad +
    "\n\nTipos de actividades permitidos:\n- opcion multiple (4 opciones)\n- completar oracion\n\n"
    "IMPORTANTE: El feedback debe reflejar la personalidad asignada de manera consistente y educativa."
)

especificaciones_selecion = """
La pregunta debe:
1. Ser clara y educativa
2. Tener 4 opciones
3. Solo una respuesta correcta
4. Incluir distractores plausibles pero incorrectos
"""

especificaiones_completar = """
La pregunta debe:
1. Tener una oración incompleta con entre uno o dos espacios en blanco
2. La respuesta debe ser una palabra o frase corta clave
3. Ser educativa sobre las características del tipo de desinformación
4. cada opcion deber corresponder a un solo espacio. (si hay dos espacios en blanco, habria que selecionar dos opciones)
"""

#====================================================GENERAR PROMPT ==================================================

def generate_prompt(tipo_pregunta, tipo_desinformacion):
    # Corregir la lógica condicion
    if tipo_pregunta == "opcion_multiple":
        instrucciones = especificaciones_selecion
        estructura_json = """
    {
        "pregunta": "Texto de la pregunta",
        "opciones": [
            "Opción A",
            "Opción B", 
            "Opción C",
            "Opción D"
        ],
        "respuesta_correcta": "Opción A",
        "feedback_acierto": "¡Excelente! Explicación de por qué es correcta...",
        "feedback_fallo": "No es correcto. porque..."
    }"""
    elif tipo_pregunta == "completar_oracion":
        instrucciones = especificaiones_completar
        estructura_json = """
    {
        "pregunta": "Completa esta oración: 'El contenido ___ se caracteriza por...'",
        "opciones": [
            "palabra1",
            "palabra2",
            "palabra3",
            "palabra4"
        ],
        "respuesta_correcta": ["palabra1", "palabra2"],
        "feedback_acierto": "¡Correcto! Explicación de por qué es correcta...",
        "feedback_fallo": "No es correcto. porque..."
    }"""
    else:
        raise ValueError(f"Tipo de pregunta no válido: {tipo_pregunta}")
        
    prompt_base = f"""
Genera una pregunta de {tipo_pregunta} sobre "{tipo_desinformacion}" de la taxonomía de Claire Wardle, sin mencionar a esta.

{instrucciones}

Responde ÚNICAMENTE en formato JSON con esta estructura:{estructura_json}

Taxonomía de referencia:
1. Sátira: Contenido humorístico que puede engañar
2. Conexión falsa: Títulos/imágenes no coinciden con contenido
3. Contenido engañoso: Información falsa para dañar persona/grupo
4. Contexto falso: Contenido genuino compartido con información contextual falsa
5. Contenido impostor: Suplantación de fuentes genuinas
6. Contenido manipulado: Información/imágenes genuinas manipuladas
7. Contenido fabricado: Contenido completamente falso


EJEMPLOS DE PLATAFORMAS/CONTEXTOS PARA USAR:
- Instagram, TikTok, YouTube, Twitter, WhatsApp
- Noticias virales, memes, posts de influencers
- Capturas de pantalla, videos, audios
- Grupos de WhatsApp, historias de Instagram

"""
    
    return prompt_base.strip()






def obtener_actividad(categoria_especifica, nivel, tipo_pregunta):
    tipo_desinformacion = tipos_desinformacion[categoria_especifica]
    personalidad = personalidades[tipo_desinformacion]
    
    # Usar la nueva función generate_prompt
    prompt_base = generate_prompt(tipo_pregunta, tipo_desinformacion)
    
    # Añadir información sobre nivel y personalidad
    prompt_completo = f"""{prompt_base}

Nivel de dificultad: {nivel}
Personalidad para el feedback: {personalidad}

Asegúrate de que el feedback refleje esta personalidad de manera consistente y educativa.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": instruccion_sistema},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=1.0,
            seed=random.randint(1, 100000),
            max_tokens=1000
        )
        
        contenido = response.choices[0].message.content.strip()
        
        # Limpiar el contenido si tiene formato markdown
        if contenido.startswith("```json"):
            contenido = contenido.replace("```json", "").replace("```", "").strip()
        
        # Parsear la respuesta JSON
        respuesta_json = json.loads(contenido)
        print(respuesta_json)

        return respuesta_json
        
    except json.JSONDecodeError as e:
        return {"error": f"Error al decodificar JSON: {str(e)}", "contenido_recibido": contenido}
    except Exception as e:
        return {"error": f"Error al generar pregunta: {str(e)}"}




def check_json(actividad):

    #En caso de que no se guarde bien... o mejor dicho que no se guarde
    if not actividad:
        print("JSON inválido o vacío")
        return False
    
    #Error al requerir
    if "error" in actividad:
        print(f"Error en la actividad: {actividad['error']}")
        return False
    
    campos_requeridos = ["pregunta", "opciones", "respuesta_correcta", "feedback_acierto", "feedback_fallo"]
    campos_faltantes = []

    #Caso campos faltantes
    for campo in campos_requeridos:
        if campo not in actividad:
            campos_faltantes.append(campo)
    
    if campos_faltantes:
        print(f"Campos faltantes: {campos_faltantes}")
        return False

    
    print("✅ JSON válido - Todos los campos requeridos están presentes")
    return True   




