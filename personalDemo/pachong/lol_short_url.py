import pymysql
import requests
from PIL import Image
from io import BytesIO
import time
from fake_useragent import UserAgent
import re
ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random
}
# 这个一天好像只能20个
# def get_wurl(urls):
#     url = "https://api.66mz8.com/api/short.php?dwz=urlcn&url={}".format(urls)
#     r = requests.get(url)
#     print(r.text)
#     if r.json()['code'] == 200:
#         return r.json()['url_short']
#     else:
#         print(r.text)
#         return -1

# def get_wurl(urls):
#     url = "https://api.302.pub/api/turl/?url={}".format(urls)
#     r = requests.get(url, headers=headers)
#     print(r.text)
#     if r.json()['code'] == 200:
#         return r.json()['content']
#     else:
#         print(r.text, urls)
#         return -1

def short_turl(urls):
    url = 'https://service.weibo.com/share/share.php?url={}&pic=pic&appkey=key&title={}'.format(urls, urls)
    r = requests.get(url)
    r.encoding = 'utf-8'
    if 'scope.short_url' in r.text:
        short_url = re.findall('scope.short_url = "(.*?)";', r.text, re.S)[0].strip()
        if len(short_url) == 0:
            return -1
        return short_url
    else:
        return -1

def get_size(urls):
    response = requests.get(urls)
    f = BytesIO(response.content)
    img = Image.open(f)
    return img.size
    # print(img.size)

# HOST = 'localhost'
HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'

mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db="public")
mysql_cursor = mysql_conn.cursor()  # 获取游标
sql = "select id,skin_url from pub_lol_wall"
mysql_cursor.execute(sql)
values = mysql_cursor.fetchall()
for v in values:
    if v[0] > 848:
        urls = v[1]
        skin_short_url = short_turl(urls)
        if skin_short_url != -1:
            skin_size = get_size(urls)
            print(v[0], skin_short_url, skin_size)
            sql1 = "update pub_lol_wall set skin_short_url = '{}',skin_size = '{}' where id = {}".format(skin_short_url, skin_size, v[0])
            mysql_cursor.execute(sql1)
            mysql_conn.commit()
        else:
            print(v[0])
            break
        # time.sleep(0.5)
    else:
        pass


