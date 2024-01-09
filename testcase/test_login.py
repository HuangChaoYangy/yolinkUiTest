from page.loginPage import LoginPage
import pytest,allure,os
from common.initDriver import initsetupteardown
from common.log import Bf_log
from common.yamlControl import Yaml_data
from appium import webdriver
from base.baseBage import BasePage
from selenium.webdriver.common.by import By

# epic 项目名称描述
@allure.epic('[项目名称] YOYO APP')
# feature 项目版本
@allure.feature('[项目版本] YOYO APP_V5.39')
class TestLogin:
    #获取driver
    def setup_class(self):
        # 获取initDriver文件中的driver对象
        # self.driver = initsetupteardown().init_driver()

        rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取文件的绝对路径
        path = os.path.join(rootPath, "config\devicesConfig.yaml")  # 获取当前文件的路径
        devices_result = Yaml_data().read_yaml_file(yaml_file=path, isAll=True)
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", devices_result["desiredCaps"])

    userPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取文件的绝对路径
    user_path = os.path.join(userPath, "testdata/testLogin/test_login.yaml")  # 获取当前文件的路径
    userInfo = Yaml_data().read_yaml_file(yaml_file=user_path, isAll=False)
    # 用例模块
    @allure.story('[功能模块] 用户登录模块')
    @pytest.mark.parametrize("inData, expData",userInfo)
    # 管理测试用例的链接地址
    @allure.testcase(url='http://pan.quanyou.com.cn/index.php?mod=onlyoffice&path=dlNQaTRtbVFaODBOLV94YWVfTGQ4ZHVGdDFQNTFnNWVtTkJsaHhaNTV4OU9nTy01VFZubWNTVi12QmxtR1pDU3BzMjZ0V2M3QTBXYjVn',name='测试用例地址')
    # 管理缺陷的链接地址
    @allure.issue(url='http://172.31.11.219/bug-browse-30-0-all.html', name='缺陷管理工具禅道地址')
    # 用例描述
    @allure.description('登录测试用例 执行人：黄朝阳')
    @allure.severity('normal')  # 用例等级
    # 用例等级 blocker、critical、normal、minor、trivial
    def test_login(self,inData, expData):
        with allure.step("实例化页面"):
            login_page = LoginPage(self.driver)

        title = inData['title']
        allure.dynamic.title(title)
        username = inData['uname']
        password = inData['pwd']
        except_result = expData['except']
        print("期望："+except_result)
        with allure.step("进行登录操作"):
            actual_result = login_page.login(username=username, password=password)
            print('实际结果：'+actual_result)

            with allure.step(f"步骤一：打开yoyo APP,进行登录页面"):
                Bf_log('test_login').info(f"步骤一：打开yoyo APP,开始执行用例:{title}")
            with allure.step(f"步骤二：输入账号：{username}"):
                Bf_log('test_login').info(f"步骤二：输入账号：{username}")
            with allure.step(f"步骤三：输入密码：{password}"):
                Bf_log('test_login').info(f"步骤三：输入密码：{password}")
            with allure.step(f"步骤四：点击同意隐私协议"):
                Bf_log('test_login').info(f"步骤四：点击同意隐私协议")
            with allure.step(f"步骤五：点击登录按钮"):
                Bf_log('test_login').info(f"步骤五：点击登录按钮")

            # 判断登录成功的定位信息是否存在
            if actual_result == except_result:
                with allure.step(f'步骤六：实际元素结果：{actual_result}, 期望元素结果：{except_result},==》测试通过'):
                    Bf_log('test_login').info(f'步骤六：实际元素结果:{actual_result}, 期望元素结果：{except_result},==》测试通过')
                with allure.step(f'步骤七：截图：{LoginPage(self.driver).get_screenshot()}'):
                    Bf_log('test_login').info(f'步骤七：截图：{LoginPage(self.driver).get_screenshot()}')
            else:
                with allure.step(f'步骤七：实际元素结果：{actual_result}, 期望元素结果：{except_result},==》测试不通过'):
                    Bf_log('test_login').info(f'步骤六：实际元素结果:{actual_result}, 期望元素结果：{except_result},==》测试不通过')
                with allure.step(f'步骤七：截图：{LoginPage(self.driver).get_screenshot()}'):
                    Bf_log('test_login').info(f'步骤七：截图：{LoginPage(self.driver).get_screenshot()}')
            assert str(actual_result) == str(except_result)

    #执行完用例之后退出会话
    def teardown_class(self):
        # self.driver.close_app()  # 关闭当前的app，未关闭驱动对象
        self.driver.quit()         # 关闭驱动对象,同时关闭所有关联的app


if __name__ == '__main__':

    pytest.main(['test_login.py','-s', '-v', '--alluredir','../report/allure-report'])
    # pytest.main(['test_login.py','-vs', '-q', '--alluredir', './report/allure-report','--clean-alluredir'])
    os.system("allure serve ../report/allure-report")
    # os.system("allure generate report/tmp -c -o report/allure-report")

    # pytest.main(['-vs', '-q', 'test_login.py', '--alluredir=./report/allure-report','--clean-alluredir', ])
    # os.system(r"allure generate -c -o allure-report")
