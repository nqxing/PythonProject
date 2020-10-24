import requests
import re
from requests.exceptions import RequestException
import pymysql

def get_url(url):
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None


def matching_html(html):
    zz = re.compile('<ul class="excerpt" style=".*?">(.*?)</ul>',re.S)
    zz1 = re.compile('<h2><a href=".*?" target="_blank" title=".*?">(.*?)</a></h2>.*?time">(.*?)</span>.*?cat"><a.*?">(.*?)</a>.*?view">.*?<span>(.*?)</span>',re.S)
    h = re.findall(zz,html)
    for h1 in h:
        h2 = re.findall(zz1,h1)
        for str in h2:
            abc(str)

def abc(str):
    title = str[0]
    timedata = str[1]
    sort = str[2]
    hot = str[3]
    global id #设置全局变量
    # 插入或更新数据，如果主键存在，则更新数据
    sql = 'INSERT INTO zd423(id, title, timedata,sort,hot) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=%s, title=%s, timedata=%s,sort=%s,hot=%s'
    try:
        cursor.execute(sql, (id, title, timedata, sort, hot)*2)
        db.commit()
    except:
        db.rollback()
        db.close()
    id = id+1
def main(i):
    url = "http://www.zdfans.com/index_%d.html" % i
    html = get_url(url)
    matching_html(html)

if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='mysql231798', port=3306, db='spiders')
    cursor = db.cursor()
    id = 1
    for i in range(1,13):
        main(i)
    sql1 = ' SELECT * FROM zd423 WHERE hot >= 100000  '
    try:
        cursor.execute(sql1)
        print("人气大于10万的有：",cursor.rowcount)
        one = cursor.fetchone()
        while one:
            print('ID：%s，标题：%s，时间：%s，人气：%s' % (one[0],one[1],one[2],one[4]))
            one = cursor.fetchone()
    except:
        print("出错了！")


