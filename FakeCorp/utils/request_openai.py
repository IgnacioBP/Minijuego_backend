from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

key=os.environ.get("OPENAI_API_KEY")

#CREO CLIENTE
client = OpenAI(
    api_key=key
)

#CONVERSION DE NUMEROS A TOPICOS
niveles_conversion = {
    1:"Satira",
    2:"Conexion falsa",
    3:"contenido engañoso",
    4:"Contexto falso",
    5:"Contenido impostor",
    6:"Contenido manipulado",
    7:"Contenido fabricado",
}


#PERSONALIDADES PARA RESPUESTAS (completar personalidades)
personalidades = {
    "Satira":"un hombre Irónico, burlón y exagerado. Ama el absurdo, los juegos de palabras.Tiene un tono juguetón, pero de vez en cuando deja caer verdades importantes." ,
    "Conexion falsa": "una mujer exagerada, persuasiva y encantada de contar cómo manipular con titulares sin decir nada real",
    "contenido engañoso":"Mujer carismática, convincente y elegante. Habla con seguridad y parece confiable, pero enseña a distorsionar la verdad usando solo partes reales" ,
    "Contexto falso":"Tono formal",
    "Contenido impostor":"Tono formal",
    "Contenido manipulado":"Tono formal",
    "Contenido fabricado":"Tono formal"
}


#SETTINGS DEL PROPMT (definicion/rol/ejemplos)
definicion_dificultad = """
Niveles de dificultad:
- fácil: la respuesta es evidente, sin necesidad de conocimientos previos.
- media: se necesita razonamiento básico o haber aprendido algo sobre desinformación.
- difícil: el estudiante debe aplicar juicio crítico y conocimientos más profundos sobre el tipo de desinformación.
"""

# Ejemplos (1 de opción múltiple y 1 de completar oración)
ejemplos = [
    {
        "role": "user",
        "content": "Genera una pregunta de tipo opción múltiple sobre 'Satira o parodia', nivel fácil.La retroalimentacion debe ser dada por un hombre Irónico, burlón y exagerado. Ama el absurdo, los juegos de palabras.Tiene un tono juguetón, pero de vez en cuando deja caer verdades importantes."
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "pregunta": "¿Cuál de los siguientes ejemplos representa una sátira o parodia?",
            "opciones": [
                "Una noticia inventada publicada en un sitio de humor",
                "Una foto antigua usada para representar un evento reciente",
                "Una entrevista manipulada digitalmente",
                "Una cita falsa atribuida a una figura pública"
            ],
            "respuesta_correcta": "Una noticia inventada publicada en un sitio de humor",
            "feedback_acierto": "¡Ah, veo que tienes buen ojo para el humor disfrazado de noticia! La sátira no busca engañar, solo hacerte reír… o pensar. Bien hecho, mente crítica en acción.",
            "feedback_fallo": "¡Uy! Esa no era una sátira, sino un buen intento de engaño. Recuerda: si no te saca una risa o una ceja levantada, probablemente no sea parodia. ¡Vamos, no te dejes confundir por imitaciones baratas!"
        }, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": "Genera una pregunta de tipo completar oración sobre 'Conexion falsa', nivel medio. La retroalimentacion debe ser dada por una mujer exagerada, persuasiva y encantada de contar cómo manipular con titulares sin decir nada real"
    },
    {
        "role": "assistant",
        "content": json.dumps({

            "pregunta": "Completa esta oración con las dos palabras que mejor mantienen el tono de conexión falsa:“Los científicos han descubierto un ___ secreto para lograr una ___ eterna.”",
            "opciones": [
                "método",
                "juventud",
                "desayuno",
                "verdad",
                "secreto",
                "vitamina"
            ],
            "respuesta_correcta": ["secreto", "juventud"],
            "feedback_acierto": "¡Bravísimo! Esa combinación vende como pan caliente. Nadie sabe cuál es el secreto… ¡pero todos quieren clicarlo! ‘Juventud eterna’ es la joya de oro: exagerada, deseada y vacía. ¡Te estás ganando mi respeto clickbaitero!",
            "feedback_fallo": "Hmm… interesante intento, pero le faltó ese toque fabuloso de exageración vacía. Si no promete algo imposible o misterioso, ¿quién va a hacer clic? Recuerda: no informamos… ¡impactamos!"
        }, ensure_ascii=False)
    }
]

# Prompt base
instruccion_sistema = (
    "Eres un asistente experto en generar actividades educativas sobre los 7 tipos de desinformación de Claire Wardle. "
    "Tu tarea es crear preguntas en JSON estructurado. Nunca repitas los ejemplos anteriores. "
    "Debes devolver únicamente el JSON de la actividad generada.\n\n"
    + definicion_dificultad +
    "\nTipos de actividades permitidos:\n- opcion multiple\n- completar la oracion"
)

def get_actividad(categoria,nivel,tipo):

    categoria = niveles_conversion[int(categoria)]

    # Entrada nueva del usuario
    pregunta_nueva = {
        "role": "user",
        "content": f"Genera una pregunta de tipo {tipo} sobre '{categoria}', nivel {nivel}. La retroalimentacion debe ser dada por {personalidades[categoria]}"
    }

    #Obtencion de respeusta
    respuesta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": instruccion_sistema},
            *ejemplos,
            pregunta_nueva
        ],
        temperature= 1.0
    )

    contenido = respuesta.choices[0].message.content.strip()
    actividad_json = None
    try:
        actividad_json = json.loads(contenido)
        print("Respuesta obtenida:")
        print(actividad_json)

    except json.JSONDecodeError:
        print("Error al decodificar el JSON. Contenido recibido:")
        print(contenido)
    
    return actividad_json

def check_json(actividad):
    valid_json = True
    if actividad:
        if ("pregunta" not in actividad): 
            print("No hay campo pregunta en el JSON generado")
            valid_json = False
        if ("opciones" not in actividad): 
            print("No hay campo opciones en el JSON generado")
            valid_json = False
        if ("respuesta_correcta" not in actividad): 
            print("No hay campo de respuesta en el JSON generado")
            valid_json = False
        if ("feedback_acierto" not in actividad): 
            print("No hay feedback de acierto en el JSON generado")
            valid_json = False
        if ("feedback_fallo" not in actividad): 
            print("No hay feedback de fallo en el JSON generado")
            valid_json = False
    else:
        print("Json invalido")
        valid_json = False
    
    return valid_json
