# Generated by Django 3.2.21 on 2023-11-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PeerLearningAPP', '0006_homework_homworkdes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='endTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='startTime',
            field=models.DateTimeField(null=True),
        ),
    ]