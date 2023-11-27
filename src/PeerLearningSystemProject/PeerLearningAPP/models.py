from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
  userId = models.IntegerField(primary_key=True)
  roleType = models.IntegerField(null=True)
  userName = models.CharField(max_length=255, null=True)
  password = models.CharField(max_length=255, null=True)
  class_field = models.IntegerField(default=-1, db_column='class', null=True)
  userFace = models.CharField(max_length=255, null=True)
  email = models.CharField(max_length=255, null=True)
  token = models.CharField(max_length=64, null=True, default="NULL_NOT_LOGIN")
  assignedHomeworkCount = models.IntegerField(default=0, verbose_name='分配作业数量')
  performanceWeight = models.FloatField(default=0,verbose_name='学生历史获得成绩高,获得高权重')
  engagementWeight = models.FloatField(default=0,verbose_name='学生分配任务参与度高,获得高权重')
  rightnessWeight = models.FloatField(default=0,verbose_name='学生历史打分高,权重高,用于衡量学生倾向于打什么分数段的分数')

class Course(models.Model):
  courseId = models.IntegerField(primary_key=True)
  courseName = models.CharField(max_length=255, null=True)

class Teaching(models.Model):
  teachingId = models.AutoField(primary_key=True)
  teacherId = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
  courseId = models.ForeignKey(Course, on_delete=models.RESTRICT, null=True)

class Answer(models.Model):
    answerId = models.IntegerField(primary_key=True, default=-1)
    homeworkId = models.ForeignKey('Homework', on_delete=models.RESTRICT, null=True)
    answer = models.TextField(null=True, verbose_name='文本回答，不同回答用￥！分隔\r\n')
    studentId = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    finalScore = models.CharField(max_length=255, null=True)
    whetherAssigned = models.BooleanField(default=False)
    otherSim = models.FloatField(null=True, verbose_name='与其他答案的相似度', default=0)
    gptSim = models.FloatField(null=True, verbose_name='与GPT文本的相似度', default=0)


class Homework(models.Model):
    teacherId = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
    homeworkId = models.IntegerField(primary_key=True)
    standAns = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True, verbose_name='作业内容，不同内容用￥！分隔')
    courseId = models.ForeignKey('Course', on_delete=models.RESTRICT, null=True)
    startTime = models.DateTimeField(null=True)  # 改为 DateTimeField
    endTime = models.DateTimeField(null=True)
    homeworkDes =  models.CharField(max_length=255, null=True)
  
  
class Assignment(models.Model):
  assignmentId = models.AutoField(primary_key=True)
  isFinished = models.IntegerField(null=True, verbose_name='0位完成,1完成')
  student = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='student_assignments', verbose_name='指定某个学生完成\r\n')
  answer = models.ForeignKey(Answer, on_delete=models.RESTRICT, null=True, related_name='assignment', verbose_name='要完成批阅的作业id\r\n')
  teacher = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='teacher_assignments', verbose_name='发起者(某个教师)')
  comments = models.CharField(max_length=255, null=True)
  grade = models.CharField(max_length=255, null=True)
  isAppealed = models.IntegerField(null=True, verbose_name='0为无申诉,1为申诉')
  appealContent = models.CharField(max_length=255, null=True)



class Check(models.Model):
    similarity = models.IntegerField(null=True, verbose_name='相似度 0到100\r\n')
    answerId1 = models.ForeignKey(
        Answer, 
        on_delete=models.RESTRICT, 
        null=True, 
        verbose_name='被检查的两份作业\r\n', 
        related_name='checks_related_to_answer1'
    )
    answerId2 = models.ForeignKey(
        Answer, 
        on_delete=models.RESTRICT, 
        null=True, 
        related_name='checks_related_to_answer2'
    )
    checkId = models.AutoField(primary_key=True)

class Selecting(models.Model):
  selectingId = models.IntegerField(primary_key=True)
  studentId = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
  teachingId = models.ForeignKey(Teaching, on_delete=models.RESTRICT, null=True)

