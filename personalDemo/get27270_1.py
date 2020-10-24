import requests
from bs4 import BeautifulSoup
import re
import os
import time
# 此程序抓取的图片不全
def main():
    max = 2
    for id in range(1,max+1):
        url(id)
def url(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    picUrlList = []
    index_url = 'https://www.27270.com{}'
    url = 'https://www.27270.com/ent/meinvtupian/list_11_%s.html'%id
    r = requests.get(url,headers=headers)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.content, 'lxml')
    ul = soup.find(class_='MeinvTuPianBox').find(name='ul')
    liList = ul.find_all(name='li')
    for li in liList:
        alink = li.find(name='a')['href']
        picUrlList.append(index_url.format(alink))
    picUrl(picUrlList)
def picUrl(picUrlList):
    sImgUrl = 'https://t1.hddhhn.com/uploads/tu/{}/{}/{}'
    # picUrlList = ['https://www.27270.com/ent/meinvtupian/2019/313891.html', 'https://www.27270.com/ent/meinvtupian/2019/313890.html']
    for pUrl in picUrlList:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        r = requests.get(pUrl, headers=headers)
        if r.status_code == 200:
            r.encoding = 'gb2312'
            soup = BeautifulSoup(r.content, 'lxml')
            srcList = soup.find(id='picBody').select('p a img')
            if srcList:
                pageInfo = int(soup.find(id='pageinfo')['pageinfo'])
                # 获取图片专辑名字
                picName = srcList[0]['alt']
                # 获取该图集第一张图片地址
                picUrl = srcList[0]['src']
                img_path = "D:/meinvtupian/%s"%picName
                folder = os.path.exists(img_path)
                if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
                # 判断该图集第一张图片地址是否是该类型地址
                if 'https://t1.hddhhn.com/uploads/tu' in picUrl:
                    # 切割图片地址 切割后为['https:', '', 't1.hddhhn.com', 'uploads', 'tu', '201901', '281', '1.jpg']或['https:', '', 't1.hddhhn.com', 'uploads', 'tu', '201901', '279', 'KL-WR-H01.jpg']
                    turl = picUrl.split('/')
                    # 匹配切割后的最后一个值中的数字
                    num = re.findall('\d+', turl[-1])
                    # 再根据数字切割一次 如 ['', '.jpg']或['KL-WR-H', '.jpg']
                    sstr = turl[-1].split(num[0])
                    # 构造图集下所有图片地址
                    imgUrlList = []
                    for i in range(pageInfo):
                        # 判断图片后缀地址为 01.jpg 类型的 大于9之后去掉前面0
                        if num[0][0] == '0' and sstr[0] == '':
                            # 把01按0为切割 得到为['','1']
                            n = num[0].split('0')
                            if (int(n[-1])+i)<10:
                                jpg = '0{}{}'.format(int(n[-1])+i, sstr[-1])
                                imgUrlList.append(sImgUrl.format(turl[-3], turl[-2], jpg))
                            else:
                                jpg = '{}{}'.format(int(n[-1])+i, sstr[-1])
                                imgUrlList.append(sImgUrl.format(turl[-3], turl[-2], jpg))
                        # 判断图片后缀地址为 KL-WR-H01.jpg 类型的 大于9之后去掉前面0
                        elif sstr[0] != '' and num[0][0] == '0':
                            n = num[0].split('0')
                            if (int(n[-1])+i)<10:
                                jpg = '{}0{}{}'.format(sstr[0],int(n[-1])+i, sstr[-1])
                                imgUrlList.append(sImgUrl.format(turl[-3], turl[-2], jpg))
                            else:
                                jpg = '{}{}{}'.format(sstr[0],int(n[-1])+i, sstr[-1])
                                imgUrlList.append(sImgUrl.format(turl[-3], turl[-2], jpg))
                        # 判断图片后缀地址为 1.jpg 类型的 这种应该是占大多数情况也是最简单的
                        else:
                            jpg = '{}{}'.format(i+int(num[0]),sstr[-1])
                            imgUrlList.append(sImgUrl.format(turl[-3],turl[-2],jpg))
                    print(imgUrlList)
                    for m in range(len(imgUrlList)):
                        img = requests.get(imgUrlList[m], headers=headers)
                        if img.status_code == 200:
                            with open(img_path + '/' + str(m+1) + ".jpg", "wb") as f:
                                f.write(img.content)
                            # time.sleep(0.5)
                    # print(turl)
                    # print(num)
                    # print(sstr)
                    # print(picName,picUrl)
main()