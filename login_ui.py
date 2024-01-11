# -*- coding: utf-8 -*-
# @Time    : 2024/1/5 16:14
# @Author  : 黄朝阳
# @FileName: login_ui
# @Software: PyCharm

import selenium.webdriver.remote.webdriver


from appium.webdriver.common.appiumby import By

from base.baseBage import BasePage


# from common.getYamlConfig import log
class LoginPage1(BasePage):

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
    #弹框确认
    click_pop= (By.ID,"cn.com.quanyou.attnd:id/tv_confirm")
    # 弹框元素获取
    pop_text=(By.ID,"cn.com.quanyou.attnd:id/tv_content")
    # 协议确认取消
    xieyi_queren =(By.ID,"cn.com.quanyou.attnd:id/agree_button")
    xieyi_qux =(By.ID,"cn.com.quanyou.attnd:id/cancel_button")

    def swith_to(self,username,password):
        """
        处于账号密码登录界面登录
        :param username:
        :param password:
        :return:返回元素对象
        """
        self.click_element(self.click_username)
        self.find_element_o(self.click_username).clear()
        self.click_element(self.click_password)
        self.find_element_o(self.click_password).clear()
        self.input_text(self.click_username, username, '输入账号')
        self.input_text(self.click_password, password, '输入密码')
        self.click_element(self.click_login, '点击登录')
        # print(self.find_element_o(self.xieyi_qux).text)
        if self.is_element_exist(self.xieyi_qux):
            self.click_element(self.xieyi_queren)
            self.click_element(self.click_login, '点击登录')


        if self.is_element_exist((By.XPATH,"//android.widget.TextView[@text='消息']")):
            return self.find_element_o((By.XPATH, "//android.widget.TextView[@text='消息']")).text
            # print(self.find_element_o(self.pop_text).text)
        else:
            result = self.find_element_o(self.pop_text).text
            self.click_element(self.click_pop)
            print(result)
            return result


    def swith_todo(self,username,password):
        """
        切换为密码登录
        :param username:
        :param password:
        :return:
        """
        self.click_element(self.click_pulogin, '密码登录')
        self.input_text(self.click_username, username, '输入账号')
        self.input_text(self.click_password, password, '输入密码')
        self.click_element(self.check_xieyi, '勾选协议')
        self.click_element(self.click_login, '点击登录')
        # print('----------------------------------')
        # print(self.find_element_o(self.pop_text))
        # print('----------------------------------')
        if self.is_element_exist((By.XPATH,"//android.widget.TextView[@text='消息']")):
            return self.find_element_o((By.XPATH, "//android.widget.TextView[@text='消息']")).text
        else:
            self.click_element(self.click_pop)
            self.click_element(self.click_username)
            self.find_element_o(self.click_username).clear()
            self.click_element(self.click_password)
            self.find_element_o(self.click_password).clear()
            return "查找元素异常"

    def quit_login(self):
        """
        退出登录
        :return:
        """
        self.click_element((By.XPATH, "//android.widget.TextView[@text='我的']"))
        self.click_element((By.XPATH, "//android.widget.TextView[@text='设置']//.."))
        self.click_element((By.ID, "cn.com.quanyou.attnd:id/bn_logout"))

    def login(self,username,password):
        if self.find_element_o((By.XPATH,"//android.widget.TextView[@text='消息']"),timeout=3)!="消息":
            print('进入')
            if self.is_element_exist(self.click_pulogin):
                    # (self.find_element_o(self.click_pulogin, '密码登录') != '查找元素异常'):
                print('进入刷脸')
                result =self.swith_todo(username,password)
                self.quit_login()
                return result
                # log().info('--进入打印---')
            else:
                print('密码登录页面')
                result = self.swith_to(username,password)
                return result
                # log().info('self.click_login')
        else:
            print('退出')
            self.quit_login()
            result =self.swith_to(username,password)
            return result


if __name__ == '__main__':

    loginObject = LoginPage1(BasePage)
    loginObject.login(username='18728421687',password='12345678')

