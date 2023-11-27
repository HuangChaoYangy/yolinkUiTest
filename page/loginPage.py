from base.baseBage import BasePage
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

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
    #登录失败提示
    login_fail_loc = (By.ID, "cn.com.quanyou.attnd:id/tv_content")
    #账号密码错误提示
    user_prd_error_loc = (By.XPATH, "//android.widget.TextView[@text='账号密码错误!!']")
    #员工不存在提示
    user_not_exist_loc = (By.XPATH, "//android.widget.TextView[@text='员工不存在.']")

    def login(self,username,password):
        '''
        登录yoyo
        :param username:
        :param password:
        :return:
        '''
        # 判断切换密码登录按钮是否存在
        if self.click_element(self.click_pulogin,'切换密码登录'):
            self.input_text(self.click_username,username,'输入账号')
            self.input_text(self.click_password,password,'输入密码')
            self.click_element(self.check_xieyi,'勾选协议')
            # self.driver.implicitly_wait(3)
            self.click_element(self.click_login,'点击登录')
        else:
            self.input_text(self.click_username,username,'输入账号')
            self.input_text(self.click_password,password,'输入密码')
            self.click_element(self.check_xieyi,'勾选协议')
            # self.driver.implicitly_wait(3)
            self.click_element(self.click_login,'点击登录')



if __name__ == '__main__':

    loginObject = LoginPage(BasePage)
    loginObject.login(username='18728421687',password='1234567811')