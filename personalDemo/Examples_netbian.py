import urllib.request
import re
import os

id = 1
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("创建新文件夹")

        print("创建成功")
    else:
        print("该文件夹已经存在")


img_path = "D:/photo/"
mkdir(img_path)

for index in range(2,8):
    url = r'http://www.netbian.com/meinv/index_%d.htm' % index

    page = urllib.request.urlopen(url).read()  # 获取到该地址的所有内容
    page = page.decode('gbk')  # 转码

    zz = r'<li><a href="/desk/(.+?).htm" title="(.+?)" target="_blank">.+?</a>.+?</li>'
    html = re.findall(zz,page,re.S)#re.S表示.可以代表\n
    for a in html:
        a1 = a[0]
        a2 = a[1]
        url1 = r'http://www.netbian.com/desk/%s-1920x1080.htm' % a1
        page1 = urllib.request.urlopen(url1).read()  # 获取到该地址的所有内容
        page1 = page1.decode('gbk')  # 转码
        zz1 = r'<table id="endimg" width=".+?">(.+?)</table>'
        #zz1 = r'<img src="(.+?)" title=".+?" alt=".+?">'
        zz2 = r'<a href="(.+?)" title=".+?">.+?</a>'
        html1 = re.findall(zz1, page1, re.S)  # re.S表示.可以代表\n
        for b in html1:
            html2 = re.findall(zz2, b, re.S)
            # 下载图片放到D:/photo/文件夹里面
            web = urllib.request.urlopen(html2[0])
            print('web = ',web)
            data = web.read()
            f = open(img_path + a2 + ".jpg", "wb")
            f.write(data)
            f.close()
            print('已成功下载%d张~'% id)
            id+=1