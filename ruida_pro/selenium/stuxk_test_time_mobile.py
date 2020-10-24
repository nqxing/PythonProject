from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# url = 'https://wechat.591iq.cn' # 正式环境
url = 'http://twweixin-test.591iq.com.cn' #测试环境
task_name = '2020renwu'
courses = ['高一课程1(1)班']

def login(driver,id):
    driver.find_element_by_xpath("//*/input[@placeholder='用户名']").send_keys(id)
    driver.find_element_by_xpath("//*/input[@placeholder='密码']").send_keys("IQ0591@Fz")
    driver.find_element_by_xpath("//*/a[text()='登录']").click()
def xk(driver, id):
    # wait = WebDriverWait(driver, 10)
    driver.get('{}/#/course/seleteSubject?tabId=4'.format(url))
    time.sleep(2)
    buttons = driver.find_elements_by_xpath("//*/div[text()='{}']/../../div".format(task_name))
    buttons[6].find_element_by_xpath("//*/div[contains(text(), '去选课')]").click()
    time.sleep(2)
    for c in courses:
        divs = driver.find_elements_by_xpath("//*/span[text()='班级：{}']/../../../div".format(c))
        divs[1].click()
    time.sleep(2)
    driver.find_element_by_xpath("//*/div[text()='提交']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    # time.sleep(5)
    # html = driver.page_source
    # print(html)
    # print('--------------------------------------------------------')
    try:
        locator = (By.XPATH, "//*/*[contains(text(), '选课成功')]")
        WebDriverWait(driver, 6).until(EC.presence_of_element_located(locator))
        print(id, '选课成功')
    except:
        print(id, '选课失败')
    time.sleep(1)
    driver.get('{}/#/ihome/mine?tabId=4'.format(url))
    time.sleep(2)
    driver.find_element_by_xpath("//*/a[text()='退出']").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//*/a[text()='确定']").click()
    time.sleep(2)
def main():
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.set_window_size(350, 850)  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('{}/#/login'.format(url))
    for id in open("defineDef\\id.txt"):
        login(driver, id.strip())
        time.sleep(3)
        xk(driver, id.strip())
main()