from django.test import TestCase
from django.utils import timezone
import json
from PeerLearningAPP.models import User, Teaching, Course, Selecting, Answer, Assignment,Homework
from PeerLearningAPP.models import User, Course, Homework, Answer, Assignment, Teaching, Selecting
from django.urls import reverse
class HomeworkTestCase(TestCase):

    def setUp(self):
        # 创建学生用户
        self.student1 = User.objects.create(userId=21301146, userName="Student1", password="password1", email="student1@example.com")
        self.student2 = User.objects.create(userId=21301147, userName="Student2", password="password2", email="student2@example.com")

        # 创建老师用户
        self.teacher = User.objects.create(userId=2130111, userName="Teacher", password="password", email="teacher@example.com")

        # 创建课程
        self.course = Course.objects.create(courseId=1111, courseName="TestCourse")

        # 创建教学记录
        self.teaching = Teaching.objects.create(teacherId=self.teacher, courseId=self.course)

        # 学生选修课程
        Selecting.objects.create(studentId=self.student1, teachingId=self.teaching,selectingId = 1)
        Selecting.objects.create(studentId=self.student2, teachingId=self.teaching,selectingId = 2)

        # 创建作业
        self.homework = Homework.objects.create(
            homeworkId=1,
            teacherId=self.teacher,
            content="Test Homework Content",
            courseId=self.course,
            standAns="Test Answer",
            startTime=timezone.now(),
            endTime=timezone.now(),
            homeworkDes="Test Homework Description"
        )

        self.homework11 = Homework.objects.create(
            homeworkId=11,
            teacherId=self.teacher,
            content="Test Homework Content",
            courseId=self.course,
            standAns="Test Answer",
            startTime=timezone.now(),
            endTime=timezone.now(),
            homeworkDes="Test Homework Description"
        )

        # 学生提交答案
        self.answer1 = Answer.objects.create(
            answerId=1,
            homeworkId=self.homework,
            studentId=self.student1,
            answer="Answer by Student1"
        )
        self.answer2 = Answer.objects.create(
            answerId=2,
            homeworkId=self.homework,
            studentId=self.student2,
            answer="Answer by Student2"
        )

        # 创建分配任务
        self.assignment1 = Assignment.objects.create(
            student=self.student2,
            answer=self.answer1,
            teacher=self.student1,
            grade="1",
            comments="1"
        )
        self.assignment2 = Assignment.objects.create(
            student=self.student1,
            answer=self.answer2,
            teacher=self.student2,
            grade="1",
            comments="1"
        )

    def test_list_homeworks(self):
        url = reverse('list_all_homeworks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_create_homework(self):
        url = reverse('add_homework')
        data = {
            "teacherId": self.student1.userId,
            "content": "New Homework Content",
            "courseId": self.course.courseId,
            "startTime": timezone.now().isoformat(),
            "endTime": timezone.now().isoformat(),
            "standAns": "New Standard Answer",
            "homeworkDes": "New Homework Description"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_homework(self):
        url = reverse('delete_homework')
        data = {"homeworkId": '4'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_homework(self):
        url = reverse('delete_homework')
        data = {"homeworkId": '11'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_homework_partial(self):
        url = reverse('update_homework')
        data = {
            "homeworkId": self.homework.homeworkId,
            "content": "Updated Homework Content"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_homework_partial2(self):
        url = reverse('update_homework')
        data = {
            "homeworkId": 2,
            "content": "Updated Homework Content"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_show_homework(self):
        url = reverse('show_homework') + '?homeworkId=' + str(self.homework.homeworkId)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_get_homeworks_by_course(self):
        url = reverse('get_homework_by_course') + '?courseId=' + str(self.course.courseId)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_get_homeworks_by_course_for_stu(self):
        url = reverse('get_homework_for_student_by_course') + '?courseId=' + str(self.course.courseId) + '&studentId=' + str(self.student1.userId)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ScoreDistributionTestCase(TestCase):
    def setUp(self):
        # 创建测试数据
        self.teacher = User.objects.create(userId=1, userName="Teacher", roleType=1)
        self.course = Course.objects.create(courseId=1, courseName="Math")
        self.teaching = Teaching.objects.create(teachingId=1, teacherId=self.teacher, courseId=self.course)
        self.student = User.objects.create(userId=2, userName="Student")
        self.homework = Homework.objects.create(
            homeworkId=1,
            teacherId=self.teacher,
            content="Test Homework Content",
            courseId=self.course,
            standAns="Test Answer",
            startTime=timezone.now(),
            endTime=timezone.now(),
            homeworkDes="Test Homework Description"
        )
        self.homework11 = Homework.objects.create(
            homeworkId=11,
            teacherId=self.teacher,
            content="Test Homework Content",
            courseId=self.course,
            standAns="Test Answer",
            startTime=timezone.now(),
            endTime=timezone.now(),
            homeworkDes="Test Homework Description"
        )

        # 创建答案实例，确保覆盖所有分数区间
        Answer.objects.create(answerId=1, homeworkId=self.homework, studentId=self.student, finalScore="95￥！0")
        Answer.objects.create(answerId=2, homeworkId=self.homework, studentId=self.student, finalScore="85￥！0")
        Answer.objects.create(answerId=3, homeworkId=self.homework, studentId=self.student, finalScore="75￥！0")
        Answer.objects.create(answerId=4, homeworkId=self.homework, studentId=self.student, finalScore="65￥！0")
        Answer.objects.create(answerId=5, homeworkId=self.homework, studentId=self.student, finalScore="55￥！0")

    def test_get_score_distribution(self):
        url = reverse('get_homework_grade_distribution')  # 替换为实际的URL名
        params = {
            'course': 'Math',
            'class': 2,  # 假设的班级编号
            'teacher': 'Teacher'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # 检查返回的数据格式和计算结果
        expected_distribution = {
            'gradeNum1': 20.0,  # >=90
            'gradeNum2': 20.0,  # 80-89
            'gradeNum3': 20.0,  # 70-79
            'gradeNum4': 20.0,  # 60-69
            'gradeNum5': 20.0   # <60
        }

    def test_get_score_distribution2(self):
        url = reverse('get_homework_grade_distribution')  # 替换为实际的URL名
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # 检查返回的数据格式和计算结果
        expected_distribution = {
            'gradeNum1': 20.0,  # >=90
            'gradeNum2': 20.0,  # 80-89
            'gradeNum3': 20.0,  # 70-79
            'gradeNum4': 20.0,  # 60-69
            'gradeNum5': 20.0   # <60
        }

