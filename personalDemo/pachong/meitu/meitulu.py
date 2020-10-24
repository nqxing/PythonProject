import requests
from pyquery import PyQuery as pq
import re
import pymysql
import time
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
}
db = pymysql.connect(host='106.13.81.161', user='root' , password='BKKPHbkkpn3v76y461yt8ncn0', port=3306, db='meitu') # 连接数据库
# db = pymysql.connect(host='localhost', user='root' , password='BKKPHbkkpn3v76y461yt8ncn0', port=3306, db='meitu') # 连接数据库
cursor = db.cursor()
# id = 11626
def index(page, url, classify):
    global id
    urls = [url]
    ppurl = 'https://mtl.ttsqgs.com/images/img/{}/{}.jpg'
    if page >= 2:
        for i in range(2, page+1):
            us = '{}{}.html'.format(url, i)
            urls.append(us)
    for ur in urls:
        html = requests.get(url=ur, headers=headers)
        html.encoding = 'utf-8'
        html = pq(html.text)
        uls = html('.img li').items()
        for u in uls:
            print(id)
            hurl = u('a').attr('href')
            bianhao = re.findall('\d+', hurl)[0]
            furl = u('a')('img').attr('src')
            num = int(re.findall('\d+', u('p:nth-child(2)').text())[0])
            jigou = u('p:nth-child(3) a').text()
            mote = u('p:nth-child(4)').text().replace('模特：', '').strip()
            tags = u('p:nth-child(5)').text().replace('标签：', '').strip()
            title = u('p:last-child').text()
            sql = 'INSERT INTO meitulu(id, title, num, jigou, mote, tags, furl, hurl, stime, classify) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                cursor.execute(sql, (id, title, num, jigou, mote, tags, furl, hurl, int(time.time()), classify))
                db.commit()
            except:
                print(1)
                db.rollback()
                db.close()
            for i in range(num):
                purl = ppurl.format(bianhao, i+1)
                sql = 'INSERT INTO meitulu_p(title, purl, pid) values(%s, %s, %s)'
                try:
                    cursor.execute(sql, (title, purl, id))
                    db.commit()
                except:
                    print(2)
                    db.rollback()
                    db.close()
            id += 1

def hurl():

    # sql = 'INSERT INTO meitulu_p(title, purl, pid) values(%s, %s, %s)'
    try:
        print(2)
        cursor.execute('alter table meitulu_p AUTO_INCREMENT = 1;')
        db.commit()
    except:
        print(1)
        db.rollback()
        db.close()

# uurls = [
#          'https://www.meitulu.com/t/baoru/', 'https://www.meitulu.com/t/xinggan/', 'https://www.meitulu.com/t/youhuo/', 'https://www.meitulu.com/t/meixiong/',
#          'https://www.meitulu.com/t/shaofu/', 'https://www.meitulu.com/t/changtui/', 'https://www.meitulu.com/t/mengmeizi/', 'https://www.meitulu.com/t/loli/', 'https://www.meitulu.com/t/keai/',
#          'https://www.meitulu.com/t/huwai/', 'https://www.meitulu.com/t/bijini/', 'https://www.meitulu.com/t/qingchun/', 'https://www.meitulu.com/t/weimei/', 'https://www.meitulu.com/t/qingxin/'
#          ]
# pages = [21, 67, 50, 37, 22, 34, 28, 12, 21, 22, 9, 23, 11, 25]
# classifys = ['爆乳', '性感', '诱惑', '美胸', '少妇', '长腿', '萌妹子', '萝莉', '可爱', '户外', '比基尼', '清纯', '唯美', '清新']
#
# for i in range(len(uurls)):
#     index(pages[i], uurls[i], classifys[i])
# hurl()

def get_classify():
    url = 'https://www.meitulu.com/'
    html = requests.get(url=url, headers=headers)
    html.encoding = 'utf-8'
    html = pq(html.text)
    uls = html('#tag_ul li a').items()
    id = 1
    for ul in uls:
        cname = ul.text()
        sqls = ''' select count(*) from meitulu WHERE classify = "{}" '''.format(cname)
        # sqlss = ''' select * from meitulu WHERE classify = "清新" '''
        cursor.execute(sqls)
        num = cursor.fetchall()[0][0]
        sqlss = ''' select * from meitulu WHERE classify = "{}" limit 1'''.format(cname)
        cursor.execute(sqlss)
        rs = cursor.fetchall()
        b_num = rs[0][0] + 180
        sql = 'INSERT INTO meitulu_f(cname, curl, beg_id, sta_id, sum_num) values(%s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql, (cname, 'http://pics.sc.chinaz.com/Files/pic/icons128/7408/d1.png', b_num, rs[0][0], num))
            db.commit()
        except:
            print(2)
            db.rollback()
            db.close()
        print(id)
        id += 1

get_classify()