# -*- coding: utf-8 -*-
# @Time    : 2023/11/14 21:19
# @Author  : 黄朝阳
# @FileName: test
# @Software: PyCharm

list = [{'uname': 18728421687, 'pwd': 12345678}, {'uname': 15178713870, 'pwd': 12345676}, {'uname': 15608078361, 'pwd': 12345676}]
new_list = []
for i in list:
    new_list.append((str(i['uname']),str(i['pwd'])))
print(new_list)



from page.loginPage import LoginPage
import pytest,allure,os
from common.initDriver import initsetupteardown
from common.log import Bf_log
from common.yamlControl import Yaml_data
from appium import webdriver
from base.baseBage import BasePage

@allure.feature("进行登录")
class TestLogin:
    #获取driver
    def setup_class(self):
        # 获取initDriver文件中的driver对象
        # self.driver = initsetupteardown().init_driver()

        rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取文件的绝对路径
        path = os.path.join(rootPath, "config\devicesConfig.yaml")  # 获取当前文件的路径
        devices_result = Yaml_data().read_yaml_file(yaml_file=path, isAll=True)
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", devices_result["desiredCaps"])

    #执行完用例之后退出会话
    def teardown_class(self):
        self.driver.quit()

    userInfo = Yaml_data().read_yaml_file(yaml_file='../testdata/usrdata.yaml', isAll=True)
    user_info = []
    for usrdata in userInfo:
        user_info.append((str(usrdata['uname']), str(usrdata['pwd'])))
    @allure.story("yolink登录")
    @allure.title("输入账号密码，点击登录")
    @pytest.mark.parametrize("username,password",user_info)
    def test_login(self,username, password):
        with allure.step("实例化页面"):
            login_page = LoginPage(self.driver)
            base_page = BasePage(self.driver)
            # 获取登录失败的定位信息
            login_fail_info = login_page.login_fail_loc
            login_fail_result = login_fail_info[1]
            print(login_fail_result)
            except_result = "cn.com.quanyou.attnd:id/tv_content"
        with allure.step("进行登录操作"):
            login_page.login(username=username, password=password)
            Bf_log('登录页面').info(f'账号：{username}，密码：{password}')
            #判断登录失败的定位信息是否存在
            if login_fail_info:
                try:
                    # self.assertEqual(login_fail_result,except_result)
                    assert login_fail_result==except_result
                    print("登录失败，用例通过")
                except AssertionError:
                    base_page.get_screen('_bug' + '.jpg')
                    print("用例不通过")
                    raise AssertionError

            else:
                print("登录成功，用例通过")


if __name__ == '__main__':

    pytest.main(['-s', '-v', '--alluredir','../report/allure-report'])
    # pytest.main(["test_login.py",'-vs', '-q', '--alluredir', './report/allure-report','--clean-alluredir'])
    os.system("allure serve ../report/allure-report")
    # os.system("allure generate report/tmp -c -o report/allure-report")

    # pytest.main(['-vs', '-q', 'test_login.py', '--alluredir=./report/allure-report','--clean-alluredir', ])
    # os.system(r"allure generate -c -o allure-report")
