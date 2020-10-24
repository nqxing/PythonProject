from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui as pg
import time
import sqlite3

def get_cookie(oped_id, mobile):
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"')
    browser = webdriver.Chrome(chrome_options=options)
    browser.maximize_window()
    url = "https://tb.ele.me/wow/msite/act/login?redirect=https%3A%2F%2Fh5.ele.me%2Fprofile%2F"
    browser.get(url)
    print(browser.title)
    if browser.title != "手机号登录1":
        browser.refresh()  # 采用此方法刷新页面
        print("清除成功")
    iframe= browser.find_element_by_id("alibaba-login-box")
    browser.switch_to.frame(iframe)
    browser.find_element_by_id("fm-sms-login-id").send_keys(mobile)
    time.sleep(1500)
    browser.find_element_by_xpath("//*/a[text()='获取验证码']").click()
    try:
        locator = (By.ID, "nc_1_n1t")
        WebDriverWait(browser, 6).until(EC.presence_of_element_located(locator))
        print('需要滑动验证码')
    except:
        print('非滑动验证码验证')

    # pg.click(648, 1057)
    # time.sleep(1)
    pg.moveTo(210,558, 2)
    pg.mouseDown()
    for i in range(210, 1825, 161):
        pg.moveTo(i, 558, duration=0.1)
        # pg.dragTo(i, 558, button='left')
    pg.mouseUp()
    # time.sleep(1)
    time.sleep(1500)
    code_str = browser.find_elements_by_css_selector(".send-btn")[0].text
    if "重发" in code_str:
        print('验证码发送成功')
        conn = sqlite3.connect(r'code.db')
        # 创建一个游标 curson
        cursor = conn.cursor()
        # cursor.execute(
        #     '''select * from code WHERE open_id = '{}' '''.format(oped_id))  # 查找饿了么库里的账号表，目前只取第一个账号
        # values = cursor.fetchall()
        for i in range(300):
            cursor.execute(
                '''select sms_code from code WHERE open_id = '{}' '''.format(oped_id))  # 查找饿了么库里的账号表，目前只取第一个账号
            values = cursor.fetchall()
            if values[0][0] != 0:
                browser.find_element_by_id("fm-smscode").send_keys(values[0][0])
                time.sleep(1.5)
                browser.find_element_by_xpath("//*/button[text()='同意协议并登录']").click()
                time.sleep(5)
                cookies = browser.get_cookies()
                for c in cookies:
                    pass

                time.sleep(1500)
                break
            time.sleep(1)
    else:
        print(code_str)

get_cookie("test", "15659020901")
