# Generated by Django 4.2.20 on 2025-06-09 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeCorp', '0004_userprogress_completado'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='final',
            field=models.BooleanField(default=False),
        ),
    ]
