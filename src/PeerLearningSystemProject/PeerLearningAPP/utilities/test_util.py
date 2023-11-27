import unittest
import string
import random
from basic_util import Enum, generate_random_string  # 替换为你的模块名

class TestEnumAndRandomString(unittest.TestCase):

    def test_enum(self):
        colors = Enum('RED', 'GREEN', 'BLUE')
        self.assertEqual(colors.RED, 0)
        self.assertEqual(colors.GREEN, 1)
        self.assertEqual(colors.BLUE, 2)
        self.assertEqual(colors['RED'], 0)
        self.assertEqual(colors['GREEN'], 1)
        self.assertEqual(colors['BLUE'], 2)
        colors[2]

    def test_generate_random_string(self):
        # 测试 generate_random_string 函数
        length = 10
        random_str = generate_random_string(length)
        self.assertEqual(len(random_str), length)
        self.assertTrue(all(c in string.ascii_letters for c in random_str))

