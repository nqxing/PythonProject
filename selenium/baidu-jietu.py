from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
time.sleep(3)
driver.get_screenshot_as_file('b1.png')
driver.quit()
