# -*- coding: utf-8 -*-
# @Time    : 2023/12/21 15:04
# @Author  : 黄朝阳
# @FileName: yolink_message
# @Software: PyCharm

import time
import threading
from multiprocessing import process
import random
import pyautogui

from pywinauto.keyboard import SendKeys
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Session:
    def __init__(self):
        self.fk = Faker('zh_CN')
        opaction = webdriver.ChromeOptions()
        opaction.add_argument('--headless')
        opaction.add_argument('--headless')
        opaction.add_argument("--disable-extensions")
        opaction.add_argument("--disable-gpu")
        opaction.add_argument("--proxy-server=direct://")
        opaction.add_argument("--proxy-bypass-list=(")
        opaction.add_argument("window-size=1920x1080")
        self.deiver = webdriver.Edge(options=opaction)
        self.deiver = webdriver.Chrome()
        self.deiver.maximize_window()
        self.deiver.get('https://yolinkcs.quanyou.com.cn/chat/#/')

    def findelmend_o(self,loc):
        '''
        查找元素
        :param loc:
        :return:
        '''
        try:
            fe = WebDriverWait(self.deiver, 30).until(EC.visibility_of_element_located(loc))
            return fe
        except:
            print(WebDriverWait(self.deiver, 30).until(EC.presence_of_element_located(loc)).text)


    def session_text(self,name, psd):
        '''
        登录+定位会话窗口
        :param name:
        :param psd:
        :return:
        '''
        element_list = ['0D87CE938606D874E0656FAF8EF401EA','0D8BDF413D761337E0656FAF8EF401EA','0D8859F20683E053E0656FAF8EF401EA']
        random_value = random.choice(element_list)

        # pyautogui.keyDown('ctrl')
        # pyautogui.keyDown('B')
        # time.sleep(3)
        #
        # # 定位下拉框并点击展开
        # dropdown = (By.XPATH,"//input[@placeholder='请选择客户端']")
        # self.findelmend_o(dropdown).click()
        #
        # # 定位下拉选项并点击目标选项
        # options = (By.XPATH,"//div[@class='el-select-dropdown__item selected hover']")
        # for option in options:
        #     if option == "el-input el-input--suffix":       # el-input el-input--suffix对应yoyoLink-windows-2.0.0
        #         option.click()
        #         break
        # time.sleep(3)
        # close_window = (By.XPATH, "//i[@class='el-dialog__close el-icon el-icon-close']")
        # self.findelmend_o(close_window).click()
        time.sleep(3)

        username = (By.XPATH,"//input[@placeholder='请输入工号']")
        password = (By.XPATH,"//input[@placeholder='请输入密码']")
        time.sleep(3)
        session = (By.XPATH, f"//div[@id='chat_list_{random_value}']")  # 定位会话窗口
        # 点击登录
        logbtn = (By.XPATH,"//div[@class='loginBtn']")
        time.sleep(3)
        self.findelmend_o(username).send_keys(name)
        self.findelmend_o(password).send_keys(psd)
        self.findelmend_o(logbtn).click()
        time.sleep(7)
        self.findelmend_o(session).click()
        time.sleep(1)

    def send_texta(self,count, name, password):
        '''
        发送消息
        :param count:
        :param name:
        :param password:
        :return:
        '''
        for i in range(int(count)):
            if i < 1:
                print('执行用户：{}'.format(name))
                self.session_text(name, password)
            else:
                input_text = (By.XPATH, "//div[@class='inputContent']")
                send_text = (By.XPATH, "//div[text()='发送']")
                self.findelmend_o(input_text).send_keys(f'编号【{i}】 ',self.fk.text())
                self.findelmend_o(send_text).click()
        else:
            time.sleep(5)
            self.deiver.quit()


if __name__ == '__main__':

    se = Session()
    se.send_texta(1000000, 'fengjing', '12345678a.')