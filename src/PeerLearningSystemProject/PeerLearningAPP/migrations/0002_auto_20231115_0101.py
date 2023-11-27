# Generated by Django 3.2.21 on 2023-11-15 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PeerLearningAPP', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answer1',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer2',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer3',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer4',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='content1',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='content2',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='content3',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='content4',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.TextField(null=True, verbose_name='文本回答，不同回答用￥！分隔\r\n'),
        ),
        migrations.AddField(
            model_name='homework',
            name='content',
            field=models.TextField(null=True, verbose_name='作业内容，不同内容用￥！分隔'),
        ),
    ]
