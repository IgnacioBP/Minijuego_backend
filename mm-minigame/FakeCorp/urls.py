from django.urls import path
from .views import elementos_por_etapa, single_activity

urlpatterns = [
    path('etapas/<int:etapa_id>/conversaciones/', elementos_por_etapa),
    path("etapas/<int:etapa_id>/actividades/<int:activity_id>/", single_activity),
]