# -*- coding: utf-8 -*-
# @Time    : 2023/11/10 13:20
# @Author  : 黄朝阳
# @FileName: base_dir
# @Software: PyCharm

import os
# 项目的路径
rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(rootPath + "\yolinkUi")
# base_dir = 'D:\project\BfLibrary'
# base_dir = r'D:\testCode\yolinkUi'
# base_dir =r'C:\Users\huangchaoyang3\PycharmProjects\yolinkUi'
# 日志地址
log_dir = os.path.join(base_dir, 'logsFile')
screenshots_dir = os.path.join(base_dir, 'screenshots')

print(screenshots_dir)
