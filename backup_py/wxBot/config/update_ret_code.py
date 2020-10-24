import sqlite3
# import pymysql

conn = sqlite3.connect(r'C:\PythonProject\Django\wxBot\config\wxbot.db')  # 饿了么数据库地址
cursor = conn.cursor()  # 获取游标

# mysql_conn = pymysql.connect(host='localhost', user='root', password='MUGVHmugvtwja116ye38b1jhb', port=3306, db='eleme')
# mysql_cursor = mysql_conn.cursor()  # 获取游标
#
# mysql_cursor.execute("UPDATE eleme_id SET is_ret_code = 'no'")
# mysql_conn.commit()

cursor.execute("UPDATE eleme_sign SET is_qd = 'no'")
conn.commit()
cursor.execute("UPDATE daka_vip SET is_shouci = 'yes'")
conn.commit()