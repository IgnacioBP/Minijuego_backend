from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Conversation, Actividad, UserProgress
from .serializers import ConversationSerializer, ActividadSerializer




#Obtener conversaciones y actividades del chat
@api_view(['GET'])
def elementos_por_etapa(request, etapa_id):
    conversaciones = Conversation.objects.filter(etapa_id=etapa_id).order_by('orden_salida')
    activities = Actividad.objects.filter(etapa_id=etapa_id).order_by('orden_salida')

    conv_serializer = ConversationSerializer(conversaciones, many=True).data
    acti_serializer = ActividadSerializer(activities, many=True).data


    resultado = []
    actividad_index = 0  

    for mensaje in conv_serializer:
        resultado.append(mensaje)
        if mensaje.get('antes_actividad') and actividad_index < len(acti_serializer):
            resultado.append(acti_serializer[actividad_index])
            actividad_index += 1

    return Response(resultado)

#Obtener una sola  actividad para renerizar
@api_view(['GET'])
def single_activity(request, etapa_id, activity_id):
    try:
        activity = Actividad.objects.get(id=activity_id, etapa_id=etapa_id)
        serializer = ActividadSerializer(activity)
        return Response(serializer.data)
    except Actividad.DoesNotExist:
        return Response({"error": "Actividad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    

#Actualizar informacion de progreso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_progreso(request):
    user = request.user
    etapa_id = request.data.get('etapa_id')
    ultimo_chat = request.data['numero_conversacion_alcanzada']
    ultima_actividad = request.data['numero_actividad_alcanzada']

    print(request.data)
    print("== DATOS RECIBIDOS EN EL BACKEND ==")
    print("Usuario:", user)
    print("Etapa ID:", etapa_id)
    print("Último chat mostrado:", ultimo_chat)
    print("Última actividad completada:", ultima_actividad)

    try:
        progreso = UserProgress.objects.get(usuario=user, etapa_id=etapa_id)
        progreso.numero_conversacion_alcanzada = ultimo_chat
        progreso.numero_actividad_alcanzada = ultima_actividad
        progreso.save()
        
        return Response({'mensaje': 'Progreso actualizado correctamente'})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Obtener progreso de jugador
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_progreso(request):
    user = request.user
    progresos = UserProgress.objects.filter(usuario=user)
    data = {}

    for progreso in progresos:
        data[f"etapa_{progreso.etapa.id}"] = {
            "ultimo_chat_mostrado": progreso.numero_conversacion_alcanzada,
            "ultima_actividad_completada": progreso.numero_actividad_alcanzada
        }

    return Response(data)