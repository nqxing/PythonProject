# coding=gbk
import sqlite3
import pymysql
# conn = sqlite3.connect(r'C:\PythonProject\wxBot1\config\eleme.db')
# conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\eleme.db')
# conn = sqlite3.connect(r'D:\wxBot1\config\eleme.db')
# 创建一个游标 curson
# cursor = conn.cursor()

HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'

# mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
# mysql_cursor = mysql_conn.cursor()  # 获取游标
# cursor.execute("UPDATE eleme_sign SET wx_beizhu = '/大号' where puid = 'f07b6cbf'")
#
# str1 = 'Hi~ 终于等到你~|1：若需监控饿了么红包请直接将红包分享给我，分享几个即监控几个哦|2：如需加入饿了么大包群，发送“加入饿了么大包群”即可收到入群邀请|3：如需使用饿了么自动签到，发送“开启饿了么签到”即可开启自动签到功能哦|4：如需加入王者荣耀壁纸群请发送“王者荣耀”，英雄联盟壁纸群请发送“英雄联盟”|5：免券下载百度文库、垃圾分类查询、上班打卡提醒、一键生成证件照可以查看我朋友圈转发的文章哦'
# #
# str1 = '$TjRl11yIol5$'
# cursor.execute(
#     "INSERT INTO eleme_text (text) VALUES ('{}')".format(str1))
# conn.commit()

# sql = """ CREATE TABLE sms_mob(
#    id INTEGER PRIMARY KEY AUTO_INCREMENT,
#    yet           INTEGER(2),
#    yet_max           INTEGER(2),
#    alink      varchar(255),
#    state           varchar(255),
#    wx_beizhu           varchar(255),
#    add_times varchar(255),
#    up_times varchar(255),
#    retry_num INTEGER(2),
#    is_send varchar(255)
# ); """

# sql = """ CREATE TABLE sms_mob(
#    id INTEGER PRIMARY KEY AUTO_INCREMENT,
#    mobile           varchar(255),
#    sms_url           varchar(255),
#    note           varchar(255)
# ); """
#
# mysql_cursor.execute(sql)
# mysql_conn.commit()

# sql = ''' drop table eleme_id'''
# cursor.execute(sql)
# conn.commit()

# cursor.execute("UPDATE sqlite_sequence SET seq = 5 where name = 'eleme_id'")
# conn.commit()
# slist = ['vip_326', 'vip_322', 'vip_312', 'vip_305', 'vip_258', 'vip_192', 'vip_92']
# for s in slist:
#     cursor.execute("UPDATE eleme_sign SET state = 'no' WHERE wx_beizhu = '{}'".format(s))
#     conn.commit()
# cursor.execute("UPDATE daka_vip SET state = 'no' WHERE wx_beizhu = 'vip_168'")
# conn.commit()
#
# cursor.execute("UPDATE eleme_group_sn SET state = 'yes' WHERE group_sn = '1d64f14aa0904896.2'")
# conn.commit()
# cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '1d64f14aa0904896.2'")
# conn.commit()

# cursor.execute('''select bianhao, group_sn, alink, wx_beizhu from eleme_group_sn WHERE state = 'no' ''')  # 查找饿了么库里的账号表，目前只取第一个账号
# values = cursor.fetchall()
# print(values)
# print(len(values))

# cursor.execute("UPDATE eleme_count SET count = '6064' where id = 1")
# conn.commit()

