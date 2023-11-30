# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 13:34
# @Author  : 黄朝阳
# @FileName: run_all_cases.py
# @Software: PyCharm

import os
import pytest

# 当前路径(使用 abspath 方法可通过dos窗口执行)
rootPath = os.path.dirname(os.path.abspath(__file__))
test_login_path = os.path.join(rootPath,"testcase/test_login.py")


if __name__ == '__main__':

    # pytest.main()
    pytest.main([f'{test_login_path}','-s', '-v', '--alluredir','../report/allure-report'])
    os.system("allure serve ../report/allure-report")
