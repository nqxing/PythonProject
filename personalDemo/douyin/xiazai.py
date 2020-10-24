import requests

url = 'http://qqadapt.qpic.cn/qqshare/0/0d19eeaa8096d1be9c5e62cd12170d4f/0'

img = requests.get(url)

print(img.status_code)

with open("1.png", "wb") as f:
    f.write(img.content)
# def get():
#     url = 'http://127.0.0.1:2222/api/douyin/parse?url=1233&name=nnn'
#     r = requests.get(url)
#     print(r.text)
#
# def post():
#     dict = {
#         'page' : 1,
#         'row' : 10
#     }
#     url = 'http://127.0.0.1:2222/test_1.0'
#     r = requests.post(url, data=dict)
#     print(r.text)
#
# # get()
# post()
# import json
# get_Data = 'age=122323&name=nnnnnn'
# get_Data = json.loads(get_Data)
# print(get_Data)