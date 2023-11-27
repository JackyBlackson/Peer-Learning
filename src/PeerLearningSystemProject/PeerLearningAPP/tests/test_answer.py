import json
from django.urls import reverse
from django.test import TestCase
from PeerLearningAPP.models import *
from PeerLearningAPP.models import User, Course, Homework, Answer, Assignment, Teaching, Selecting

class AnswerViewTestCase(TestCase):

    def setUp(self):
        # 设置测试数据
        self.user = User.objects.create(userId=1, userName="TestUser", email="test@example.com", password="password")
        self.homework = Homework.objects.create(homeworkId=1, content="Test Homework")
        self.homework2 = Homework.objects.create(homeworkId=2, content="Test Homework")
        self.answer = Answer.objects.create(answerId=1, homeworkId=self.homework, studentId=self.user, answer="Test Answer")
        

    def test_get_answer_details_success(self):
        # 测试获取答案详情成功的情况
        url = reverse('get_answer_details')  # 替换为实际的URL名
        response = self.client.get(url, {'answerId': 1})
        self.assertEqual(response.status_code, 200)
        # 这里可以添加更多的断言来检查响应内容是否正确


    def test_create_answer_success(self):
        # 测试创建答案成功的情况
        url = reverse('create_answer')
        data = {
            'homeworkId': 1,
            'studentId': 1,
            'answer': 'New Answer',
            'finalScore': 100
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_answer_successs(self):
        # 测试创建答案成功的情况
        url = reverse('create_answer')
        data = {
            'answerId':1,
            'homeworkId': 2,
            'studentId': 1,
            'answer': 'New Answer',
            'finalScore': 100
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_answer_success(self):
        # 测试删除答案成功的情况
        url = reverse('delete_answer')
        data = {'answerId': 1}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    


    def test_update_answer_success(self):
        # 测试更新答案成功的情况
        url = reverse('update_answer')
        data = {'answerId': 1, 'answer': 'Updated Answer'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_answer_f(self):
        # 测试更新答案成功的情况
        url = reverse('update_answer')
        data = {'answerId': 4, 'answer': 'Updated Answer'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)




    def test_delete_answer_nonexistent_answer(self):
        # 测试删除不存在的答案
        url = reverse('delete_answer')
        data = {'answerId': 9999}  # 假设 9999 是一个不存在的答案 ID
        response = self.client.post(url, json.dumps(data), content_type='application/json')
       
