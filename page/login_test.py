# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 13:56
# @Author  : 黄朝阳
# @FileName: login_test  用于调试
# @Software: PyCharm

from appium import webdriver
from selenium.webdriver.common.by import By
from base.basePage_test import BasePage_test

class initsetupteardown(BasePage_test):

    # 勾选协议
    check_xieyi = (By.ID, "cn.com.quanyou.attnd:id/deal_check_box")
    # 切换[密码登录]
    click_pulogin = (By.ID, "cn.com.quanyou.attnd:id/password_login_btn")
    # 切换[刷脸登录]
    face_login = (By.ID, "cn.com.quanyou.attnd:id/face_login_way")
    # 输入密码输入框
    password_input = (By.XPATH, "//android.widget.EditText[@text='请输入密码']")
    # yoyo头像
    user_avatar = (By.ID, "cn.com.quanyou.attnd:id/user_avatar")
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
        desiredCaps["paltformVersion"] = "13"
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
        print(desiredCaps)
        #获取driver对象
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desiredCaps)
        return self.driver

    def login(self,username,password):
        user_avatar_text = self.find_element_o_t(loc=(By.ID, "cn.com.quanyou.attnd:id/user_avatar"))
        # print(user_avatar_text)
        if user_avatar_text == "查找元素异常":
            self.input_text_t(self.click_username,username,'输入账号')
            self.input_text_t(self.click_password,password,'输入密码')
            self.click_element_t(self.check_xieyi,'勾选协议')
            self.driver.implicitly_wait(3)
            self.click_element_t(self.click_login,'点击登录')

            # result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='账号密码错误!!']"))
            try:
                result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='友信']")).text
            except:
                result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='友信']"))
            print(result)
            print(222222222222222222222222)

            return result

        else:
            self.click_element_t(self.click_pulogin, '切换密码登录')
            self.input_text_t(self.click_username,username,'输入账号')
            self.input_text_t(self.click_password,password,'输入密码')
            self.click_element_t(self.check_xieyi,'勾选协议')
            self.driver.implicitly_wait(3)
            self.click_element_t(self.click_login,'点击登录')

            # result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='账号密码错误!!']"))
            try:
                result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='友信']")).text
            except:
                result = self.find_element_o_t(loc=(By.XPATH, "//android.widget.TextView[@text='友信']"))
            print(result)
            print(1111111111111111)

            return result


    def quit_driver(self):
        self.driver.quit()



if __name__ == '__main__':

    loc = initsetupteardown()
    login=loc.login(username="18728421687", password="123456789")