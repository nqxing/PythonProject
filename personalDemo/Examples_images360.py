import requests
from urllib.parse import urlencode
import json
import os
id = 1
def url():
    data = {'ch': 'photography', 'listtype': 'new'}
    base_url = 'https://image.so.com/zj?'
    for page in range(1, 50):
        data['sn'] = page * 30
        params = urlencode(data)
        url = base_url + params
        r = requests.get(url,params).text
        result = json.loads(r)
        for image in result.get('list'):
            imgurl = image.get('qhimg_url')
            img_url(imgurl)
def img_url(imgurl):
    img_path = "D:/360images/"
    folder = os.path.exists(img_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    img_name = imgurl.split('/')[-1]
    r = requests.get(imgurl)
    global id
    with open(img_path + img_name + ".jpg", "wb") as f:
        f.write(r.content)
    print(id,': ',imgurl)
    id+=1
url()