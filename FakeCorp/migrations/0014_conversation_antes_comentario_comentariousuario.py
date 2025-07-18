# Generated by Django 4.2.20 on 2025-07-09 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FakeCorp', '0013_alter_respuestadesafio_respuesta_correcta'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='antes_comentario',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ComentarioUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('etapa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FakeCorp.etapa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
