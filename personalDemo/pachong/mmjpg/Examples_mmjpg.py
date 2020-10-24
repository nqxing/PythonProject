import requests
import re
import os
import time
import sys
from bs4 import BeautifulSoup

def get_li(url):
    try:
        html = requests.get(url)
        if html.status_code == 200:
            html.encoding = 'utf-8'
            html = html.text
            soup = BeautifulSoup(html, 'lxml')
            # page = soup.find(class_='ch')
            nextpage = soup.select('.ch')
            nextpage = nextpage[-1]['href']
            zz = re.compile('<li>(.*?)</li>',re.S)
            li = re.findall(zz,html)
            get_url(li)
            return nextpage
    except Exception as e:
        r = requests.get(url)
        print("%s - 该链接解析失败~~ %s" % (r.status_code, url))
        print(e)
def get_url(li):
    for l in li:
        soup = BeautifulSoup(l, 'lxml')
        url = soup.a['href']
        title = soup.span.string
        matching_url(url,title)
def matching_url(url,title):
    html = requests.get(url)
    html = html.text
    soup = BeautifulSoup(html, 'lxml')
    pagemax = soup.select('#page a')
    sum = int(pagemax[-2].string)
    img_path = "D:/mmjpg/%s(%s)" % (title,sum)
    folder = os.path.exists(img_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    for i in range(1,sum+1):
        try:
            li_url = '%s/%s' % (url,i)
            html = requests.get(li_url)
            if html.status_code == 200:
                html.encoding = 'utf-8'
                html = html.text
                soup = BeautifulSoup(html,'lxml')
                content = soup.find(id='content')
                img_url = content.img['src']
                img_name = content.img['alt']
                sava_img(img_url,img_name,img_path,url)
                li_url = ''
                sys.stdout.write('\r')
                sys.stdout.write('%s - 正在下载%s %s/%s' % (title,int(i % 6) * '.', i, sum))
                sys.stdout.flush()
                time.sleep(0.5)
        except Exception as e:
            r = requests.get(url)
            print("%s - 该链接解析失败~~ %s" %(r.status_code,url))
            print(e)
    sys.stdout.write('\n')
def sava_img(img_url,img_name,img_path,url):
    headers = {
        'Referer':url,
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
    }
    img = requests.get(img_url,headers=headers)
    with open(img_path + '/' + img_name + ".jpg", "wb") as f:
        f.write(img.content)
def input_page():
    page = input("请输入您要抓取的页数: ")
    try:
        return int(page)
    except Exception:
        print('您输入的不是数字，请重新输入~~')
        return input_page()
def main():
    url = 'http://www.mmjpg.com'
    page = input_page()
    print('程序正在执行~~')
    starttime = int(time.time())
    for i in range(page):
        sys.stdout.write('\r')
        sys.stdout.write('当前任务进度 %s/%s' % (i+1, page))
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\n')
        nextpage = get_li(url)
        url = 'http://www.mmjpg.com%s'% nextpage
        print('第%s页任务抓取完毕~~' % (i+1))
    runtime = int(time.time()-starttime)
    print('程序执行完毕,共运行%s时%s分%s秒~~ 图片保存路径为:D:/mmjpg/'%(int(runtime/3600),int(int(runtime%3600)/60),int(runtime%3600)%60))
if __name__ == '__main__':
    main()
