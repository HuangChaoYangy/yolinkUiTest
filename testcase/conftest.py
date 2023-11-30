# -*- coding: utf-8 -*-
# @Time    : 2023/11/9 21:48
# @Author  : 黄朝阳
# @FileName: conftest
# @Software: PyCharm

import pytest

# 自动化测试止执行前 -- 环境初始化操作
@pytest.fixture(scope="session",autouse=True)        #function（测试函数级别），class（测试类级别），module（测试模块“.py”级别），session（多个文件级别）。默认是function级别
def start_running():
    print('---马上开始执行自动化测试---')
    yield   # 通过yield来唤醒teardown执行
    print('\n---自动化测试完成,开始处理本次测试数据---')

# import os
# import time
# import pytest
# from appium import webdriver
# from common.yamlControl import Yaml_data
#
# rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取文件的绝对路径
# path = os.path.join(rootPath, "config\devicesConfig.yaml")  # 获取当前文件的路径
# devices_result = Yaml_data().read_yaml_file(yaml_file=path, isAll=True)
# # driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", devices_result["desiredCaps"])
# appPackage = devices_result["desiredCaps"]['appPackage']
#
# @pytest.fixture()
# def start_app(devices_result):
#     global driver
#     driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',devices_result["desiredCaps"])
#     return driver
#
# # 关闭安卓系统中的计算器app
# @pytest.fixture()
# def close_app():
#     yield driver
#     time.sleep(2)
#     driver.terminate_app(appPackage)
