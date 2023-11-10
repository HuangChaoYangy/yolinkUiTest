from appium import webdriver
from selenium.webdriver.common.by import By
from base.baseBage import BasePage

class initsetupteardown(BasePage):

    # 勾选协议
    check_xieyi = (By.ID, "cn.com.quanyou.attnd:id/deal_check_box")
    # 切换[密码登录]
    click_pulogin = (By.ID, "cn.com.quanyou.attnd:id/password_login_btn")
    # 输入账号
    click_username = (By.ID, "cn.com.quanyou.attnd:id/username")
    # 输入密码
    click_password = (By.ID, "cn.com.quanyou.attnd:id/password")
    # 登录
    click_login = (By.ID, "cn.com.quanyou.attnd:id/login")

    def init_driver(self):
        desiredCaps = {}
        #设备信息
        desiredCaps["platformName"] = "Android"
        #设备系统版本
        desiredCaps["paltformVersion"] = "12"
        #app包名
        desiredCaps["appPackage"] = "cn.com.quanyou.attnd"
        #app启动activity
        desiredCaps["appActivity"] = "cn.com.quanyou.attnd.ui.SplashActivity"
        #设备名字
        desiredCaps["deviceName"] = "21091116AC"
        #不清除应用数据
        desiredCaps["noReset"] = True
        #允许输入中文
        desiredCaps["unicodeKeyboard"] = True
        desiredCaps["resetKeyboard"] = True
        #允许app获取相关权限
        desiredCaps["autoGrantPermissions"]: True
        desiredCaps["automationName"] = "UiAutomator2"
        #修改超时时长，默认60s
        desiredCaps["newCommandTimeout"] = 3600

        #获取driver对象
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desiredCaps)
        return self.driver

    def quit_driver(self):
        self.driver.quit()

    def login(self,username,password):

        self.click_element(self.click_pulogin,'切换密码登录')
        self.input_text(self.click_username,username,'输入账号')
        self.input_text(self.click_password,password,'输入密码')
        self.click_element(self.check_xieyi,'勾选协议')
        self.click_element(self.click_login,'点击登录')

if __name__ == '__main__':

    object = initsetupteardown(BasePage)
    login=object.login(username="18728421687", password="12345678")