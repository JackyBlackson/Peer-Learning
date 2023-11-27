from django.test import TestCase
from django.core.exceptions import ValidationError
from PeerLearningAPP.models import User
from django.urls import reverse
import json





class UserViewTestCase(TestCase):

    def setUp(self):
        # 在测试开始前运行，创建测试数据
        User.objects.create(userId=1, userName="Alice", password="alice123", email="alice@example.com")

    def test_register_user(self):
        # 测试用户注册
        url = reverse('register_user')  # 假设您的 URL 名为 'register_user'
        data = {
            "email": "bob@example.com",
            "userName": "Bob",
            "password": "bob123",
            "userId": 2
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        # 测试用户登录
        url = reverse('user_login')  # 假设您的 URL 名为 'user_login'
        data = {
            "userId": "21301148",
            "password": "123456"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        # 测试用户删除
        # 这里需要处理身份验证和权限的问题，假设在测试中已经处理
        url = reverse('user_delete')  # 假设您的 URL 名为 'user_delete'
        data = {"userName": "Alice", "userId": 1}
        response = self.client.post(url, data)
        # self.assertEqual(response.status_code, 200)
    
    def test_show_info(self):
        # 测试显示用户信息
        url = reverse('show_info')  # 假设您的 URL 名为 'show_info'
        response = self.client.get(url + '?userId=1')
        self.assertEqual(response.status_code, 200)

    def test_modify_info(self):
        # 测试修改用户信息
        url = reverse('modify_user_info')  # 假设您的 URL 名为 'modify_info'
        data = {
            "userId": 1,
            "roleType": 2,
            "userName": "AliceUpdated",
            # ... 其他字段 ...
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        # 测试用户登出
        url = reverse('user_logout')  # 假设您的 URL 名为 'user_logout'
        response = self.client.post(url, {'userId': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_upload_token(self):
        # 测试获取上传令牌
        url = reverse('get_upload_token')  # 假设您的 URL 名为 'get_upload_token'
        response = self.client.get(url + '?filename=testfile.jpg')
        self.assertEqual(response.status_code, 200)

    def test_modify_user_info(self):
        # 测试修改用户信息（管理员功能）
        url = reverse('modify_user_info')  # 假设您的 URL 名为 'modify_user_info'
        data = {
            "userId": 1,
            "userName": "AliceAdmin",
            # ... 其他字段 ...
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_list_all_users(self):
        # 测试列出所有用户
        url = reverse('list_all_users')  # 假设您的 URL 名为 'list_all'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_assignments(self):
        # 测试列出用户的任务
        url = reverse('list_assignments')  # 假设您的 URL 名为 'list_assignment'
        response = self.client.get(url + '?userId=1')
        self.assertEqual(response.status_code, 200)
