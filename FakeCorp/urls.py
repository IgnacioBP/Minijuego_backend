from django.urls import path
from .views import elementos_por_etapa
from .views import actualizar_progreso, obtener_progreso
from .views import generar_actividad_desafio
from .views import register_user
from .views import guardar_respuesta_desafio, obtener_mejor_puntaje, guardar_informacion_desafio, revisar_respuesta_redactada, guardar_comentario

urlpatterns = [
    path('registrar/', register_user),


    path('etapas/<int:etapa_id>/conversaciones/', elementos_por_etapa),
    path('actualizar-progreso/', actualizar_progreso),
    path('obtener-progreso/', obtener_progreso),
    path('generar-pregunta/', generar_actividad_desafio),

    #GUARDAR PREGUNTYAS GENERADAS Y RESPEUSTA DE JUGADOR
    path('guardar-respuesta-desafio/', guardar_respuesta_desafio),
    path('mejor-puntaje/', obtener_mejor_puntaje),
    path('guardar-informacion-desafio/', guardar_informacion_desafio),
    path('revisar_respuesta/',revisar_respuesta_redactada),
    path('guardar-comentario/',guardar_comentario)
]