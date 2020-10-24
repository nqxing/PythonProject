import requests
from bs4 import BeautifulSoup
import os
def main():
    max = input_page()
    print('程序开始执行~~')
    for id in range(1,max+1):
        url(id)
    print('程序执行完毕~~')
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
    picUrl(picUrlList,id)
def picUrl(picUrlList,id):
    # picUrlList = ['https://www.27270.com/ent/meinvtupian/2019/313891.html', 'https://www.27270.com/ent/meinvtupian/2019/313890.html']
    for i in range(len(picUrlList)):
        print('正在爬取第{}页图集（{}/{}）..'.format(id,i+1,len(picUrlList)))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        imgUrlList = []
        r = requests.get(picUrlList[i], headers=headers)
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
                imgUrlList.append(picUrl)
                urlStr = picUrlList[i].split('.')
                for p in range(2,pageInfo+1):
                    newUrl = '{}.{}.{}_{}.{}'.format(urlStr[0],urlStr[1],urlStr[2],p,urlStr[3])
                    r1 = requests.get(newUrl, headers=headers)
                    if r1.status_code == 200:
                        r1.encoding = 'gb2312'
                        soup = BeautifulSoup(r1.content, 'lxml')
                        srcList = soup.find(id='picBody').select('p a img')
                        if srcList:
                            # 获取该图集图片地址
                            picUrl = srcList[0]['src']
                            imgUrlList.append(picUrl)
                for m in range(len(imgUrlList)):
                    img = requests.get(imgUrlList[m], headers=headers)
                    if img.status_code == 200:
                        with open(img_path + '/' + str(m + 1) + ".jpg", "wb") as f:
                            f.write(img.content)
def input_page():
    page = input("请输入您本次要抓取的总页数: ")
    try:
        return int(page)
    except Exception:
        print('您输入的不是数字，请重新输入~~')
        return input_page()
main()