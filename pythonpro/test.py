import os
from time import sleep

import unittest

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class SimpleAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'BY3AEK14CW089372'
        # desired_caps['app'] = '/Users/runehero/Downloads/ApiDemos-debug.apk'
        desired_caps['appPackage'] = 'io.appium.android.apis'
        desired_caps['appActivity'] = '.ApiDemos'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()
        print('quit')

    # def test_install(self):
    #     if not self.driver.is_app_installed('io.appium.android.apis'):
    #         self.driver.install_app('/Users/runehero/Downloads/ApiDemos-debug.apk')
    #         print('install')

    # def test_activity(self):
    #     self.assertEqual('.ApiDemos', self.driver.current_activity)
    #     sleep(5)
    #
    # def test_background(self):
    #     self.driver.background_app(5)
    #     self.assertEqual('.ApiDemos', self.driver.current_activity)
    #     print('background')
    #     sleep(5)

    def test_screenshot(self):
        sleep(3)
        self.driver.get_screenshot_as_file('/Users/runehero/Desktop/test.png')
        print('screenshot')
        sleep(3)

    def test_click(self):
        self.driver.find_element_by_accessibility_id('Accessibility').click()
        sleep(3)
        self.driver.find_element_by_accessibility_id('Custom View').click()
        sleep(3)
        self.driver.get_screenshot_as_file('/Users/runehero/Desktop/test2.png')
        self.driver.press_keycode(4)
        sleep(2)
        self.driver.press_keycode(4)
        sleep(4)

    # def test_find_elements(self):
    #     el = self.driver.find_element_by_accessibility_id('Graphics')
    #     el.click()
    #     el = self.driver.find_element_by_accessibility_id('Arcs')
    #     self.assertIsNotNone(el)
    #     sleep(3)
    #
    #     self.driver.back()
    #     sleep(3)
    #
    #     el = self.driver.find_element_by_accessibility_id("App")
    #     self.assertIsNotNone(el)
    #     sleep(3)
    #
    #     els = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
    #     print(els)
    #     self.assertGreaterEqual(12, len(els))
    #     sleep(3)
    #
    #     self.driver.find_element_by_android_uiautomator('text("API Demos")')
    #     sleep(3)

    # def test_simple_actions(self):
    #     el = self.driver.find_element_by_accessibility_id('Graphics')
    #     el.click()
    #     sleep(3)
    #
    #     el = self.driver.find_element_by_accessibility_id('Arcs')
    #     el.click()
    #
    #     self.driver.find_element_by_android_uiautomator('new UiSelector().text("Graphics/Arcs")')
    #     sleep(3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
