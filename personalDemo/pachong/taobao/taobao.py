from selenium import webdriver
import time
from pyquery import PyQuery as pq

def login(driver, user, pwd):
    driver.find_element_by_xpath("//*/a[text()='密码登录']").click()
    time.sleep(0.5)
    driver.find_element_by_id("TPL_username_1").send_keys(user)
    driver.find_element_by_id("TPL_password_1").send_keys(pwd)
    time.sleep(1)
    driver.find_element_by_id("J_SubmitStatic").click()
    time.sleep(8)
    driver.find_element_by_id("TPL_password_1").send_keys(pwd)
    time.sleep(1)
    driver.find_element_by_id("J_SubmitStatic").click()

def xk(driver, value):
    driver.get('https://s.taobao.com/search?q={}'.format(value))
    html = driver.page_source
    print(html)
    # html = requests.get(url, headers = headers)
    # html.encoding = 'gbk'
    items = pq(html)('.m-itemlist div div:nth-child(1) div').items()
    for item in items:
        print(item)

    time.sleep(5000)

def main():
    # driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()

    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)


    driver.maximize_window()  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F')
    time.sleep(1)
    login(driver, '15659020901', 'mm@541116212')
    time.sleep(2)
    xk(driver, '牛仔裤')
main()
