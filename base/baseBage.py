import os
import allure
from tkinter import Image

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver
# from PIL import Image
import datetime
from base_dir import screenshots_dir
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(5)

    def find_element_o(self,loc,timeout=30,poll=0.5):
        """
        根据定位获取单个元素
        :param loc: 查找元素方式及属性值，元祖方式传递（By.ID,ID属性值）
        :param timeout: 等待时长
        :param poll: 查询频率
        :return: 定位对象
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(*loc))
        except Exception as e:
            return "查找元素异常"
        #return self.driver.find_element(*loc)

    def find_element_os(self,loc,timeout=30,poll=0.5):
        """
        根据定位获取一组个元素
        :param loc: 查找元素方式及属性值，元祖方式传递（By.ID,ID属性值）
        :param timeout: 等待时长
        :param poll: 查询频率
        :return: 定位对象
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_elements(*loc))
        except Exception as e:
            return "查找元素异常"
        #return self.driver.find_element(*loc)

    def click_element(self,loc,desc=''):
        """
        点击操作
        :param loc: 查找元素方式及属性值，元祖方式传递（By.ID,ID属性值）
        :return:
        """
        self.find_element_o(loc).click()

    def input_text(self,loc,text,desc=''):
        """
        输入操作
        :param loc: 查找元素方式及属性值，元祖方式传递（By.ID,ID属性值）
        :param text: 输入的值
        :return:
        """
        ele = self.find_element_o(loc)
        ele.clear()
        ele.send_keys(text)

    # def long_press_element(self,ele,duration=2000,desc=''):
    #     """
    #     长按操作
    #     :param loc:
    #     :return:
    #     """
    #     TouchAction(self.driver).long_press(el=ele,duration=duration)

    def swipe(self,start_x,start_y,end_x,end_y,duration):
        '''
        需更新
        滑动操作
        :param start_x: 左滑的坐标
        :param start_y: 右滑的坐标
        :param end_x: 上滑的坐标
        :param end_y: 下滑的坐标
        :param duration: 等待时间
        :return:
        '''
        windows_size = self.driver.get_window_size()
        x = windows_size['width']
        y = windows_size['height']
        self.driver.swipe(start_x=x*start_x,
                          start_y=y*start_y,
                          end_x=x*end_x,
                          end_y=y*end_y,
                          duration=duration)


    def get_screen(self, screen_name):
        '''
        全屏截图
        :param screen_name:
        :return:
        '''
        self.driver.get_screenshot_as_file("screen/" + screen_name)

    def screenshot(self, partName, pictureName):
        '''
        共用方法：根据坐标区域精确截图
        :param partName:
        :param pictureName:
        :return:
        '''
        box = (0, 0, 0, 0)
        if partName == 'default':
            box = (0, 210, 1110, 1430)  # 区域1
        elif partName == 'hair':
            box = (110, 270, 950, 1145)  # 区域2
        self.driver.get_screenshot_as_file(
            '../picture/screenshot.png')  # 路径和名称，图片是.png格式
        image = Image.open('../picture/screenshot.png')
        new_image = image.crop(box)
        new_image.save(pictureName)  # 截取精确区域后的图片

    def get_screenshot(self):
        '''
        截图,截图的方法中不允许存在以下符号 / : * ? # ” < > |不然截图失败，所以只能将：改为-
        :return:
        '''

        img_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '//screenshots//'
        # time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        currrent_time =datetime.datetime.now()
        now_time = currrent_time.strftime("%Y-%m-%d %H-%M-%S")
        screen_save_path = screenshots_dir + "\\" + now_time + ".png"
        self.driver.get_screenshot_as_file(screen_save_path)
        return self.driver.get_screenshot_as_file(screen_save_path)

    def input_text(self,loc,text,desc=''):
        """
        输入操作
        :param loc: 查找元素方式及属性值，元祖方式传递（By.ID,ID属性值）
        :param text: 输入的值
        :return:
        """
        ele = self.find_element_o(loc)
        ele.clear()
        ele.send_keys(text)

    def long_press_element(self,loc,duration=4000,desc=''):
        """
        长按操作
        :param loc:
        :return:
        """
        el = self.find_element_o(loc).location
        TouchAction(self.driver).long_press(x=el['x'],y=el['y'],duration=duration).release().perform()

        action = TouchAction(self.driver)
        action.long_press(x=el['x'], y=el['y']).wait(duration).move_to(x=el['x'], y=el['y']).release()
        action.release()

    def alter(self,alter_text):
        """
        需更新
        弹窗
        :param alter_text:确认是否需要更新
        :return:
        """
        if self.find_element_o((By.XPATH,"//android.widget.TextView[@text='新版本']")).is_displayed():
            if alter_text:
                self.click_element(self.click_update)
            else:
                self.click_element(self.click_not_update)
        else:
            return None
    def Session_click(self,name:str=None):
        """
        点击进入会话
        :param name: 会话名称
        :return:
        """
        self.click_element((By.XPATH, f"//android.widget.TextView[@text='{name}']/.."))
    def send_text(self,text:str=None):
        """
        发送一条文本消息
        :param text: 输入内容
        :return:
        """
        if self.is_element_exist((By.ID,'cn.com.quanyou.attnd:id/audioButton')):
            self.click_element((By.XPATH,
                                '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView[@index="0"]'))

        self.input_text((By.ID,'cn.com.quanyou.attnd:id/editText'),text)
        self.click_element((By.CLASS_NAME,'android.widget.Button'))
    def send_voice(self,time):
        """
        语音发送
        :param time: 时间参数，毫秒级
        :return:
        """
        self.click_element((By.XPATH,'//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView[@index="0"]'))
        self.long_press_element((By.ID,'cn.com.quanyou.attnd:id/audioButton'),time)
    def is_element_exist(self, element, wait_seconds=3):
        """
        判断元素是否存在
        :param element: 元素值例如：(id,元素id)
        :param wait_seconds: 等待时间默认3秒
        :return: true或者false
        """
        by = element[0]
        value = element[1]
        try:
            if by == By.ID:
                WebDriverWait(self.driver, wait_seconds, 0.5).until(
                    expected_conditions.presence_of_element_located((By.ID, value)))
            elif by == By.NAME:
                WebDriverWait(self.driver, wait_seconds, 0.5).until(
                    expected_conditions.presence_of_element_located((By.NAME, value)))
            elif by == By.CLASS_NAME:
                WebDriverWait(self.driver, wait_seconds, 0.5).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == By.XPATH:
                WebDriverWait(self.driver, wait_seconds, 0.5).until(
                    expected_conditions.presence_of_element_located((By.XPATH, value)))
            elif by == By.CSS_SELECTOR:
                WebDriverWait(self.driver, wait_seconds, 1).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NameError("输入属性值错误,'id','name','class','xpath','css'.")
        except:
            return False
        return True

    def get_screen_size(self):
        """
        获取屏幕大小
        :return: tuple
        """
        windows_siize = self.driver.get_window_size()
        return [windows_siize['width'], windows_siize['height']]

    def swipe_screen(self, direction: str, duration_ms: int = 2000):
        """ 屏幕滑动操作
         direction: 操作方向 up\down\left\right
         duration_ms: 滑动时间 ms
         """
        location = self.get_screen_size()
        if direction.lower() == "up":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.75)
            end_y = int(location[1] * 0.25)
            self.driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "down":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.25)
            end_y = int(location[1] * 0.75)
            self.driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "left":
            start_x = int(location[0] * 0.9)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.1)
            self.driver.swipe(start_x, y, end_x, y, duration_ms)
        elif direction.lower() == "right":
            start_x = int(location[0] * 0.1)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.9)
            self.driver.swipe(start_x, y, end_x, y, duration_ms)
        else:
            print("请输入正确的方向")

    def get_screenshots(self, doc):
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        pic_name = now + '.png'
        self.driver.get_screenshot_as_file(pic_name)
        with open(pic_name, mode='rb') as f:
            file = f.read()
        allure.attach(file, doc, allure.attachment_type.PNG)
        return pic_name

    def result_assert(self, res, expected, doc=''):
        '''
        通过断言进行截图
        :param res:
        :param expected:
        :param doc:
        :return:
        '''
        try:
            assert res in expected
            with allure.step('添加成功截图...'):
                screen_name = self.get_screenshots(doc)
        except AssertionError:
            with allure.step('添加失败截图...'):
                screen_name = self.get_screenshots(doc)
                print((f'截图成功，图片为{screen_name}'))
            raise

