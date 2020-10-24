import requests
from bs4 import BeautifulSoup
import sqlite3
from pyquery import PyQuery as pq
import re
import datetime
from rili.get_rili import get_rili
def getYear():
    yearDic = {}
    week = 3 # 初始星期，2019年1月1日为星期二
    year = 2020 # 年份
    urlList = []
    uUrl = 'https://wannianrili.51240.com/ajax/?q={}-{}&v=18121803'
    # 构造每个月的接口链接
    for y in range(1,13):
        if y<10:
            rUrl = uUrl.format(year,'0'+str(y))
            urlList.append(rUrl)
        else:
            rUrl = uUrl.format(year,y)
            urlList.append(rUrl)
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    for i in range(0,len(urlList)):
        monthDic = {}
        html = requests.get(urlList[i], headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        riqiList = soup.find_all(class_='wnrl_riqi')
        for riqi in riqiList:
            dayList = []
            g = riqi.find_all(class_='wnrl_td_gl')
            n = riqi.find_all(class_='wnrl_td_bzl')
            gStr = g[0].get_text()
            nStr = n[0].get_text()
            # 找到该元素视为法定节假日
            # if riqi.find_all(class_='wnrl_riqi_xiu'):
            #     nStr+='(休)'
            dayList.append(week)
            # 到星期日后重置为0
            if week == 7:
                week = 0
            week+=1
            dayList.append(gStr)
            dayList.append(nStr)
            monthDic[gStr] = dayList
        yearDic[i+1] = monthDic
    return yearDic,year
def sava_db():
    jiri_str = '元旦春节妇女节清明节五一劳动节端午节中秋节国庆节'
    conn = sqlite3.connect(r'rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    yearDic, year = getYear()
    for i in range(1, 13):
        daykeyList = list(yearDic[i].keys())
        for k in range(len(daykeyList)):  # 每个月的日期
            dayList = yearDic[i][daykeyList[k]]  # 获取每日的列表值['2','01','元旦']  第一个值为星期几，第二个为日期，第三个为农历或节假日
            if i < 10:
                month = '0{}'.format(i)
            else:
                month = i
            date_id = '{}{}{}'.format(year, month, dayList[1])
            date_str = '{}年{}月{}日'.format(year, month, dayList[1])
            if dayList[2] in jiri_str:
                is_jishi = 'yes'
            else:
                is_jishi = 'no'
            cursor.execute(
                "INSERT INTO rilibiao (date_id, date_str, week, holiday, is_jishi) VALUES ('{}', '{}', '{}', '{}', '{}')".format(date_id, date_str, dayList[0], dayList[2],
                                                                                                               is_jishi))
            conn.commit()
def sava_yuju():
    conn = sqlite3.connect(r'D:\wxBot\rili\rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    num = 423
    week = 4
    i = 0
    f = open(r"wangyiyun.txt", "r", encoding='UTF-8')
    lines = f.readlines()  # 读取全部内容
    while True:
    #    for id in open("wangyiyun.txt", encoding='UTF-8'):
        if week == 6 or week == 7:
            cursor.execute("UPDATE rilibiao SET yuju = '周末' where id = {}".format(num))
            conn.commit()
        else:
            id = lines[i].strip().replace(' ', '')
            id = id.replace("'", '')
            # id = id.replace("|", '——来自网易云热评')
            cursor.execute("UPDATE rilibiao SET yuju = '{}' where id = {}".format(id.strip(), num))
            conn.commit()
            i += 1
            print(i)
        if week == 7:
            week = 1
        else:
            week += 1
        # conn.commit()
        num += 1
        if len(lines) == i:
            break
def lishi_jt():
    conn = sqlite3.connect(r'D:\Eleme\rili\rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    def get_data(cursor, month, day):
        lishi_list = []
        url = 'http://www.lssdjt.com/{}/{}/'.format(month, day)
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        }
        html = requests.get(url, headers = headers)
        html.encoding = 'UTF-8'
        html = pq(html.text)
        aList = pq(html('.main .list'))('li').items()
        for a in aList:
            text = a.text().replace(' ', '|')
            lishi_list.append(text)
        lishi_str = '#'.join(lishi_list)
        if month < 10:
            month = '0{}'.format(month)
        else:
            month = '{}'.format(month)
        if day < 10:
            day = '0{}'.format(day)
        else:
            day = '{}'.format(day)
        print(lishi_str)
        # try:
        #     cursor.execute(
        #         "INSERT INTO lishi_jt (date_id, date_str) VALUES ('{}', '{}')".format(
        #             month + day, lishi_str))
        #     conn.commit()
        # except:
        #     print('Err {}'.format(month + day))
    # for m in range(1, 13):
    #     if m in (1, 3, 5, 7, 8, 10, 12):
    #         for d in range(1, 32):
    #             get_data(cursor, m, d)
    #     elif m == 2:
    #         for d in range(1, 29):
    #             get_data(cursor, m, d)
    #     elif m in (4, 6, 9, 11):
    #         for d in range(1, 31):
    #             get_data(cursor, m, d)
    get_data(cursor, 7, 22)
def replace_str():
    f = open(r"wangyiyun.txt", "r", encoding='UTF-8')
    lines = f.readlines()  # 读取全部内容
    stt = lines[0]
    for i in range(101, 1, -1):
        stt = stt.replace("{}.".format(i), '\n')
    with open("wangyiyun1.txt", "w", encoding='utf-8') as f:
        f.write(stt)
    print(stt)
# sava_db()
sava_yuju()
# lishi_jt()
# conn = sqlite3.connect(r'D:\Eleme\rili\rili.db')
# # 创建一个游标 curson
# cursor = conn.cursor()
# date_id = datetime.datetime.now().strftime('%Y%m%d')
# print(date_id)
# cursor.execute(
#     '''select is_jishi from rilibiao WHERE date_id = '{}' '''.format(date_id))  # 查找饿了么库里的账号表，目前只取第一个账号
# values = cursor.fetchall()
# print(values[0][0])
