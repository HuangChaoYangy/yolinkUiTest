import time

import selenium
#     def session_send(self):
from pywinauto.application import Application
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from base.baseBage import BasePage
from common.initDriver import initsetupteardown

#+更多按钮元素
more_img = (By.ID,"cn.com.quanyou.attnd:id/extImageView")
# 图片icon
img_id = (By.ID,"cn.com.quanyou.attnd:id/icon_0")
# 获取一组图片对象
imgs = (By.XPATH,"//android.widget.LinearLayout/android.widget.TextView[@class='android.widget.TextView']")
# 发送图片
send_img=(By.ID,"cn.com.quanyou.attnd:id/ll_picture_container")
# 返回按钮
left_back = (By.ID,"cn.com.quanyou.attnd:id/left_icon")
# 发送失败
fail = (By.ID,"cn.com.quanyou.attnd:id/errorLinearLayout")
# 获取发送消息元素
get_texts = (By.ID,"cn.com.quanyou.attnd:id/contentTextView")
list_text = (By.XPATH,"//android.widget.TextView[@text='文件传输助手']/../android.widget.TextView[3]")
# get_test = (By.XPATH,"//android.widget.TextView")


class SessionText(BasePage):

    def session_text(self,texts):

        self.Session_click('文件传输助手')
        self.send_text(text=texts)
        time.sleep(4)
        print(self.find_element_os(get_texts))
        result = self.find_element_os(get_texts)[-1].text

        self.click_element(left_back,'返回')
        result_c_last = self.find_element_o(list_text).text
        print(result,result_c_last)
        return result,result_c_last

if __name__ == '__main__':

    se = SessionText(initsetupteardown().init_driver())
    se.session_text(texts="测试文本")
