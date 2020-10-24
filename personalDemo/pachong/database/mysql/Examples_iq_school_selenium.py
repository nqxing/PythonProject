from selenium import webdriver
import time
from pyquery import PyQuery as pq
import re
from bs4 import BeautifulSoup
import pymysql
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# 启用PhantomJS无界面浏览
# driver = webdriver.PhantomJS()

# 启用谷歌无界面浏览
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

# driver = webdriver.Chrome()  # 打开chrome，如果没有安装chrome,换成webdriver.Firefox()
# driver.maximize_window()  # 最大化浏览器窗口
driver.implicitly_wait(8)  # 设置隐式时间等待

wait = WebDriverWait(driver, 10)  # 设置显式时间等待，最大等待时间为10秒

def login_admin():
    try:
        driver.get('http://sso.iqcedu.com/login?flag=forward')
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("userPwd").send_keys("beijing2018")
        driver.find_element_by_id("loginBtn").click()
        time.sleep(2)
        driver.get('http://base.iqcedu.com/student/student!initfun.do?initFunId=50277')
        # 判断总页数 id属性page-max 10秒内是否加载完成
        pagenum = wait.until(EC.presence_of_element_located((By.ID, 'page-max')))
        return pagenum.text
    except Exception as e:
        print("登录出错了，正在重试...")
        login_admin()
def matching_data():
    # 判断下一页按钮 id属性btnNextPage 10秒内是否加载完成
    nextpage = wait.until(EC.presence_of_element_located((By.ID, 'btnNextPage')))
    html = driver.page_source # 获取当前页面源码
    doc = pq(html) # 调用PyQuery库解析网页
    items = doc('#table-model-body')
    item = items.children().items() # 获取items 子节点 并以列表形返回
    zz = re.compile('<td>(.*?)</td>', re.S) # 正则表达式，re.S表示换行也能匹配
    for ite in item:
        soup = BeautifulSoup(str(ite), 'lxml') # 调用BeautifulSoup库规范每个节点源码
        st = re.findall(zz, str(soup)) # 正则匹配
        save_sql(st) # 匹配成功结果传入 sava_sql 方法
    nextpage.click() # 点击下一页
    time.sleep(1)
def save_sql(st):
    uid = st[0]
    stunum = st[3]
    classname = st[4]
    stuname = st[6]
    stuid = st[7]
    # 插入或更新数据，如果主键存在，则更新数据
    sql = 'INSERT INTO IQ_School_selenium(uid, stunum, classname,stuname,stuid) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE uid=%s, stunum=%s, classname=%s,stuname=%s,stuid=%s'
    try:
        cursor.execute(sql, (uid, stunum, classname, stuname, stuid) * 2)
        db.commit()
        print('已成功抓取%s条数据~~'% uid)
    except:
        db.rollback()
        db.close()
        print('数据写入失败~~')
def main():
    nextmax = login_admin()
    for i in range(0,int(nextmax)):
        matching_data()
    print('程序执行完毕~~')
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='mysql231798', port=3306, db='nqxing') # 连接数据库
    cursor = db.cursor()
    main()