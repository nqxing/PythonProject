import requests
from config import *
# r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(AppID, AppSecret))
# print(r.text)
# token
t = '21_JJKjfD1Ysdb4agZlnZI-Am_uMVi9Pvohkqt9-a8jtSSog_jTNe1UjOCFDcAKnjoat3Lniz1ux7Sn0EP-a-zvq6j20O8Qv7rJIhqNth1MSKg8VMTIdFU8JE4syTtRwwSeuvckAc0DBT5Mf6_DFOKjAEAVEA'
# d = {
#     "touser":"oBYPr5nZOIceef0pN-BFtlMrfm7w",
#     "msgtype":"text",
#     "text":
#     {
#          "content":"Hello World"
#     }
# }

r = requests.get('https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={}'.format(t),)
print(r.text)
print(r.status_code)