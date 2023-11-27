from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver
from PIL import Image

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
        return WebDriverWait(self.driver,timeout,poll).until(lambda x:x.find_element(*loc))
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

    def long_press_element(self,ele,duration=2000,desc=''):
        """
        长按操作
        :param loc:
        :return:
        """
        TouchAction(self.driver).long_press(el=ele,duration=duration)

    def swipe(self,start_x,start_y,end_x,end_y,duration):
        '''
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


    def get_scrren(self, screen_name):
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

