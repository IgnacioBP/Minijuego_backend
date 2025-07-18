# Generated by Django 4.2.20 on 2025-07-17 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FakeCorp', '0019_rename_respuesta_correcta_challengeanswer_correct_answer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprogress',
            old_name='numero_actividad_alcanzada',
            new_name='activity_number_reached',
        ),
        migrations.RenameField(
            model_name='userprogress',
            old_name='numero_conversacion_alcanzada',
            new_name='chat_number_reached',
        ),
        migrations.RenameField(
            model_name='userprogress',
            old_name='completado',
            new_name='completed',
        ),
        migrations.RenameField(
            model_name='userprogress',
            old_name='dificultad_maxima_alcanzada',
            new_name='max_difficulty_reached',
        ),
        migrations.RenameField(
            model_name='userprogress',
            old_name='etapa',
            new_name='stage',
        ),
        migrations.RenameField(
            model_name='userprogress',
            old_name='usuario',
            new_name='user',
        ),
    ]
