# -*- coding: utf-8 -*-
# @Time    : 2023/11/9 21:48
# @Author  : 黄朝阳
# @FileName: conftest
# @Software: PyCharm

import pytest
import allure
from common.initDriver import initsetupteardown


# driver_=None
# @pytest.fixture(scope="session",autouse=True)
# def driver_init():
#     global driver_
#     if driver_ is None:
#         driver_ = initsetupteardown().init_driver()
#     return driver_
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#     print(rep)
#     # rep.when可选参数有call、setup、teardown，s
#     # call表示为用例执行环节、setup、teardown为环境初始化和清理环节
#     if rep.when == "call" and rep.failed:
#         if hasattr(driver_, "get_screenshot_as_png"):
#             with allure.step('添加失败截图...'):
#                 allure.attach(driver_.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
#     elif rep.when == "call" and rep.passed:
#         if hasattr(driver_, "get_screenshot_as_png"):
#             with allure.step('添加成功截图...'):
#                 allure.attach(driver_.get_screenshot_as_png(), "成功截图", allure.attachment_type.PNG)

# 自动化测试止执行前 -- 环境初始化操作
@pytest.fixture(scope="session",autouse=True)        #function（测试函数级别），class（测试类级别），module（测试模块“.py”级别），session（多个文件级别）。默认是function级别
def start_running():
    print('---马上开始执行自动化测试---')
    yield   # 通过yield来唤醒teardown执行
    print('\n---自动化测试完成,开始处理本次测试数据---')

