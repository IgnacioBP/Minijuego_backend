# Generated by Django 4.2.20 on 2025-04-20 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("FakeCorp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="actividad",
            name="comentario_correcto",
            field=models.TextField(default="Buen trabajo, ¡respuesta correcta!"),
        ),
        migrations.AddField(
            model_name="actividad",
            name="comentario_incorrecto",
            field=models.TextField(
                default="Respuesta incorrecta, pero tranquilo, eso solo significa que aun puedes aprender."
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="etapa",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="FakeCorp.etapa",
            ),
        ),
        migrations.AddField(
            model_name="userprogress",
            name="numero_actividad_alcanzada",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userprogress",
            name="numero_conversacion_alcanzada",
            field=models.IntegerField(default=0),
        ),
    ]
