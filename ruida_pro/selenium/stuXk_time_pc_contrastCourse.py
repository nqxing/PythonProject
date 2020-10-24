from selenium import webdriver
from IQ.selenium.defineDef.iq_getTimeTaskCourseList_test import *
from bs4 import BeautifulSoup
import time
# 多学校测试服 获取选课任务可选的所有行政班，再根据行政班列出所有可选课程
# 再从页面获取加载出的课程对比接口返回的课程
def login(driver,id):
    driver.find_element_by_name("userName").send_keys(id)
    driver.find_element_by_name("userPwd").send_keys("IQ0591@Fz")
    driver.find_element_by_id("loginBtn").click()
def xk(driver):
    userName = driver.find_element_by_id("userName").text
    if len(userName) != 0:
        driver.find_element_by_xpath("//*/li[@data-name='学生选课']").click()
        time.sleep(3.5)
        driver.switch_to.frame(1)
        html = driver.page_source
        driver.switch_to.default_content()
        return html
    else:
        print('登录失败!')
def main():
    driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
    driver.maximize_window()  # 最大化浏览器窗口
    driver.implicitly_wait(8)  # 设置隐式时间等待
    driver.get('http://web-test.591iq.com.cn/apps/course/index.html')
    # 从接口获取所有班级可见课程数
    coueseDit = get_course()
    for data in open("definedef\\id.txt",encoding='utf-8'):
        userList = data.strip().split(',')
        id = userList[0]
        className = userList[1]
        login(driver,id)
        time.sleep(3)
        html = xk(driver)
        soup = BeautifulSoup(html, 'lxml')
        tbody = soup.find_all('tbody')
        courseNameList = []
        # 从页面获取该账号可见课程数
        for t in tbody:
            trList = t.find_all('tr')
            for tr in trList:
                courseName = tr.find_all('td')[1].get_text()
                courseNameList.append(courseName)
        # 对比接口获取中有而页面中没有的课程
        a = list(set(coueseDit[className]).difference(set(courseNameList)))
        # 对比页面中有而接口获取中没有的课程
        b = list(set(courseNameList).difference(set(coueseDit[className])))
        # 两次对比都是空，则判定为两边课程一样，该班级行政班课程可见正常
        if len(a) == 0 and len(b) == 0:
            print('{},{},可见课程对比正常'.format(id,className))
        else:
            print('{},{},对比异常,接口可见（{}）,页面可见（{}）'.format(id, className,coueseDit[className],courseNameList))
        driver.find_element_by_id("userName").click()
        time.sleep(2)
        driver.find_element_by_id("logout").click()
        time.sleep(2)
main()
