import sqlite3
import base64
# conn = sqlite3.connect(r'D:\wxBot1\bizhi\yxlm.db')
# # 创建一个游标 curson
# cursor = conn.cursor()
# cursor.execute(
#     "SELECT * FROM news_list WHERE id = 1")
# values = cursor.fetchall()
# print(values[0][2])
# debs64=base64.b64decode(values[0][2])
# print(debs64)
# print(type(values[0][2]))
# print()
# str = '13519014395584700416'
# str = str.encode('utf-8')
# #加密
# bs64=base64.b64encode(str)
# print(bs64)
# print(bytes.decode(bs64))
import datetime
print(datetime.datetime.now().strftime('%Y-%m-%d'))