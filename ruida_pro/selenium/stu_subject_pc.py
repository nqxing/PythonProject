from selenium import webdriver
import time
def login(driver,id):
    driver.find_element_by_name("userName").send_keys(id)
    driver.find_element_by_name("userPwd").send_keys("IQ0591@Fz")
    driver.find_element_by_id("loginBtn").click()
def xk(driver, sub):
    userName = driver.find_element_by_id("userName").text
    if len(userName) != 0:
        driver.get('https://www.tianwayun.com/saas/#/stu/course')
        time.sleep(2)
        buttons = driver.find_elements_by_xpath("//*/h2[text()='2018-2019学年下学期高一新高考正式选科']/../div[@class='button-box']/button")
        buttons[0].click()
        time.sleep(1)
        driver.find_element_by_xpath("//*/i[@class='close-icon']").click()
        subs = sub.split(',')
        for s in subs:
            driver.find_element_by_xpath("//*/h3[text()='{}']/..".format(s)).click()
        driver.find_element_by_xpath("//*/button[contains(text(), '提交')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*/button[contains(text(), '确定')]").click()
        time.sleep(5)
        try:
            divs = driver.find_elements_by_xpath("//*/button[contains(text(), '我知道了')]/../../div")
            print('{}选了{}，{}'.format(userName, sub, divs[1].text))
            # msg = driver.find_element_by_xpath("//*/{}/p".format(divs[1])).text
            # print(msg)
            divs[2].click()
        except:
            print('选科失败')
        driver.get('https://www.tianwayun.com/apps/desktop/index.html')
        time.sleep(3)
        driver.find_element_by_id("userName").click()
        time.sleep(1)
        driver.find_element_by_id("logout").click()
        time.sleep(2)
    else:
        print('登录失败!')
def main():
    sub_list = ['历史,地理,化学','历史,地理,生物','历史,地理,政治','历史,化学,生物','历史,化学,政治','历史,生物,政治','地理,化学,物理','地理,生物,物理','地理,物理,政治','化学,生物,物理','化学,物理,政治','生物,物理,政治']
    num = 0
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.maximize_window()  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('https://www.tianwayun.com/apps/desktop/index.html')
    for id in open("defineDef\\id.txt"):
        login(driver, id.strip())
        time.sleep(3)
        xk(driver, sub_list[num])
        num += 1
        if num == 12:
            num = 0
main()
