from page.loginPage import LoginPage
import pytest,allure
from common.initDriver import initsetupteardown

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
    def test_login(self):
        with allure.step("实例化页面"):
            login_page = LoginPage(self.driver)
        with allure.step("进行登录操作"):
            login_page.login("15608078361","zyh@910426KaKa")

if __name__ == '__main__':
    pytest.main()
