from rest_framework import serializers
from .models import Conversation, Actividad

class ConversationSerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_tipo(self, obj):
        return 'mensaje'


class ActividadSerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Actividad
        fields = '__all__'

    def get_tipo(self, obj):
        return 'actividad'