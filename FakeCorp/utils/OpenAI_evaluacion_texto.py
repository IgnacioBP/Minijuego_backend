from openai import OpenAI
from dotenv import load_dotenv
import os
import random 

load_dotenv()

api_key=os.environ.get("OPENAI_API_KEY")

#CREO CLIENTE
client = OpenAI(
    api_key=api_key
)


def generate_news_for_title(tipo_desinformacion, dificultad):
    # Tipos de desinformación según Claire Wardle
    tipos_info = {
        1: {
            "nombre": "Sátira/Parodia",
            "descripcion": "Contenido humorístico que puede confundir si se toma en serio",
            "ejemplo": "Artículos de sitios como 'El Deforma' o memes exagerados"
        },
        2: {
            "nombre": "Conexión Falsa",
            "descripcion": "Cuando el título no coincide con el contenido real",
            "ejemplo": "Titular alarmante sobre una noticia que dice algo diferente"
        },
        3: {
            "nombre": "Contenido Engañoso",
            "descripcion": "Mezcla información real con información falsa de forma sutil",
            "ejemplo": "Estadísticas reales usadas para conclusiones incorrectas"
        },
        4: {
            "nombre": "Contexto Falso",
            "descripcion": "Información real compartida en situación o momento equivocado",
            "ejemplo": "Foto real de un evento pasado presentada como actual"
        },
        5: {
            "nombre": "Contenido Impostor",
            "descripcion": "Se hace pasar por fuente confiable cuando no lo es",
            "ejemplo": "Cuenta falsa que imita a un medio reconocido"
        },
        6: {
            "nombre": "Contenido Manipulado",
            "descripcion": "Fotos, videos o documentos que han sido modificados",
            "ejemplo": "Imágenes editadas o videos deepfake"
        },
        7: {
            "nombre": "Contenido Fabricado",
            "descripcion": "Completamente falso, creado desde cero para engañar",
            "ejemplo": "Noticias inventadas que parecen reales"
        }
    }

    # Especificaciones por dificultad
    dificultades_specs = {
        "facil": {
            "descripcion": "Señales muy evidentes de desinformación",
            "contexto": "Situaciones claras y obvias",
            "complejidad": "Un solo elemento problemático muy visible"
        },
        "media": {
            "descripcion": "Requiere análisis básico para identificar el problema",
            "contexto": "Situaciones que necesitan cierta reflexión",
            "complejidad": "Dos elementos que deben ser considerados"
        },
        "dificil": {
            "descripcion": "Necesita pensamiento crítico y conocimientos más profundos",
            "contexto": "Situaciones complejas con múltiples factores",
            "complejidad": "Varios elementos sutiles que interactúan entre sí"
        }
    }

    prompt = f"""
Eres un generador de contenido educativo especializado en alfabetización mediática para niños y niñas de 10 a 12 años. 

Tu tarea es crear UNA NOTICIA CORTA SIN TÍTULO, que simule un caso realista de desinformación según el tipo indicado.

TIPO DE DESINFORMACIÓN A INCLUIR:
- Tipo {tipo_desinformacion}: {tipos_info[tipo_desinformacion]["nombre"]}
- Definición (solo como referencia interna): {tipos_info[tipo_desinformacion]["descripcion"]}
- Ejemplo típico (solo como guía para ti): {tipos_info[tipo_desinformacion]["ejemplo"]}

NIVEL DE DIFICULTAD: {dificultad.upper()}
- Características: {dificultades_specs[dificultad]["descripcion"]}
- Contexto: {dificultades_specs[dificultad]["contexto"]}
- Complejidad: {dificultades_specs[dificultad]["complejidad"]}


INSTRUCCIONES ESPECÍFICAS:
1. NO incluyas título, explicaciones ni contexto externo.
2. NO expliques que el texto es desinformación ni cómo detectarla o evitarla.
3. Escribe solo el CUERPO de una noticia breve que simule este tipo de desinformación.
4. El contenido debe contener elementos del tipo de desinformación indicado, de forma evidente (en nivel fácil) o sutil (en nivel difícil).
5. Usa temas cercanos a adolescentes: tecnología, redes sociales, videojuegos, deportes, entretenimiento, vida escolar, influencers, etc.
6. El texto debe estar escrito en lenguaje simple y apropiado para lectores de 10 a 12 años.
7. La noticia debe ser lo suficientemente rica como para que un estudiante pueda crear un título que refleje el tipo de desinformación.

CONTEXTO SUGERIDO:
- Noticias virales en redes sociales (Instagram, TikTok, YouTube)
- Influencers o celebridades
- Videojuegos y tecnología
- Deportes o espectáculos
- Eventos escolares o juveniles

IMPORTANTE:
- No debes aclarar en ningún momento que se trata de desinformación.
- No incluyas ningún análisis ni moraleja.
- El texto debe simular una noticia real desde el punto de vista de un lector ingenuo.
- Ajusta el nivel de sutileza según la dificultad seleccionada.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en educación digital que crea noticias específicas para ejercicios de titulación. Siempre respondes solo con el cuerpo de la noticia, sin título ni texto adicional."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            seed=random.randint(1, 100000),
            max_tokens=800,
        )

        news_content = response.choices[0].message.content.strip()
        # Limpiar cualquier formato extra
        news_content = news_content.replace('"', '').strip()
        
        # Remover cualquier título que haya podido generar
        lines = news_content.split('\n')
        # Si la primera línea parece un título (corta y sin punto final), la removemos
        if lines and len(lines[0]) < 100 and not lines[0].endswith('.'):
            news_content = '\n'.join(lines[1:]).strip()
        
        return news_content
        
    except Exception as e:
        return f"Error al generar la noticia: {str(e)}"







    # news_content = generate_news_for_title(
    #     tipo_desinformacion=tipo_desinformacion,  
    #     dificultad=dificultad
    # )
    

