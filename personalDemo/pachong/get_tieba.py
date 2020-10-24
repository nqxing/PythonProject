import requests
import re
import os
import hashlib
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
}
url = 'https://tieba.baidu.com/f?kw=%E8%A1%A8%E6%83%85%E5%8C%85&ie=utf-8&tab=good'
html = requests.get(url,headers=headers)
# print(html.text)
linkList = re.findall('<a rel="noreferrer" href="(.*?)" title=".*?" target="_blank" class="j_th_tit ">.*?</a>' , html.text)
pUrlList = []
img_path = "D:/贴吧表情包/"
folder = os.path.exists(img_path)
if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs(img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
for f in linkList:
    pUrlList.append('https://tieba.baidu.com{}'.format(f))
def get_tiezi(pUrlList):
    print('本次共找到{}个精品贴~'.format(len(pUrlList)))
    for p in range(len(pUrlList)):
        # uurl = 'https://tieba.baidu.com/p/5817136809'
        # uurl = 'https://tieba.baidu.com/p/5817136809?pn=3'
        uhtml = requests.get(pUrlList[p], headers=headers)
        imgurlList = re.findall('<img class="BDE_Image".*?src="(.*?)" .*?">', uhtml.text)
        pageMax = re.findall('回复贴，共<span class="red">(.*?)</span>页', uhtml.text)[0]
        print('正在下载第{}个帖子,共{}页回复~~'.format(p+1,pageMax))
        if len(imgurlList) != 0:
            sava_img(imgurlList)
        else:
            print('该页没有表情包~')
        for u in range(2,int(pageMax)+1):
            furl = '{}?pn={}'.format(pUrlList[p],u)
            fhtml = requests.get(furl, headers=headers)
            fimgurlList = re.findall('<img class="BDE_Image".*?src="(.*?)" .*?">', fhtml.text)
            if len(fimgurlList) != 0:
                sava_img(fimgurlList)
            else:
                print('该页没有表情包~')
def sava_img(imgurlList):
    for imgUrl in imgurlList:
        imgName = hashlib.md5()
        imgName.update(imgUrl.encode('utf8'))
        imgName = imgName.hexdigest()
        img = requests.get(imgUrl, headers=headers)
        with open(img_path  + "{}.jpg".format(imgName), "wb") as f:
            f.write(img.content)
get_tiezi(pUrlList)