from django.urls import path
from .views import conversaciones_por_etapa

urlpatterns = [
    path('etapas/<int:etapa_id>/conversaciones/', conversaciones_por_etapa),
]