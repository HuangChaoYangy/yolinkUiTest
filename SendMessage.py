# -*- coding: utf-8 -*-
# @Time    : 2023/12/21 10:38
# @Author  : 黄朝阳
# @FileName: SendMessage
# @Software: PyCharm

import time

from faker import Faker
from pywinauto import keyboard
class Send:
    def __init__(self):
        self.fk = Faker("zh_CN")
        time.sleep(5)
        keyboard.SendKeys(self.fk.address())
        keyboard.SendKeys('^a')
        keyboard.SendKeys('^c')
    def key_send(self):
        keyboard.SendKeys('^v')
        # keyboard.SendKeys(self.fk.address())
        keyboard.SendKeys('{ENTER}')

if __name__ == '__main__':
    se=Send()
    numbers = 10
    for i in range(numbers):
        se.key_send()
        print(f"已发送：{i + 1}条,剩余{numbers - i - 1}条")