from page.loginPage import LoginPage
import pytest,allure,os
from common.initDriver import initsetupteardown
from common.log import Bf_log

@allure.feature("进行登录")
class TestLogin:
    #获取driver
    def setup_class(self):
        self.driver = initsetupteardown().init_driver()

    #执行完用例之后退出会话
    def teardown_class(self):
        self.driver.quit()

    @allure.story("yolink登录")
    @allure.title("进行登录")
    def test_login_01(self):
        with allure.step("实例化页面"):
            login_page = LoginPage(self.driver)
        with allure.step("进行登录操作"):
            login_page.login(username="13551391038",password="12345678")
            Bf_log('登录').info(f'账号：{13551391038}')


if __name__ == '__main__':

    pytest.main(['-s', '-v', '--alluredir=report/allure-report'])
    # pytest.main(["test_login.py",'-vs', '-q', '--alluredir', './report/allure-report','--clean-alluredir'])
    # os.system("allure serve ./report/allure-report")
    # os.system("allure generate report/tmp -c -o report/allure-report")

    # pytest.main(['-vs', '-q', 'test_login.py', '--alluredir=./report/allure-report','--clean-alluredir', ])
    # os.system(r"allure generate -c -o allure-report")
