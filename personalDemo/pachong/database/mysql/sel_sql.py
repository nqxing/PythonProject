# 插入数据

import pymysql
db = pymysql.connect(host='122.51.67.37', user='root', password='mm123456', port=3306, db='eleme')
cursor = db.cursor()
# sql = """ update books set id = id + 1 """
# # sql = 'select * from books where id between {} and {};'.format(1, 20)
# cursor.execute(sql)
# db.commit()
# rows = cursor.fetchall()
# print(rows)


cursor.execute('''select * from eleme_id WHERE id = {} '''.format(1))
values = cursor.fetchall()
print(values)
# db.commit()