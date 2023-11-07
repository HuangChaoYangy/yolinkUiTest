from base.baseBage import BasePage
from appium.webdriver.common.mobileby import By

class LoginPage(BasePage):

    #勾选协议
    check_xieyi = (By.ID,"cn.com.quanyou.attnd:id/deal_check_box")
    #切换[密码登录]
    click_pulogin = (By.ID,"cn.com.quanyou.attnd:id/password_login_btn")
    #输入账号
    click_username = (By.ID,"cn.com.quanyou.attnd:id/username")
    #输入密码
    click_password = (By.ID,"cn.com.quanyou.attnd:id/password")
    #登录
    click_login = (By.ID,"cn.com.quanyou.attnd:id/login")

    def login(self,username,password):
        self.click_element(self.click_pulogin,'切换密码登录')
        self.input_text(self.click_username,username,'输入账号')
        self.input_text(self.click_password,password,'输入密码')
        self.click_element(self.check_xieyi,'勾选协议')
        self.click_element(self.click_login,'点击登录')