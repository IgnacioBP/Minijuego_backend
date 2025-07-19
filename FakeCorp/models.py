from django.db import models
from django.contrib.auth.models import User


class Stage(models.Model):  #MODIFICACION LISTA
    desinformation_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Etapa {self.id} - {self.desinformation_name}"


class UserProgress(models.Model): #MODIFICACION LISTA
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Subtemaa asociado (satira,contenido engañoso, etc)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    # Atributos relacionados a los chats
    chat_number_reached = models.IntegerField(default = 0)
    activity_number_reached = models.IntegerField(default = 0)
    completed = models.BooleanField(default= False)
    
    # Atributo relacionado al desafio
    DIFFICULTY_CHOICES = [
        ("facil", "Fácil"),
        ("media", "Media"),
        ("dificil", "Difícil"),
    ]

    max_difficulty_reached = models.CharField(
        max_length = 10,
        choices = DIFFICULTY_CHOICES,
        default = "media"
    )

    def __str__(self):
        return f"{self.user.username} en {self.stage}"


class Conversation(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    output_order = models.IntegerField()
    content = models.TextField()
    before_activity = models.BooleanField(default=False)
    before_comment = models.BooleanField(default=False)
    end = models.BooleanField(default=False) 

    def __str__(self):
        return f"Conversación {self.id} (Etapa {self.stage.id})"


class Activity(models.Model):

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    mode = models.CharField(max_length=50)
    output_order = models.IntegerField()
    statement = models.TextField()
    answer = models.TextField()
    content = models.JSONField()

    correct_feedback  = models.TextField(default= "Buen trabajo, ¡respuesta correcta!")
    incorrect_feedback  = models.TextField(default= "Respuesta incorrecta, pero tranquilo, eso solo significa que aun puedes aprender.")


    def __str__(self):
        return f"Actividad {self.id} - {self.mode}"


class UserAnswer(models.Model): #MODIFICACION LISTA
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField()

    def __str__(self):
        return f"Respuesta de {self.user.username} a actividad {self.activity.id}"


class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    comment = models.TextField()

#==========RELACIONADOS A LOS DESAFIOS========== 

class ChallengeAnswer(models.Model): #MODIFICACION LISTA
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    topic  = models.TextField()
    difficulty  = models.CharField(max_length=10)

    question  = models.TextField()
    options = models.JSONField()
    correct_answer  = models.JSONField(null=True)
    player_answer  = models.JSONField()
    is_correct  = models.BooleanField()
    image = models.TextField(default= None, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    score  = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.dificultad} - {'✔' if self.es_correcta else '✘'}"


class ChallengeRecord(models.Model): #MODIFICACION LISTA
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Datos de interacion
    total_score = models.IntegerField()   # preguntas + bono de tiempo

    ##de las preguntas
    question_score  = models.IntegerField()  #solo preguntas(valor obtenido)
    max_score  = models.IntegerField()     #solo preguntas(valor si buenas)
    bonus_score = models.IntegerField()     #solo bono tiempo
    
    #Datos temporales de la pregunta (temporal de teimpo, no de corta duracion)
    start_time  = models.DateTimeField()
    end_time  = models.DateTimeField()
    total_duration = models.DurationField()

    #Diccionarios con dificultades y numero de tema
    initial_difficulties  = models.JSONField() 
    final_difficulties  = models.JSONField()

    timestamp = models.DateTimeField(auto_now_add=True)
    




