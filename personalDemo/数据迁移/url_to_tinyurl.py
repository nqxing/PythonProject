import pymysql
import requests
nonce = "nonce_NOeZiXdbG8kRaxOk6sb9ELNM911CbtknYXkTSeck0qLqcn6YwqmJaQyI8"
def tinyurl(url):
    r = requests.get('http://tinyurl.com/api-create.php?url={}'.format(url)).text
    if 'tinyurl.com' in r:
        return r
    else:
        return -1

def tcn(url):
    r = requests.get('http://dwz.2xb.cn/t?url={}'.format(url)).json()
    if r['code'] == 200:
        return r['shortUrl']
    else:
        return -1

def slal(url):
    global nonce
    r = requests.get('https://sl.al/?url={}&nonce={}'.format(url, nonce)).json()
    print(r)
    if 'link' in r and 'nonce' in r:
        nonce = r['nonce']
        return r['link']['shortname']
    else:
        return -1

def wz():
    mysql_conn = pymysql.connect(host="122.51.67.37", user="root", password="mm123456", port=3306, db='public')
    # mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    mysql_cursor.execute("select * from pub_wz_wall")
    values = mysql_cursor.fetchall()
    for v in values:
        id = v[0]
        if v[2] != None:
            # r1 = tinyurl(v[2])
            # r1 = tcn(v[2])
            r1 = 'https://sl.al/{}'.format(slal(v[2]))
        else:
            r1 = -1
        if v[7] != None:
            # r2 = tinyurl(v[7])
            # r2 = tcn(v[7])
            r2 = 'https://sl.al/{}'.format(slal(v[7]))
        else:
            r2 = -1
        if r1 != -1 and r2 != -1:
            sql = "update pub_wz_wall set skin_short_url = '{}',mob_skin_short_url = '{}' where id = {}".format(r1, r2,
                                                                                                                id)
            mysql_cursor.execute(sql)
            mysql_conn.commit()
            # print('{}更新完毕'.format(id))
        else:
            print(v)

def lol():
    mysql_conn = pymysql.connect(host="122.51.67.37", user="root", password="mm123456", port=3306, db='public')
    # mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    mysql_cursor.execute("select * from pub_lol_wall")
    values = mysql_cursor.fetchall()
    for v in values:
        id = v[0]
        if v[2] != None:
            r1 = tinyurl(v[2])
        else:
            r1 = -1
        if r1 != -1:
            sql = "update pub_lol_wall set skin_short_url = '{}' where id = {}".format(r1, id)
            mysql_cursor.execute(sql)
            mysql_conn.commit()
            # print('{}更新完毕'.format(id))
        else:
            print(v)

# lol()
wz()