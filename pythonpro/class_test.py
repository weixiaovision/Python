#coding:utf-8
#Import the common package
import os
import unittest
from appium import webdriver
from time import sleep
import sys

# __author__ = 'sker'

#设置路径信息
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class LoginAndroidTests(unittest.TestCase):


    def setUp(self):
        #初始化测试平台
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'BY3AEK14CW089372'
        #desired_caps['app'] = 'D:\apk\爱壁纸.apk'
        desired_caps['appPackage'] = 'com.lovebizhi.wallpaper'
        desired_caps['appActivity'] = 'com.lovebizhi.wallpaper.WelcomeActivity'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        #三种登录的方法，默认选中的都为False
        self._logins = {"weibo":False,"tencent":False,"lovebizhi":False}
        #跳转到登录界面
        self.toLoginPage()

    def tearDown(self):

        self.driver.quit()

    """
    loginMethod:登录的方法
    method：传入的字符串
    """
    def loginMethod(self,method):
        try:
            self.method = self.driver.find_element_by_class_name(method)
        except Exception as e:
            self._logins[method] = False
            print(e)
        else:
            self._logins[method] = True
    """
    toLoginPage:跳转到登录界面
    """
    def toLoginPage(self):
        #判断是否安装爱壁纸APP
        wallpaper = self.driver.is_app_installed("com.lovebizhi.wallpaper")
        if wallpaper:
            sleep(8)
            print(u"已经安装爱壁纸")
            # 点击头部的菜单栏
            self.driver.find_element_by_id("com.lovebizhi.wallpaper:id/logo").click()
            print(u"出现隐藏的菜单栏")
            sleep(2)
            print(u"当前的activity是" + self.driver.current_activity)
            # 点击登录头像
            self.driver.find_element_by_id("com.lovebizhi.wallpaper:id/ivFace").click()
            print(u"跳转到登录页面")
            sleep(2)
            print(u"获取控件名称")
            print(self.driver.contexts)
            for context in self.driver.contexts:
                print(context)
            sleep(2)
            print(u"切入h5的webdriver控件")
            self.driver.switch_to.context("WEBVIEW_com.lovebizhi.wallpaper")
            sleep(2)

        else:
            print(u"开始安装apk")
            self.driver.install_app("D:\apk\爱壁纸.apk")
            sleep(30)

    """
    weiBo:微博登录
    username:用户名
    password:密码
    """
    def weiBo(self,username,password):
        if(self._logins["weibo"]):
            self.driver.find_element_by_accessibility_id('用新浪微博登录').click()
            print(u"进入通过微博登录")
            sleep(5)
            print(u"输入用户名和密码")
            self._username = self.driver.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[3]/android.widget.EditText[1]")
            self._username.send_keys(username)
            self._pwd = self.driver.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[3]/android.widget.EditText[2]")
            self._pwd.send_keys(password)
            sleep(2)
            print(u"点击登录")
            self.driver.find_element_by_accessibility_id('登录 Link').click()
            sleep(5)
        else:
            print(u"无法用微博登录")

    # """
    # QQ:QQ登录
    # username:用户名
    # password:密码
    # """
    # def QQ(self, username, password):
    #     if(self._logins["tencent"]):
    #         self.method.click()
    #         print(u"进入通过QQ登录")
    #         sleep(6)
    #         print(u"输入用户名和密码")
    #         self._username = self.driver.find_element_by_id("u")
    #         self._username.send_keys(username)
    #         self._pwd = self.driver.find_element_by_id("p")
    #         self._pwd.send_keys(password)
    #         sleep(2)
    #         print(u"点击登录")
    #         self.driver.find_element_by_id("go").click()
    #         sleep(5)
    #     else:
    #         print(u"无法用QQ登录")
    #
    # """
    # paper:爱壁纸登录
    # username:用户名
    # password:密码
    # """
    # def paper(self,username,password):
    #     if(self._logins["lovebizhi"]):
    #         self.method.click()
    #         print(u"进入通过爱壁纸登录")
    #         sleep(6)
    #         print(u"输入用户名和密码")
    #         self._username = self.driver.find_element_by_id("user")
    #         self._username.send_keys(username)
    #         self._pwd = self.driver.find_element_by_id("pass")
    #         self._pwd.send_keys(password)
    #         sleep(2)
    #         print(u"点击登录")
    #         self.driver.find_element_by_id("login").click()
    #         sleep(5)
    #     else:
    #         print(u"无法用QQ登录")


    def test_weibo1(self):
        self.loginMethod("weibo")
        self.weiBo("admin","123456")
        sleep(4)
        self.assertEqual(u"admin",self.driver.find_element_by_class_name("logins_a_em").text)
        sleep(2)

    # def test_QQ1(self):
    #     self.loginMethod("tencent")
    #     self.QQ("admin","123456")
    #     sleep(4)
    #     self.assertEqual(u"admin",self.driver.find_element_by_id("name").value)
    #     sleep(2)
    #
    # def test_paper1(self):
    #     self.loginMethod("lovebizhi")
    #     self.paper("admin","123456")
    #     sleep(4)

if __name__ == '__main__':
    suite =unittest.TestLoader().loadTestsFromTestCase(LoginAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)