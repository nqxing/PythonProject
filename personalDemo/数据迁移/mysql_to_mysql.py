import os
import pymysql
import re
import datetime

mysql_conn = pymysql.connect(host="122.51.67.37", user="root", password="mm123456", port=3306, db='eleme')
# mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标

mysql_conn1 = pymysql.connect(host="122.51.67.37", user="root", password="mm123456", port=3306, db='public')
# mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
mysql_cursor1 = mysql_conn1.cursor()  # 获取游标

def group_sn():
    mysql_cursor.execute("select * from eleme_group_sn")
    values = mysql_cursor.fetchall()
    for v in values:
        print(v)
        if v[6] == 'yes':
            v6 = True
        else:
            v6 = False
        if v[9] == None:
            v9 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            v9 = v[9]
        sql = "INSERT INTO pub_ele_group_sn (bianhao, group_sn, yet, yet_max, url, state, from_name, create_time, up_time) VALUES ('{}', '{}', {}, {}, '{}', {}, '{}', '{}', '{}')".format(
                v[1], v[2], v[3], v[4],
            v[5], v6, v[7], v[8], v9)
        mysql_cursor1.execute(sql)
        mysql_conn1.commit()

def eleme_id():
    mysql_cursor.execute("select * from eleme_id")
    values = mysql_cursor.fetchall()
    for v in values:
        print(v)
        if v[6] == None:
            v6 = ''
        else:
            v6 = v[6]
        if v[7] == None:
            v7 = ''
        else:
            v7 = v[7]
        if v[8] == 'no':
            v8 = False
        else:
            v8 = True
        if v[9] == None:
            v9 = ''
        else:
            v9 = v[9]
        sql = "INSERT INTO pub_ele_id VALUES ({}, '{}', '{}', '{}','{}', '{}', '{}', '{}', {}, '{}', null, '{}', '{}')".format(v[0], v[1], v[2], v[3], v[4], v[5], v6, v7, v8, v9, v[11], v[12])
        mysql_cursor1.execute(sql)
        mysql_conn1.commit()
# group_sn()
# eleme_id()
def mob_list():
    mysql_cursor.execute("select * from sms_mob")
    values = mysql_cursor.fetchall()
    for v in values:
        print(v)
        sql = "INSERT INTO pub_sms_list VALUES ({}, '{}', '{}', '{}','{}')".format(v[0], v[1], v[2], v[3], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        mysql_cursor1.execute(sql)
        mysql_conn1.commit()
mob_list()