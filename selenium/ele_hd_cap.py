from selenium import webdriver
from pymouse import PyMouse
import time
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import ActionChains

mobile = '17134025292'
options = webdriver.ChromeOptions()
# options.add_argument(
#     'user-agent="Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"')
browser = webdriver.Chrome(chrome_options=options)
browser.maximize_window()
url = "https://tb.ele.me/wow/msite/act/login?redirect=https%3A%2F%2Fh5.ele.me%2Fprofile%2F"
browser.get(url)
# print(browser.page_source)
iframe = browser.find_element_by_id("alibaba-login-box")
browser.switch_to.frame(iframe)
browser.find_element_by_id("fm-sms-login-id").send_keys(mobile)
time.sleep(1.5)
browser.find_element_by_xpath("//*/a[text()='获取验证码']").click()
time.sleep(2)
button = browser.find_element_by_id('nc_1_n1t')# 找到“蓝色滑块”

action = ActionChains(browser)

 #鼠标左键按下不放

m = PyMouse()
(x,y)=m.position()#获取当前坐标的位置
time.sleep(1)
m.move(x,y)#鼠标移动到xy位置
print(x,y)


# action = ActionChains(browser)
# action.click_and_hold(button).perform()# perform()用来执行ActionChains中存储的行为
# action.reset_actions()
# action.move_by_offset(1000, 0).perform()# 移动滑块
time.sleep(300)
# 模拟人工滑动验证
# pg.moveTo(210, 558, 1)
# pg.mouseDown()
# for i in range(210, 1825, 161):
#     pg.moveTo(i, 558, duration=0.1)
# pg.mouseUp()
# time.sleep(1)