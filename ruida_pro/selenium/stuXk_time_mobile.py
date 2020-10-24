from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
def login(driver,id):
    driver.find_element_by_xpath("//*/input[@placeholder='用户名']").send_keys(id)
    driver.find_element_by_xpath("//*/input[@placeholder='密码']").send_keys("IQ0591@Fz")
    driver.find_element_by_xpath("//*/a[text()='登录']").click()
def xk(driver,id):
    # wait = WebDriverWait(driver, 10)
    driver.get('http://twweixin-test.591iq.com.cn/#/course/selete')
    time.sleep(3.5)
    lists = driver.find_elements_by_xpath("//*/span[text()='展开 ']")
    for l in lists:
        l.click()
    time.sleep(1)
    course = ['班级：高一小说阅读基础理论(1)班']
    # course = ['班级：高一健康人生美好未来(4)班','班级：高一美丽英文与英文金曲赏析(1)班']
    for c in course:
        driver.find_element_by_xpath("//*/p[text()='{}']/../../label".format(c)).click()
    time.sleep(1)
    driver.find_element_by_xpath("//*/a[text()='提交']").click()
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    # time.sleep(3)
    # html = driver.page_source
    # print(html)
    # print('--------------------------------------------------------')
    try:
        locator = (By.XPATH, "//*/p[text()='选课成功']")
        WebDriverWait(driver, 6).until(EC.presence_of_element_located(locator))
        print(id,'选课成功')
    except:
        print(id,'选课失败')
    time.sleep(1)
    driver.get('http://twweixin-test.591iq.com.cn/#/ihome/mine?tabId=4')
    time.sleep(2)
    driver.find_element_by_xpath("//*/a[text()='退出']").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    time.sleep(2)
def main():
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.set_window_size(420, 850)  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('http://twweixin-test.591iq.com.cn/#/login')
    for id in open("defineDef\\id.txt"):
        login(driver,id.strip())
        time.sleep(3)
        xk(driver,id.strip())
main()