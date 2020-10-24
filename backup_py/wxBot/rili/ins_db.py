import sqlite3
conn = sqlite3.connect(r'rili.db')
# 创建一个游标 curson
# cursor = conn.cursor()
# sql = """ CREATE TABLE rilibiao(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    date_id           varchar(100) ,
#    date_str           varchar(100) ,
#    week        varchar(100),
#    holiday            varchar(100) ,
#    is_jishi        varchar(100),
#    yuju        varchar(500)
# ); """
#
# cursor.execute(sql)
# conn.commit()

# cursor = conn.cursor()
# sql = """ CREATE TABLE lishi_jt(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    date_id           varchar(100) ,
#    date_str           varchar(500)
# ); """
#
# cursor.execute(sql)
# conn.commit()