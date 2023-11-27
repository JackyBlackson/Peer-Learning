# Generated by Django 3.2.23 on 2023-11-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PeerLearningAPP', '0008_rename_homworkdes_homework_homeworkdes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='gptSim',
            field=models.FloatField(default=0, null=True, verbose_name='与GPT文本的相似度'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='otherSim',
            field=models.FloatField(default=0, null=True, verbose_name='与其他答案的相似度'),
        ),
    ]