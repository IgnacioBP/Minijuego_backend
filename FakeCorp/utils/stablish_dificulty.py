
from dotenv import load_dotenv
from FakeCorp.models import UserProgress

load_dotenv()


def check_dificulty (id_etapa,usuario,dificultad,acierto):
    nueva_dificultad = dificultad
    
    if acierto:
        if dificultad == "facil":
            nueva_dificultad = "media"
        elif dificultad == "media":
            nueva_dificultad = "dificil"
    else:
        if dificultad == "media":
            nueva_dificultad = "facil"
        elif dificultad == "dificil":
            nueva_dificultad = "media"

    if nueva_dificultad != dificultad:
        try:
            progreso = UserProgress.objects.get(usuario=usuario, etapa_id=id_etapa)
            progreso.dificultad_maxima_alcanzada = nueva_dificultad
            progreso.save()
            print(f"Dificultad actualizada a: {nueva_dificultad}")
        except UserProgress.DoesNotExist:
            print("No se encontró progreso para el usuario y etapa.")
        except Exception as e:
            print(f"Error al actualizar la dificultad: {e}")