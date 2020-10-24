import pymysql
db = pymysql.connect(host='106.13.81.161', user='root' , password='BKKPHbkkpn3v76y461yt8ncn0', port=3306, db='meitu') # 连接数据库
cursor = db.cursor()

#
# sql = 'CREATE TABLE IF NOT EXISTS meitulu (id INT (10) PRIMARY KEY NOT NULL , title VARCHAR(255) NULL ,' \
# 'num INT (5) NULL , jigou VARCHAR(255) NULL, mote VARCHAR(255) NULL, tag VARCHAR(255) NULL, furl VARCHAR(255) NULL, hurl VARCHAR(255) NULL, stime INT(20) NULL)'
# cursor.execute(sql)
#
# sql1 = 'CREATE TABLE IF NOT EXISTS meitulu_p (id INT (10) PRIMARY KEY AUTO_INCREMENT NOT NULL , title VARCHAR(255) NULL ,' \
# 'purl VARCHAR(255) NULL, pid INT(5) NULL)'
# cursor.execute(sql1)
#
sql2 = 'CREATE TABLE IF NOT EXISTS meitulu_f (id INT (3) PRIMARY KEY AUTO_INCREMENT NOT NULL , cname VARCHAR(100) NULL ,' \
'curl VARCHAR(255) NULL, beg_id INT(10) NULL, sta_id INT(10) NULL, sum_num INT(10) NULL)'
cursor.execute(sql2)

# sqls = ''' select cname, beg_id from meitulu_c WHERE id != 26 limit 1 '''
# sqlss = ''' select * from meitulu WHERE classify = "唯美" limit 1'''
# cursor.execute(sqlss)
# num = cursor.fetchall()
# print(num)
# print(num[-1])
# print(type(num))
# db.close()

# sqlsss = 'alter table meitulu_c AUTO_INCREMENT=1;'
# cursor.execute(sqlsss)
