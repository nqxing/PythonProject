from selenium import webdriver
import time
# sss = {'domain': '.ele.me', 'httpOnly': False, 'name': 'snsInfo[101204453]', 'path': '/', 'secure': True, 'value': '%7B%22city%22%3A%22%E5%8E%A6%E9%97%A8%22%2C%22constellation%22%3A%22%22%2C%22eleme_key%22%3A%220ceb2557e771603ab407f9b618ffd284%22%2C%22figureurl%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F30%22%2C%22figureurl_1%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F50%22%2C%22figureurl_2%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F100%22%2C%22figureurl_qq%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D640%26t%3D1556538515%22%2C%22figureurl_qq_1%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D40%26t%3D1556538515%22%2C%22figureurl_qq_2%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D100%26t%3D1556538515%22%2C%22figureurl_type%22%3A%221%22%2C%22gender%22%3A%22%E5%A5%B3%22%2C%22gender_type%22%3A1%2C%22is_lost%22%3A0%2C%22is_yellow_vip%22%3A%220%22%2C%22is_yellow_year_vip%22%3A%220%22%2C%22level%22%3A%220%22%2C%22msg%22%3A%22%22%2C%22nickname%22%3A%22%E5%B0%91%E5%B9%B4%E6%A2%A6%E4%BB%96%E5%9F%8E%E3%80%81%22%2C%22openid%22%3A%22969C874F3DAFCBDE2E48EEA12E9A87D3%22%2C%22province%22%3A%22%E7%A6%8F%E5%BB%BA%22%2C%22ret%22%3A0%2C%22vip%22%3A%220%22%2C%22year%22%3A%221996%22%2C%22yellow_vip_level%22%3A%220%22%2C%22name%22%3A%22%E5%B0%91%E5%B9%B4%E6%A2%A6%E4%BB%96%E5%9F%8E%E3%80%81%22%2C%22avatar%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D40%26t%3D1556538515%22%7D'}

options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\ditto.he\AppData\Local\Google\Chrome\User Data')
# options.add_argument('disable-infobars')
# options.add_argument('--ignore-certificate-errors')
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
browser = webdriver.Chrome(chrome_options=options)
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"')

# time.sleep(3)
# options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"')
url = "https://tb.ele.me/wow/msite/act/login?redirect=https%3A%2F%2Fh5.ele.me%2Fprofile%2F"
browser.get(url)
# browser.add_cookie(sss)
time.sleep(3000)
browser.get(url)
# 通过js新打开一个窗口
# newwindow='window.open("https://h5.ele.me/hongbao/#is_lucky_group=true&device_id=&theme_id=569&sn=2a7a9095ea2a98bd.2&hardware_id=&platform=4&lucky_number=0");'
# # 删除原来的cookie
# browser.delete_all_cookies()
# # 携带cookie打开
# browser.add_cookie(sss)
# # 通过js新打开一个窗口
# browser.execute_script(newwindow)
# input("查看效果")
print('当前页面title',browser.title)
print('当前页面url',browser.current_url)
time.sleep(11)

# browser.refresh()
# browser.get(url)

browser.find_element_by_class_name("ps-login-phone").send_keys("15838229537")
time.sleep(2)
browser.find_element_by_xpath("//*/div[text()='获取验证码']").click()
time.sleep(3333)
print(111)