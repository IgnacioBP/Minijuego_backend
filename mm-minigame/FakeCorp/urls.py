from django.urls import path
from .views import elementos_por_etapa, single_activity
from .views import actualizar_progreso, obtener_progreso
from .views import generar_actividad_desafio
from .views import register_user

urlpatterns = [
    path('registrar/', register_user),


    path('etapas/<int:etapa_id>/conversaciones/', elementos_por_etapa),
    path("etapas/<int:etapa_id>/actividades/<int:activity_id>/", single_activity),
    path('actualizar-progreso/', actualizar_progreso),
    path('obtener-progreso/', obtener_progreso),
    path('generar-pregunta/', generar_actividad_desafio)
]