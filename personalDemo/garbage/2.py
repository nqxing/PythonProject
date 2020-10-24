import sqlite3
import json
from xpinyin import Pinyin
conn = sqlite3.connect("garbage.db")
#创建一个游标 curson
cursor = conn.cursor()
# sql = """ CREATE TABLE garbage_data(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    name           varchar(100) ,
#    type            int(2) ,
#    name_pinyin        varchar(100)
# ); """
# cursor.execute(sql)

# f = open("1.txt", "r")
# lists = list(f.readlines())
# dic = json.loads(lists[0])
# pin = Pinyin()
#
# for i in list(dic['data'].keys()):
#     for s in dic['data']['{}'.format(i)]:
#         name = s['n']
#         type = int(i)
#         name_pinyin = pin.get_pinyin(name, "")
#         sql = "INSERT INTO garbage_data(name, type, name_pinyin) values('{}', '{}', '{}') ".format(name, type, name_pinyin)
#         cursor.execute (sql)
#         conn.commit()
str = '人123'
cursor.execute("SELECT * FROM garbage_data WHERE name LIKE '%"+"{}".format(str)+"%'")
is_ret_code = cursor.fetchall()
print(is_ret_code)