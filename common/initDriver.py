from appium import webdriver

class initsetupteardown:
    def init_driver(self):
        desiredCaps = {}
        #设备信息
        desiredCaps["platformName"] = "Android"
        #设备系统版本
        desiredCaps["paltformVersion"] = "7.1.2"
        #app包名
        desiredCaps["appPackage"] = "cn.com.quanyou.attnd"
        #app启动activity
        desiredCaps["appActivity"] = "cn.com.quanyou.attnd.ui.SplashActivity"
        #设备名字
        desiredCaps["deviceName"] = "xiaomi"
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

if __name__ == '__main__':
    initsetupteardown().init_driver()