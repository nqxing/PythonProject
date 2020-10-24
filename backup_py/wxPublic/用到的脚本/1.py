import sqlite3
# conn = sqlite3.connect(r'keyword.db')
# 创建一个游标 curson
# cursor = conn.cursor()

# sql = """ CREATE TABLE keywords(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    text           varchar(255),
#    text_note       varchar(10000)
# ); """

# cursor.execute(sql)
# conn.commit()
# name = '万能直播'
# sss = """
# 【万能直播】下载地址：|百度网盘：<a href="https://pan.baidu.com/s/1agUb6R3WLxeutoGUHhBDMw">点我下载</a>  【提取码：g2dv】
# """
# cursor.execute(
#     "INSERT INTO keywords (text, text_note) VALUES ('{}', '{}')".format(name, sss.strip())
#         )
# conn.commit()

# cursor.execute("SELECT text_note FROM keywords WHERE text LIKE '%" + "{}".format(name) + "%'")
# results = cursor.fetchall()
# print(results[0][0])
from PIL import Image
import time
im = Image.open('1.png')
x, y = im.size
try:
    p = Image.new('RGBA', im.size, (18, 150, 219))
    p.paste(im, (0, 0, x, y), im)
    p.save(r'{}_white.png'.format("1"))
except:
    pass
try:
    p = Image.new('RGBA', im.size, (19,34,122))
    p.paste(im, (0, 0, x, y), im)
    p.save(r'{}_blue.png'.format("1"))
except:
    pass
try:
    p = Image.new('RGBA', im.size, (212,35,122))
    p.paste(im, (0, 0, x, y), im)
    p.save(r'{}_red.png'.format("1"))
except:
    pass
# def short_url(urls):
#     import requests,re
#     url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=short_url&need_short_url=1&url={}"
#     try:
#         r = requests.get(url.format(urls))
#         if 'ok' in r.text and 'short_url' in r.text:
#             short_url = re.findall('"short_url" : "(.*?)"', r.text)[0]
#             return short_url
#         else:
#             return -1
#     except:
#         return -1
# print(short_url("http://122.51.67.37:81/dz_info.txt"))