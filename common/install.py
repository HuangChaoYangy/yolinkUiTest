# -*- coding: utf-8 -*-
# @Time    : 2023/12/14 20:41
# @Author  : 黄朝阳
# @FileName: install,安装uiautomator2
# @Software: PyCharm

import os

# https://pypi.douban.com/simple  # 豆瓣镜像
# https://pypi.tuna.tsinghua.edu.cn/simple  # 清华镜像
mirror = " -i https://pypi.tuna.tsinghua.edu.cn/simple"
os.system("python -m pip install --upgrade pip" + mirror)  # 更新 pip
os.system("pip install --pre -U uiautomator2" + mirror)  # 安装 uiautomator2
os.system("pip install --pre weditor" + mirror)  # 安装 weditor
os.system("python -m uiautomator2 init")  #安装 atx-agent 至手机
