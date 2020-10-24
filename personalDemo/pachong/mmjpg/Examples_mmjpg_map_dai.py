import requests
import re
import os
import time
import sys
from bs4 import BeautifulSoup
import threadpool
proxy = '121.69.105.238:50956'
# proxy = '106.56.102.192:8070'
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy
}

def get_li(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        html = requests.get(url,proxies=proxies,headers=headers)
        if html.status_code == 200:
            html.encoding = 'utf-8'
            html = html.text
            # page = soup.find(class_='ch')
            zz = re.compile('<li>(.*?)</li>',re.S)
            li = re.findall(zz,html)
            get_url(li)
    except Exception as e:
        r = requests.get(url)
        print("%s - 该页链接解析失败~~ %s" % (r.status_code, url))
        print(e)
def get_url(li):
    urls = []
    titles = []
    for l in li:
        soup = BeautifulSoup(l, 'lxml')
        url = soup.a['href']
        urls.append(url)
        title = soup.span.string
        titles.append(title)
    data = [((url1, title1), None) for (url1, title1) in zip(urls, titles)]  # (index,i)也可以写成[index,i]
    pool = threadpool.ThreadPool(15)
    requests = threadpool.makeRequests(matching_url, data)
    [pool.putRequest(req) for req in requests]
    pool.wait()
def matching_url(url,title):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    html = requests.get(url,proxies=proxies,headers=headers)
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
            html = requests.get(li_url,proxies=proxies,headers=headers)
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
                sys.stdout.write('%s - 正在下载... %s/%s' % (title, i, sum))
                sys.stdout.flush()
                time.sleep(0)
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
    img = requests.get(img_url,headers=headers,proxies=proxies)
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
    page = input_page()
    print('程序正在执行~~')
    urls = ['http://www.mmjpg.com']
    for i in range(2,page+1):
        newpage = 'http://www.mmjpg.com/home/' + str(i)
        urls.append(newpage)
    starttime = int(time.time())
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(get_li, urls)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    runtime = int(time.time()-starttime)
    print('程序执行完毕,共运行%s时%s分%s秒~~ 图片保存路径为:D:/mmjpg/'%(int(runtime/3600),int(int(runtime%3600)/60),int(runtime%3600)%60))
if __name__ == '__main__':
    main()
