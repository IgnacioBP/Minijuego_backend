from rest_framework import serializers
from .models import Conversation, Actividad, UserProgress

#Para cargar conversaciones
class ConversationSerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_tipo(self, obj):
        return 'mensaje'

#Para cargar actividades
class ActividadSerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Actividad
        fields = '__all__'

    def get_tipo(self, obj):
        return 'actividad'
    
#Para cargar el progreso
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


#Para actualizar el progreso
