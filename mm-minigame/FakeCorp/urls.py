from django.urls import path
from .views import elementos_por_etapa, single_activity
from .views import actualizar_progreso, obtener_progreso

urlpatterns = [
    path('etapas/<int:etapa_id>/conversaciones/', elementos_por_etapa),
    path("etapas/<int:etapa_id>/actividades/<int:activity_id>/", single_activity),
    path('actualizar-progreso/', actualizar_progreso),
    path('obtener-progreso/', obtener_progreso),
]