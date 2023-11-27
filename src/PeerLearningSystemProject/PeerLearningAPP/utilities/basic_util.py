import random
import string

# python好像有enmu枚举类(
class Enum:
    def __init__(self, *args):
        self.enum_values = args
        self.name_to_value = {name: idx for idx, name in enumerate(args)}
        for idx, name in enumerate(args):
            setattr(self, name, idx)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.name_to_value[item]
        elif isinstance(item, int):
            return self.enum_values[item]


    
    
def generate_random_string(length : int) -> str:
    # 定义包含字符的范围，即大小写字母和数字
    characters = string.ascii_letters
    # 从字符范围中随机选择 length 个字符
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string