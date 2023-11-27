# Generated by Django 3.2.23 on 2023-11-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PeerLearningAPP', '0009_auto_20231123_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='appealContent',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='isAppealed',
            field=models.IntegerField(null=True, verbose_name='0为无申诉,1为申诉'),
        ),
    ]