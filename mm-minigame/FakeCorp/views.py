#from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Actividad
from .serializers import ConversationSerializer, ActividadSerializer



@api_view(['GET'])
def elementos_por_etapa(request, etapa_id):
    conversaciones = Conversation.objects.filter(etapa_id=etapa_id)
    activities = Actividad.objects.filter(etapa_id=etapa_id)

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


@api_view(['GET'])
def single_activity(request, etapa_id, activity_id):
    try:
        activity = Actividad.objects.get(id=activity_id, etapa_id=etapa_id)
        serializer = ActividadSerializer(activity)
        return Response(serializer.data)
    except Actividad.DoesNotExist:
        return Response({"error": "Actividad no encontrada"}, status=status.HTTP_404_NOT_FOUND)