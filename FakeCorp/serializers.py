from rest_framework import serializers
from .models import Conversation, Activity, UserProgress, ChallengeAnswer
from .models import ChallengeRecord

#Para cargar conversaciones
class ConversationSerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_tipo(self, obj):
        return 'mensaje'

#Para cargar actividades
class ActivitySerializer(serializers.ModelSerializer):
    tipo_general = serializers.SerializerMethodField("get_tipo")

    class Meta:
        model = Activity
        fields = '__all__'

    def get_tipo(self, obj):
        return 'actividad'
    
#Para cargar el progreso
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


#Para guardar informacion de las preguntas generadas t respondidas
class ChallengeAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeAnswer
        fields = '__all__'

#Para guardar informacion  general del desafio
class ChallengeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeRecord
        fields = '__all__'