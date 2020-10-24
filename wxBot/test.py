from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.get('http://www.baidu.com/')
# 打印标题
print(driver.title)
# 关闭浏览器
driver.quit()