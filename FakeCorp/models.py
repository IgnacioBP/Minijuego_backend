from django.db import models
from django.contrib.auth.models import User


class Etapa(models.Model):
    habilidad = models.CharField(max_length=100)

    def __str__(self):
        return f"Etapa {self.id} - {self.habilidad}"


class UserProgress(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    #Subtemaa asociado (satira,contenido engañoso, etc)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)

    #Atributos relacionados a los chats
    numero_conversacion_alcanzada = models.IntegerField(default = 0)
    numero_actividad_alcanzada = models.IntegerField(default = 0)
    completado = models.BooleanField(default= False)
    
    #Atributo relacionado al desafio
    DIFICULTAD_CHOICES = [
        ("facil", "Fácil"),
        ("media", "Media"),
        ("dificil", "Difícil"),
    ]

    dificulad_maxima_alcanzada = models.CharField(
        max_length=10,
        choices=DIFICULTAD_CHOICES,
        default="media"
    )

    def __str__(self):
        return f"{self.usuario.username} en {self.etapa}"


class Conversation(models.Model):
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    orden_salida = models.IntegerField()
    contenido = models.TextField()
    antes_actividad = models.BooleanField(default=False)
    final = models.BooleanField(default=False) 

    def __str__(self):
        return f"Conversación {self.id} (Etapa {self.etapa.id})"


class Actividad(models.Model):
    TIPOS = [
        ('seleccion_multiple', 'Selección Múltiple'),
    ]

    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    orden_salida = models.IntegerField()
    enunciado = models.TextField()
    respuesta = models.TextField()
    contenido = models.JSONField()

    comentario_correcto = models.TextField(default= "Buen trabajo, ¡respuesta correcta!")
    comentario_incorrecto = models.TextField(default= "Respuesta incorrecta, pero tranquilo, eso solo significa que aun puedes aprender.")


    def __str__(self):
        return f"Actividad {self.id} - {self.tipo}"


class UserAnswer(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, null=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    respuesta = models.TextField()
    buena = models.BooleanField()

    def __str__(self):
        return f"Respuesta de {self.usuario.username} a actividad {self.actividad.id}"