# cursor.execute("UPDATE eleme_id SET mobile = '18866674230',sid = 'wYkxnxQnLzgHR8CXR81zFzhlQKWzZlHRMmGQ',sms_url = 'https://www.pdflibr.com/SMSContent/75' WHERE id = 1")
# conn.commit()
# cursor.execute("UPDATE eleme_id SET mobile = '18866478814',sid = 'EMNEvB2G5Dbf359eRSGsa5CinLk1E7QE8IAw',sms_url = 'https://www.pdflibr.com/SMSContent/76' WHERE id = 6")
# conn.commit()
# cursor.execute("UPDATE eleme_id SET mobile = '18866478774',sid = '0PhcVfkPFjGoJSmYKMxypwsxShrT6U9qHoVQ',sms_url = 'https://www.pdflibr.com/SMSContent/78' WHERE id = 8")
# conn.commit()
# cursor.execute("UPDATE eleme_id SET mobile = '18866478647',sid = 'T4kYqvp4E4RfLajYmfHzIwu5nDRTsBHzQKXg',sms_url = 'https://www.pdflibr.com/SMSContent/80' WHERE id = 9")
# conn.commit()
# cursor.execute("UPDATE eleme_id SET mobile = '15263819401',sid = 'vvdlJ8I3QqPHieAxom6xc0uFvUNkzqDQFdPw',sms_url = 'https://www.pdflibr.com/SMSContent/82' WHERE id = 5")
# conn.commit()
#
# cursor.execute("UPDATE eleme_xh SET mobile = '18866674230',sid = 'wYkxnxQnLzgHR8CXR81zFzhlQKWzZlHRMmGQ',sms_url = 'https://www.pdflibr.com/SMSContent/75' WHERE id = 2")
# conn.commit()
# cursor.execute("UPDATE eleme_xh SET mobile = '15263819401',sid = 'vvdlJ8I3QqPHieAxom6xc0uFvUNkzqDQFdPw',sms_url = 'https://www.pdflibr.com/SMSContent/82' WHERE id = 7")
# conn.commit()

# cursor.execute("UPDATE eleme_id SET mobile = '18866478974',sid = 'MtMO7DXEGfNmDGlVNQ4EGaCjSWiLaMrA0rmg',sms_url = 'https://www.pdflibr.com/SMSContent/84' WHERE id = 3")
# conn.commit()
# cursor.execute("UPDATE eleme_xh SET mobile = '18866478974',sid = 'MtMO7DXEGfNmDGlVNQ4EGaCjSWiLaMrA0rmg',sms_url = 'https://www.pdflibr.com/SMSContent/84' WHERE id = 4")
# conn.commit()


# cursor.execute("alter table eleme_text add text_info varchar(255);")
# conn.commit()
#
# cursor.execute("UPDATE eleme_text SET {} = '菜单信息' WHERE id = 1;".format('text_info'))
# cursor.execute("UPDATE eleme_text SET text_info = '一键领大包信息' WHERE id = 2;")
# cursor.execute("UPDATE eleme_text SET text_info = '淘口令代码' WHERE id = 3;")
# conn.commit()

# cursor.execute("alter table eleme_group_sn add up_times varchar(255);")
# conn.commit()
# cursor.execute("alter table eleme_group_sn add retry_num INTEGER(2);")
# conn.commit()
# cursor.execute("alter table eleme_group_sn add is_send varchar(255);")
# conn.commit()

# cursor.execute("alter table eleme_xh add is_sx varchar(10);")
# conn.commit()


# cursor.execute(
#     "INSERT INTO eleme_id (mobile, interface, sign, sid, sms_url, is_ret_code, users_id) VALUES ('17128240034', '810E17565A9C7EB9F14B791C244A48B1', 'ca480cac0634f829def66e3b2f89e0b5', "
#     "'qZ6nhS7ZrPzFJsoHte7S3V8UqXIupDhNQXQw', 'https://www.pdflibr.com/SMSContent/41', 'no', '1000003824024')"
#         )
# conn.commit()
#
# cursor.execute(
#     "INSERT INTO eleme_id (mobile, interface, sign, sid, sms_url, is_ret_code, users_id) VALUES ('17128240242', 'A58BE1DCB572D2C5DF77116047AF8252', '16e1b628c62becafa235e07fff2aa956', "
#     "'LAtVslaa657xyxmqSS75AKOeowpk0X75h4yA', 'https://www.pdflibr.com/SMSContent/52', 'no', '5983199482')"
#         )
# conn.commit()
#
# cursor.execute(
#     "INSERT INTO eleme_id (mobile, interface, sign, sid, sms_url, is_ret_code, users_id) VALUES ('17128240047', 'C27E47F19367530476F193E137E7958E', '91df0f4ceb5352e1a60bf71e2a334985', "
#     "'Bt80tkB3aWAhJ4ApqZtoUmTpX0zqWJ0JFczw', 'https://www.pdflibr.com/SMSContent/49', 'no', '5978519562')"
#         )
# conn.commit()
# import random,string
# num=string.ascii_letters+string.digits
# nwename =  "".join(random.sample(num,10))
# with open("name.txt", "w", encoding='utf-8') as f:
#     f.write(nwename)
import time
print(1)