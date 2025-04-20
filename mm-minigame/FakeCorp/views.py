from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Conversation
from .serializers import ConversationSerializer

@api_view(['GET'])
def conversaciones_por_etapa(request, etapa_id):
    conversaciones = Conversation.objects.filter(etapa_id=etapa_id).order_by('orden_salida')
    serializer = ConversationSerializer(conversaciones, many=True)
    return Response(serializer.data)
