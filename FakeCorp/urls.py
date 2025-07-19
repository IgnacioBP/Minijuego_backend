from django.urls import path
from .views import elements_per_stage, update_progress, obtain_progress
from .views import generate_challenge_activity, register_user
from .views import save_challenge_answer, get_best_score, save_challenge_information
from .views import review_written_response, save_comment





urlpatterns = [
    path('registrar/', register_user),


    path('etapas/<int:etapa_id>/conversaciones/', elements_per_stage),
    path('actualizar-progreso/', update_progress),
    path('obtener-progreso/', obtain_progress), #OK
    path('guardar-comentario/',save_comment),

    path('generar-pregunta/', generate_challenge_activity), #OK
    path('guardar-respuesta-desafio/', save_challenge_answer), #OK
    path('mejor-puntaje/', get_best_score), #OK
    path('guardar-informacion-desafio/', save_challenge_information), #OK
    path('revisar_respuesta/',review_written_response), #OK
]