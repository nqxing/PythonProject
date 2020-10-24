import pymysql
db = pymysql.connect(host='106.13.81.161', user='root' , password='BKKPHbkkpn3v76y461yt8ncn0', port=3306) # 连接数据库
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print("abc: ", data)
cursor.execute('CREATE DATABASE meitu DEFAULT CHARACTER SET utf8') # 创建数据库
db.close()