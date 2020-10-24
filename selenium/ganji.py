from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://fz.ganji.com/")

h = driver.current_window_handle

print(h)  # 打印首页句柄

driver.find_element_by_link_text("福州招聘").click()

all_h = driver.window_handles

print(all_h)     # 打印所有的句柄
driver.switch_to.window(all_h[1])
print(driver.title)
time.sleep(5)
#将页面滚动条拖到底部  
js="var q=document.documentElement.scrollTop=100000"  
driver.execute_script(js)  
time.sleep(3)  
#将滚动条移动到页面的顶部  
js="var q=document.documentElement.scrollTop=0"  
driver.execute_script(js)  
time.sleep(3)  
#将页面滚动条移动到页面任意位置，改变等于号后的数值即可  
js="var q=document.documentElement.scrollTop=50"  
driver.execute_script(js)  
a = driver.current_window_handle
print(a)
driver.quit()