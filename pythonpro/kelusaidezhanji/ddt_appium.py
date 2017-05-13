#!/usr/bin/python
# -*- coding:utf-8 -*-


import unittest
from appium import webdriver
from time import sleep


class AndroidLoggingTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '4.4.2',
                        'deviceName': 'BY3AEK14CW089372',
                        'appPackage': 'com.otaku.CrusadersQuest.huawei',
                        'appActivity': 'com.toastgame.hsp.otakuchannel.LaunchActivity'
                        }

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        print('初始化完成。')
        print(self.driver.current_activity)

    def tearDown(self):
        self.driver.quit()
        print('关闭app')

    def testlogging(self):
        print('开始测试：')
        wallapp = self.driver.is_app_installed('com.otaku.CrusadersQuest.huawei')
        if wallapp:
            print('已安装，可以直接测试')
            self.driver.launch_app()
            sleep(100)
            pass
        else:
            print('没有安装该app')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidLoggingTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
