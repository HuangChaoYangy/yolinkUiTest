# 导入需要用到的库
import os
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 定义常量
APP_PACKAGE = 'cn.com.quanyou.attnd'
APP_ACTIVITY = 'cn.com.quanyou.attnd.ui.SplashActivity'

# 设置DesiredCapabilities
desired_capabilities = {
    'platformName': 'Android',  # 指定平台（iOS或Android）
    'platformVersion': '12',  # 指定版本号
    'deviceName': '21091116AC',  # 指定设备名称
    'appPackage': APP_PACKAGE,  # 指定应用包名
    'appActivity': APP_ACTIVITY,  # 指定应用入口Activity
    'autoGrantPermissions': True,  # 自动授予权限
    'noReset': True,  # 不重置应用
}


class AppiumDriver(object):
    """
    Appium驱动核心类，封装了许多Appium驱动所用的方法
    """

    def __init__(self):
        """
        初始化Appium驱动
        """
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities)

    def __del__(self):
        """
        退出Appium驱动并释放资源
        """
        self.driver.quit()

    def find_element(self, locator, timeout=10):
        """
        通过元素定位器查找单个元素
        :param locator: 元素定位器，格式为(By.XXX, 'value')，比如(By.ID, 'com.example.app:id/btn_login')
        :param timeout: 超时时间，默认为10秒
        :return: 找到的单个元素对象
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException):
            raise ValueError(f'找不到元素：{locator}')
        return element

    def find_elements(self, locator, timeout=10):
        """
        通过元素定位器查找多个元素
        :param locator: 元素定位器，格式为(By.XXX, 'value')，比如(By.ID, 'com.example.app:id/btn_login')
        :param timeout: 超时时间，默认为10秒
        :return: 找到的多个元素对象，返回一个列表
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except (TimeoutException, NoSuchElementException):
            raise ValueError(f'找不到元素：{locator}')
        return elements

    def find_element_by_text(self, text, timeout=10):
        """
        通过元素文本查找单个元素
        :param text: 元素文本
        :param timeout: 超时时间，默认为10秒
        :return: 找到的单个元素对象
        """
        locator = (By.XPATH, f'//*[contains(@text,"{text}")]')
        return self.find_element(locator, timeout)

    def find_elements_by_text(self, text, timeout=10):
        """
        通过元素文本查找多个元素
        :param text: 元素文本
        :param timeout: 超时时间，默认为10秒
        :return: 找到的多个元素对象，返回一个列表
        """
        locator = (By.XPATH, f'//*[contains(@text,"{text}")]')
        return self.find_elements(locator, timeout)

    def click(self, selector):
        """
        点击元素
        :param selector: 元素，可以是元素对象、元素定位器，或者是元素文本
        """
        if isinstance(selector, tuple):
            element = self.find_element(selector)
        elif isinstance(selector, str):
            element = self.find_element_by_text(selector)
        else:
            element = selector
        element.click()

    def send_keys(self, selector, value):
        """
        在元素中输入文本
        :param selector: 元素，可以是元素对象、元素定位器，或者是元素文本
        :param value: 要输入的文本
        """
        if isinstance(selector, tuple):
            element = self.find_element(selector)
        elif isinstance(selector, str):
            element = self.find_element_by_text(selector)
        else:
            element = selector
        element.send_keys(value)


if __name__ == '__main__':

    driver_re = AppiumDriver()

    # 切换密码登录
    login_button = (By.ID, 'cn.com.quanyou.attnd:id/password_login_btn')
    driver_re.click(login_button)

    # 输入用户名和密码
    username = (By.ID, 'cn.com.quanyou.attnd:id/username')
    password = (By.ID, 'cn.com.quanyou.attnd:id/password')
    driver_re.send_keys(username, '18728421687')
    driver_re.send_keys(password, '12345678')

    # 勾选协议
    xieyi_button = (By.ID, 'cn.com.quanyou.attnd:id/deal_check_box')
    driver_re.click(xieyi_button)

    # 点击登录按钮
    confirm_button = (By.ID, 'cn.com.quanyou.attnd:id/login')
    driver_re.click(confirm_button)