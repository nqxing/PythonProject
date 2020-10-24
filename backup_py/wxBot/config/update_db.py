import sqlite3
conn = sqlite3.connect(r'D:\Eleme\config\eleme.db')
# conn = sqlite3.connect(r'config\eleme.db')
#创建一个游标 curson
cursor = conn.cursor()
# sql = """ CREATE TABLE daka_vip(
#    puid           varchar(100) ,
#    wx_beizhu           varchar(100) ,
#    wx_name            varchar(100) ,
#    state        varchar(100),
#    tx_time         varchar(100),
#    tx_time_num         varchar (2),
#    is_shouci         varchar (100),
#    kt_time         varchar(100)
# ); """
#
# cursor.execute(sql)
# conn.commit()
#
# sql = """ CREATE TABLE daka_text(
#    text1           varchar(100),
#    text2           varchar(100),
#    text3           varchar(100),
#    text4           varchar(100),
#    text5           varchar(100),
#    text6           varchar(100)
# ); """
# cursor.execute(sql)
# conn.commit()
#
# sql = """ CREATE TABLE eleme_text(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    text           varchar(500)
# ); """
# cursor.execute(sql)
# conn.commit()
#
# str1 = 'Hi~ 终于等到你~|1:若需监控饿了么红包请直接将红包分享给我，分享几个即监控几个哦|2:如需加入饿了么大包群，发送“加入饿了么大包群”即可收到入群邀请|3:如需使用一键领大包功能（无需等待，系统直接帮你点到最佳前一个），请发送“一键领大包”开通此功能|4:免券下载百度文库、垃圾分类查询、一键生成证件照可以查看我朋友圈转发的文章哦~'
# cursor.execute(
#     "INSERT INTO eleme_text (text) VALUES ('{}')".format(str1))
# conn.commit()
#
# str2 = '一键领大包点的基本都是3.2，太小了，大家暂时别充了'
# cursor.execute(
#     "INSERT INTO eleme_text (text) VALUES ('{}')".format(str2))
# conn.commit()
#
#
#
# text1 = '辛苦了~ 这么晚了还要工作~ 记得打卡哦~'
# text2 = '早啊~ 今天也是美美的一天~ 记得打卡哦~'
# text3 = '一天已快过半, 饿不饿呀~ 记得打卡哦~'
# text4 = '一天已经过半了, 饿不饿呀~ 记得打卡哦~'
# text5 = '好困啊啊! 不想上班，我要睡觉~ 记得打卡哦~'
# text6 = '忙碌一天了, 好好犒劳下自己吧~ 记得打卡哦~'
# cursor.execute(
#     "INSERT INTO daka_text (text1,text2,text3,text4,text5,text6) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(text1, text2, text3, text4, text5, text6))
# conn.commit()
cursor.execute('''select count from eleme_count where id = 2''')
num = int(cursor.fetchall()[0][0])
print(num)

num += 1
cursor.execute('''UPDATE eleme_count SET count = '{}' where id = 2'''.format(num))
conn.commit()

cursor.execute('''select count from eleme_count where id = 2''')
num = int(cursor.fetchall()[0][0])
print(num)