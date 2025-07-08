

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()


api_key=os.environ.get("OPENAI_API_KEY")

#CREO CLIENTE
client = OpenAI(
    api_key=api_key
)

def create_title_evaluation_prompt(news_content, user_title, target_disinformation_type):
    # Diccionario completo de tipos de desinformación
    all_types = {
        1: "Sátira/Parodia (contenido humorístico que puede confundir si se toma en serio)",
        2: "Conexión Falsa (el título no coincide con el contenido real)",
        3: "Contenido Engañoso (mezcla información real con información falsa)",
        4: "Contexto Falso (información real usada en situación o momento equivocado)",
        5: "Contenido Impostor (se hace pasar por algo que no es)",
        6: "Contenido Manipulado (fotos, videos o documentos modificados)",
        7: "Contenido Fabricado (completamente falso, creado desde cero)"
    }
    
    
    prompt = f"""
Actúas como un mentor educativo especializado en enseñar alfabetización digital a adolescentes de 12 a 15 años.

Tu tarea es evaluar el TÍTULO que un estudiante adolescente creó para una noticia desinformativa, considerando:

1. Si el título es apropiado para el contenido de la noticia
2. Si refleja correctamente el tipo de desinformación objetivo que el estudiante está aprendiendo (por ejemplo, parodia, contenido engañoso, etc.)
3. Si demuestra pensamiento crítico y creatividad
4. Otorgar un puntaje entre 0 y 50 puntos
5. Entregar retroalimentación constructiva, clara y motivadora


TIPO DE DESINFORMACIÓN OBJETIVO EN ESTA NOTICIA: {all_types[target_disinformation_type]}

IMPORTANTE: 
- La noticia fue diseñada para contener elementos del tipo {target_disinformation_type}
- El estudiante debe crear un título que simule intencionalmente este tipo de desinformación, como parte de un ejercicio de análisis y comprensión crítica.
- Evalúa si el título logra recrear características propias del tipo de desinformación objetivo (por ejemplo, exageración en parodia, sesgo en contenido engañoso, etc.).

NOTICIA ORIGINAL:
{news_content}

TÍTULO CREADO POR EL ESTUDIANTE:
"{user_title}"

CRITERIOS DE EVALUACIÓN PARA TÍTULOS (50 puntos total):
- Correspondencia con el tipo de desinformación objetivo (15 puntos): ¿El título representa bien el estilo de ese tipo de desinformación?
- Precisión del contenido (15 puntos): ¿El título se basa en el contenido de la noticia, incluso si lo distorsiona intencionalmente para simular desinformación?
- Claridad y comprensión (10 puntos): ¿Es fácil de leer y entender para su audiencia?
- Creatividad y responsabilidad crítica (10 puntos): ¿Demuestra comprensión crítica del fenómeno y creatividad al aplicarlo?

CONSIDERACIONES ESPECIALES PARA ADOLESCENTES:
- Sé más flexible con errores menores de redacción
- Reconoce el esfuerzo y la intención, no solo la perfección
- Valora la creatividad apropiada
- Considera que están aprendiendo a escribir títulos periodísticos

INSTRUCCIONES DE RESPUESTA:
Responde ÚNICAMENTE en formato JSON con la siguiente estructura:

{{
    "puntaje": [número entre 0 y 50],
    "retroalimentacion": {{
        "mensaje_motivador": "[Inicia con algo positivo sobre su título]",
        "lo_que_hiciste_bien": "[Destaca aspectos específicos del título que funcionan]",
        "como_mejorar_titulo": "[Sugiere mejoras específicas para el título]",
        "tip_escritura": "[Consejo práctico para escribir mejores títulos]",
        "ejemplo_mejorado": "[Propón una versión mejorada del título o alternativa]"
    }},
}}

GUÍAS DE COMUNICACIÓN PARA ADOLESCENTES:
- Usa lenguaje cercano y comprensible
- Mantén un tono positivo y constructivo
- Reconoce que están aprendiendo a escribir títulos periodísticos
- Conecta con situaciones que viven diariamente
- Proporciona consejos prácticos para mejorar
- Evita sonar condescendiente
- Celebra la creatividad apropiada

RANGOS DE PUNTAJE ADAPTADOS:
- 0-15: Necesita más apoyo (enfócate en conceptos básicos de titulación)
- 16-30: Buen progreso (refuerza técnicas de escritura)
- 31-40: Muy bien (desafía con títulos más complejos)
- 41-50: Excelente (estudiante avanzado en titulación)

EJEMPLOS DE RETROALIMENTACIÓN POSITIVA:
- "¡Me gusta cómo pensaste en hacer el título claro!"
- "Buen trabajo evitando sensacionalismo..."
- "Tu título captura bien la idea principal..."
- "¡Genial! Estás aprendiendo a ser responsable con la información..."

NOTA IMPORTANTE: Si el título del estudiante perpetúa el tipo de desinformación objetivo, úsalo como oportunidad de aprendizaje, no como falla grave. Explica gentilmente por qué ese enfoque puede ser problemático.
"""
    return prompt





def evaluate_title_response(news_content, user_title, target_disinformation_type):
    prompt = create_title_evaluation_prompt(news_content, user_title, target_disinformation_type)
    print("ENTRADNO AL TRY")
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": f"Eres un mentor educativo amigable especializado en enseñar escritura de títulos periodísticos y alfabetización digital a adolescentes de 12-15 años. Sé constructivo y motivador en tu evaluación."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,  # Slightly higher for more empathetic responses
            max_tokens=1000
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"ESTE ES EL RESULTADO {result}")
        # Añadir información contextual
        result['tipo_objetivo'] = target_disinformation_type
        result['noticia_original'] = news_content[:100] + "..." if len(news_content) > 100 else news_content
        
        return result
        
    except json.JSONDecodeError:
        return {"error": "Error al procesar la respuesta del evaluador"}
    except Exception as e:
        return {"error": f"Error en la evaluación: {str(e)}"}





def check_title_evaluation(evaluacion):
    if not isinstance(evaluacion, dict):
        return False, "La evaluación no es un diccionario válido"
    
    # Claves principales esperadas
    claves_principales = ["puntaje", "retroalimentacion"]
    for clave in claves_principales:
        if clave not in evaluacion:
            return False, f"Falta la clave principal: {clave}"
    
    # Validación de retroalimentacion
    retro = evaluacion["retroalimentacion"]
    if not isinstance(retro, dict):
        return False, "La clave 'retroalimentacion' no es un diccionario"
    
    claves_retro = ["mensaje_motivador", "lo_que_hiciste_bien", "como_mejorar_titulo", "tip_escritura", "ejemplo_mejorado"]
    for clave in claves_retro:
        if clave not in retro:
            return False, f"Falta la clave en retroalimentacion: {clave}"
    
    # Validación del puntaje
    puntaje = evaluacion["puntaje"]
    if not isinstance(puntaje, (int, float)) or puntaje < 0 or puntaje > 50:
        return False
        
    return True, "Estructura válida"


