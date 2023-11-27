from django.test import TestCase
from django.urls import reverse
from PeerLearningAPP.models import User, Teaching, Course, Selecting, Answer, Assignment,Homework
import json

from PeerLearningAPP.views.assignment_views  import compute_student_score
from PeerLearningAPP.models import User, Course, Homework, Answer, Assignment, Teaching, Selecting
from datetime import datetime, timedelta

class PeerLearningAppTestCase(TestCase):

    def setUp(self):
        # 初始化测试数据，比如创建用户、课程、作业、答案等
        self.teacher = User.objects.create(userId=1, userName="TeacherUser", roleType=1)
        self.student = User.objects.create(userId=2, userName="StudentUser", roleType=2)
        self.course = Course.objects.create(courseId=1, courseName="Test Course")
        self.teaching = Teaching.objects.create(teachingId=1, teacherId=self.teacher, courseId=self.course)
        self.selecting = Selecting.objects.create(selectingId=1, studentId=self.student, teachingId=self.teaching)
        self.homework = Homework.objects.create(homeworkId=1, teacherId=self.teacher, courseId=self.course, content="Test Homework")
        self.answer = Answer.objects.create(answerId=1, homeworkId=self.homework, studentId=self.student, finalScore="80")
        self.assignment = Assignment.objects.create(assignmentId=1, student=self.student, answer=self.answer, teacher=self.teacher)

    def test_get_course_summary(self):
        # 测试 get_course_summary 函数
        response = self.client.get(reverse('get_course_summary'), {'teacherId': 1, 'courseId': 1})
        self.assertEqual(response.status_code, 200)

    def test_update_assignments_complaint(self):
        # 测试 update_assignments_complaint 函数
        url = reverse('update_assignment_complaint')
        data = {'answerId': 1, 'complaint': 'Test complaint'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # ... 更多测试用例 ...

    def test_get_courses_by_teacher(self):
        # 测试 get_courses_by_teacher 函数
        response = self.client.get(reverse('get_courses_by_teacher'), {'teacherId': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_courses_by_student(self):
        # 测试 get_courses_by_student 函数
        response = self.client.get(reverse('get_courses_by_student'), {'studentId': 2})
        self.assertEqual(response.status_code, 200)

    # ... 可以添加更多的测试用例 ...

    def test_compute_student_score(self):
    # 直接调用 compute_student_score 函数进行测试
        score = compute_student_score(80, 0.5, 8, 7)
        self.assertTrue(score is not None)

