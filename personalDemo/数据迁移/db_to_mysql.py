import sqlite3
import os
import pymysql
import re
import datetime

conn = sqlite3.connect(os.getcwd()+"/wxbot.db")  # 饿了么数据库地址
cursor = conn.cursor()  # 获取游标
mysql_conn = pymysql.connect(host="122.51.67.37", user="root", password="mm123456", port=3306, db='public')
# mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标

def daka_vip():
    cursor.execute("select * from daka_vip")
    values = cursor.fetchall()
    for v in values:
        print(v)
        if v[3] == 'yes':
            v3 = True
        else:
            v3 = False
        if v[6] == 'yes':
            v6 = True
        else:
            v6 = False
        if v[4] == None:
            v4 = "无"
        else:
            v4 = v[4]
        if v[5] == None:
            v5 = 0
        else:
            v5 = v[5]
        mysql_cursor.execute(
            "INSERT INTO pub_card_users (wx_puid,wx_note,wx_name,state,time_list,time_num,is_first,create_time) VALUES ('{}', '{}', '{}', {}, '{}', {}, {}, '{}')".format(v[0], v[1], v[2], v3, v4, v5, v6, v[7]))
        mysql_conn.commit()

def eleme_amount():
    cursor.execute("select * from eleme_amount")
    values = cursor.fetchall()
    for v in values:
        # print(v)
        try:
            mysql_cursor.execute(
                "INSERT INTO pub_ele_hb_record (bianhao,name,amount,create_time,esource) VALUES ({}, '{}', '{}', '{}', '{}')".format(v[1], v[2], v[3], v[4], v[5]))
            mysql_conn.commit()
        except:
            # 转移微信名字带表情的呢陈 不然存不了
            reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
            file_name = re.sub(reg, '', v[2])
            mysql_cursor.execute(
                "INSERT INTO pub_ele_hb_record (bianhao,name,amount,create_time,esource) VALUES ({}, '{}', '{}', '{}', '{}')".format(v[1], file_name, v[3], v[4], v[5]))
            mysql_conn.commit()
            print('添加错误的{}'.format(v))

def rilibiao():
    conn = sqlite3.connect(os.getcwd() + "/rili.db")  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select * from rilibiao")
    values = cursor.fetchall()
    for v in values:
        print(v)
        if v[3] == None:
            v3 = ""
        else:
            v3 = v[3]
        if v[6] == "yes":
            v6 = True
        else:
            v6 = False
        mysql_cursor.execute(
            "INSERT INTO pub_card_text (text_id,text_info,text_story,week,holiday,is_holiday) VALUES ({}, '{}', '{}', {}, '{}', {})".format(v[1], v[2], v3, v[4], v[5], v6))
        mysql_conn.commit()

def eleme_sign():
    cursor.execute("select * from eleme_sign")
    values = cursor.fetchall()
    for v in values:
        print(v)
        if v[7] == 'yes':
            v7 = True
        else:
            v7 = False
        if v[8] == 'yes':
            v8 = True
        else:
            v8 = False
        if v[10] == "yes":
            v10 = True
        else:
            v10 = False
        if v[4] == None:
            v4 = ""
        else:
            v4 = v[4]
        if v[5] == None:
            v5 = ""
        else:
            v5 = v[5]
        if v[6] == None:
            v6 = ""
        else:
            v6 = v[6]
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        file_name = re.sub(reg, '', v[3])
        mysql_cursor.execute(
            "INSERT INTO pub_ele_sign_users (wx_puid,wx_note,wx_name,mobile,sid,user_id,state,is_bind,is_sign,create_time) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}')".format(v[1], v[2], file_name, v4, v5, v6, v7, v8, v10,v[9]))
        mysql_conn.commit()
def eleme_tx():
    cursor.execute("select * from eleme_tx")
    values = cursor.fetchall()
    for v in values:
        print(v)
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        file_name = re.sub(reg, '', v[1])
        mysql_cursor.execute(
            "INSERT INTO pub_ele_tx_urls (url,name,create_time) VALUES ('{}', '{}', '{}')".format(v[0], file_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        mysql_conn.commit()

def eleme_vip():
    cursor.execute("select * from eleme_vip")
    values = cursor.fetchall()
    for v in values:
        print(v)
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        file_name = re.sub(reg, '', v[3])
        mysql_cursor.execute(
            "INSERT INTO pub_vip_users (wx_puid,wx_note,wx_name,num,create_time) VALUES ('{}', '{}', '{}', {}, '{}')".format(v[0], v[2], file_name, v[1], v[4]))
        mysql_conn.commit()

# daka_vip()
# eleme_amount()
# rilibiao()
# eleme_sign()
# eleme_tx()
# eleme_vip()