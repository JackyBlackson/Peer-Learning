# Generated by Django 3.2.21 on 2023-11-07 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answerId', models.IntegerField(default=-1, primary_key=True, serialize=False)),
                ('answer1', models.CharField(max_length=255, null=True, verbose_name='文本回答\r\n')),
                ('answer2', models.CharField(max_length=255, null=True, verbose_name='文本回答\r\n')),
                ('answer3', models.CharField(max_length=255, null=True, verbose_name='文本回答\r\n')),
                ('answer4', models.CharField(max_length=255, null=True, verbose_name='文本回答\r\n')),
                ('finalScore', models.IntegerField(default=-1, null=True)),
                ('whetherAssigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseId', models.IntegerField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.IntegerField(primary_key=True, serialize=False)),
                ('roleType', models.IntegerField(null=True)),
                ('userName', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('class_field', models.IntegerField(db_column='class', default=-1, null=True)),
                ('userFace', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('token', models.CharField(default='NULL_NOT_LOGIN', max_length=64, null=True)),
                ('assignedHomeworkCount', models.IntegerField(default=0, verbose_name='分配作业数量')),
                ('performanceWeight', models.FloatField(default=0, verbose_name='学生历史获得成绩高,获得高权重')),
                ('engagementWeight', models.FloatField(default=0, verbose_name='学生分配任务参与度高,获得高权重')),
                ('rightnessWeight', models.FloatField(default=0, verbose_name='学生历史打分高,权重高,用于衡量学生倾向于打什么分数段的分数')),
            ],
        ),
        migrations.CreateModel(
            name='Teaching',
            fields=[
                ('teachingId', models.AutoField(primary_key=True, serialize=False)),
                ('courseId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.course')),
                ('teacherId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.user')),
            ],
        ),
        migrations.CreateModel(
            name='Selecting',
            fields=[
                ('selectingId', models.IntegerField(primary_key=True, serialize=False)),
                ('studentId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.user')),
                ('teachingId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.teaching')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('homeworkId', models.IntegerField(primary_key=True, serialize=False)),
                ('content1', models.CharField(max_length=255, null=True)),
                ('content2', models.CharField(max_length=255, null=True)),
                ('content3', models.CharField(max_length=255, null=True)),
                ('content4', models.CharField(max_length=255, null=True)),
                ('courseId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.course')),
                ('teacherId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.user')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('similarity', models.IntegerField(null=True, verbose_name='相似度 0到100\r\n')),
                ('checkId', models.AutoField(primary_key=True, serialize=False)),
                ('answerId1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='checks_related_to_answer1', to='PeerLearningAPP.answer', verbose_name='被检查的两份作业\r\n')),
                ('answerId2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='checks_related_to_answer2', to='PeerLearningAPP.answer')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignmentId', models.AutoField(primary_key=True, serialize=False)),
                ('startTime', models.DateField(null=True)),
                ('endTime', models.DateField(null=True)),
                ('isFinished', models.IntegerField(null=True, verbose_name='0位完成,1完成')),
                ('comments', models.CharField(max_length=255, null=True)),
                ('grade', models.CharField(max_length=255, null=True)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='assignment', to='PeerLearningAPP.answer', verbose_name='要完成批阅的作业id\r\n')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='student_assignments', to='PeerLearningAPP.user', verbose_name='指定某个学生完成\r\n')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='teacher_assignments', to='PeerLearningAPP.user', verbose_name='发起者(某个教师)')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='homeworkId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.homework'),
        ),
        migrations.AddField(
            model_name='answer',
            name='studentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='PeerLearningAPP.user'),
        ),
    ]
