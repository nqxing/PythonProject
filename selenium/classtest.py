# coding=utf-8
import time
from selenium import webdriver


class BaiduSearch(object):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    def open_baidu(self):
        self.driver.get("https://www.baidu.com")
        time.sleep(1)

    def test_search(self):
        self.driver.find_element_by_id('kw').send_keys("selenium")
        time.sleep(1)
        print(self.driver.title)
        try:
            assert 'selenium' in self.driver.title
            print ('Test pass.')

        except Exception as e:
            print ('Test fail.')
        

baidu = BaiduSearch()
baidu.open_baidu()
baidu.test_search()