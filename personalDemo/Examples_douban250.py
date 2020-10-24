import requests
from requests.exceptions import RequestException
import re
import json

def get_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None

def matching_html(html):
    zz = re.compile('<div class="item">.*?<em.*?>(.*?)</em>.*?src="(.*?)".*?class="hd">(.*?)</div>.*?bd.*?<p class="">(.*?)</p>.*?rating_num.*?">(.*?)</span>.*?<span>(.*?)</span>.*?inq">(.*?)</span>.*?</div>',re.S)
    items = re.findall(zz,html)
    for item in items:
        s = re.sub("<span.*?>|</span>","",item[2])
        s1 = re.sub("<a.*?>|</a>","",s)
        s2 = re.sub("\s","",s1)
        s3 = re.sub("&nbsp;","",s2)
        b = re.sub("&nbsp;|<br>", "", item[3])
        yield {
            "排名：" : item[0],
            "图片地址：": item[1],
            "片名：": s3,
            "演职详情：": b.strip(),
            "评分：": item[4],
            "评价人数：": item[5],
            "影片简介": item[6],
        }
def write_file(content):
    with open('douban_250.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
def main(i):
    url = 'https://movie.douban.com/top250?start=%d&filter=' % i
    html = get_url(url)
    for item in matching_html(html):
        print(item)
        write_file(item)

if __name__ == '__main__':
    for i in range(0,250,25):
        main(i)