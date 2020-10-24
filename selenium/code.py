import sqlite3

conn = sqlite3.connect(r'code.db')
# 创建一个游标 curson
cursor = conn.cursor()
#
# sql = """ CREATE TABLE code(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    open_id           varchar(500),
#    sms_code           INTEGER(255)
# ); """
#
# cursor.execute(sql)
# conn.commit()

# cursor.execute(
#     "INSERT INTO code (open_id, sms_code) VALUES ('test', 123456)"
#         )
# conn.commit()

cursor.execute(
    "UPDATE code SET sms_code = 408838 WHERE open_id = '{}'".format("test")
        )
conn.commit()