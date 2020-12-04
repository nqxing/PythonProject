from django.test import TestCase

# Create your tests here.

import requests

dict = {
    "long":"http://game.gtimg.cn/images/yxzj/coming/v2/skins/image/20200119/47a6a19fbcfc69bd3da39e852ac17c27.jpg",
    "period":"长期"
}

r = requests.post("http://zuiqu.net/s/addShortUrl/", data=dict)
print(r.text)

# dict = {
#     "short":"http://127.0.0.1:8000/1"
# }
#
# r = requests.post("http://127.0.0.1:8000/restoreUrl/", data=dict)
# print(r.text)

