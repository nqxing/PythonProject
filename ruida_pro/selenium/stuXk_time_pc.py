from selenium import webdriver
import time
def login(driver,id):
    driver.find_element_by_name("userName").send_keys(id)
    driver.find_element_by_name("userPwd").send_keys("IQ0591@Fz")
    driver.find_element_by_id("loginBtn").click()
def xk(driver):
    userName = driver.find_element_by_id("userName").text
    if len(userName) != 0:
        driver.find_element_by_xpath("//*/li[@data-name='学生选课']").click()
        time.sleep(3)
        driver.switch_to.frame(1)
        course = ['高二古希腊神话小说(1)班',]
        for c in course:
            driver.find_element_by_xpath("//*/input[@data-classname='{}']/../span".format(c)).click()
        driver.find_element_by_xpath("//*/button[text()='确定']").click()
        time.sleep(1)
        driver.switch_to.default_content()
        driver.find_element_by_xpath("//*/a[text()='确定']").click()
        time.sleep(5)
        xkResult = driver.find_element_by_xpath("//*/div[@id='selectCourseDialog']/div/p").text
        print('{},{}'.format(userName,xkResult))
        driver.find_element_by_xpath("//*/button[text()='确定']").click()
        driver.find_element_by_id("userName").click()
        time.sleep(2)
        driver.find_element_by_id("logout").click()
        time.sleep(2)
    else:
        print('登录失败!')
def main():
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.maximize_window()  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('http://web-test.591iq.com.cn/apps/course/index.html')
    for id in open("defineDef\\id.txt"):
        login(driver,id.strip())
        time.sleep(3)
        xk(driver)
main()
