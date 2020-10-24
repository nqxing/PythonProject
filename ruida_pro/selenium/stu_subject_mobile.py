from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
def login(driver,id):
    driver.find_element_by_xpath("//*/input[@placeholder='用户名']").send_keys(id)
    driver.find_element_by_xpath("//*/input[@placeholder='密码']").send_keys("IQ0591@Fz")
    driver.find_element_by_xpath("//*/a[text()='登录']").click()
def xk(driver, id, sub):
    # wait = WebDriverWait(driver, 10)
    driver.get('https://wechat.591iq.cn/#/course/seleteSubject?tabId=4')
    time.sleep(2)
    buttons = driver.find_elements_by_xpath("//*/div[text()='2018-2019学年下学期高一新高考正式选科']/../div")
    buttons[5].find_element_by_xpath("//*/div[contains(text(), '去选科')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*/span[text()='选科公告']/../../img").click()
    time.sleep(2)
    subs = sub.split(',')
    for s in subs:
        driver.find_element_by_xpath("//*/div[text()='{}']/../..".format(s)).click()
    time.sleep(2)
    driver.find_element_by_xpath("//*/div[text()='提交']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    # html = driver.page_source
    # print(html)
    # print('--------------------------------------------------------')
    try:
        locator = (By.XPATH, "//*/p[text()='操作成功']")
        WebDriverWait(driver, 6).until(EC.presence_of_element_located(locator))
        print(id, sub, '选科成功')
    except:
        print(id, sub, '选科失败')
    time.sleep(1)
    driver.get('https://wechat.591iq.cn/#/ihome/mine?tabId=4')
    time.sleep(2)
    driver.find_element_by_xpath("//*/a[text()='退出']").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    time.sleep(2)
def main():
    sub_list = ['历史,地理,化学','历史,地理,生物','历史,地理,政治','历史,化学,生物','历史,化学,政治','历史,生物,政治','地理,化学,物理','地理,生物,物理','地理,物理,政治','化学,生物,物理','化学,物理,政治','生物,物理,政治']
    num = 0
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.set_window_size(350, 850)  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('https://wechat.591iq.cn/#/login')
    for id in open("defineDef\\id.txt"):
        login(driver, id.strip())
        time.sleep(3)
        xk(driver, id.strip(), sub_list[num])
        num += 1
        if num == 12:
            num = 0
main()