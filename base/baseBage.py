from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

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