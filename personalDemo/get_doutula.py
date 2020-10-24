import requests
from pyquery import PyQuery as pq
import os
import hashlib
import sys
class doutula():
    def __init__(self):
        self.img_path = "D:/表情包/"
        folder = os.path.exists(self.img_path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
        }
    def get_imgUrl(self,link,k):
        print('正在下载第{}页表情包~'.format(k+1))
        html = pq(requests.get(link,headers = self.headers).text)
        aList = pq(html('.page-content.text-center div'))('a').items()
        # print(aList)
        # print(type(aList))
        imgUrlList = []
        for a in aList:
            # print(a)
            if a('img').attr('data-original') != None:
                imgUrl = a('img').attr('data-original')
                imgUrlList.append(imgUrl)
            else:
                html = pq(requests.get(a.attr('href'), headers=self.headers).text)
                gifUrl = html('tbody tr:first-child td img').attr('src')
                imgUrlList.append(gifUrl)
        # print(imgUrlList)
        # print(len(imgUrlList))
        self.sava_img(imgUrlList)
    def sava_img(self,imgUrlList):
        for imgUrl in imgUrlList:
            imgName = hashlib.md5()
            imgName.update(imgUrl.encode('utf8'))
            imgName = imgName.hexdigest()
            if '.gif' in imgUrl:
                imgName = imgName + '.gif'
            elif '.png' in imgUrl:
                imgName = imgName + '.png'
            else:
                imgName = imgName + '.jpg'
            img = requests.get(imgUrl, headers=self.headers)
            if img.status_code == 200:
                with open(self.img_path + imgName, "wb") as f:
                    f.write(img.content)
            else:
                print('{},该图片下载失败~~'.format(imgUrl))
    def main(self):
        link = 'https://www.doutula.com/photo/list/'
        Linklist = ['{}'.format(link)]
        try:
            max = int(input('请输入要爬取的总页数：'))
            for i in range(2, max + 1):
                Linklist.append('{}?page={}'.format(link,i))
        except:
            print('出错了,请确认你输入的是数字~')
            sys.exit()
        for k in range(len(Linklist)):
            self.get_imgUrl(Linklist[k],k)
        print('程序执行完毕~')
d = doutula()
d.main()