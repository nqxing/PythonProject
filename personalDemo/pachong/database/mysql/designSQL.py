
# 创建设计IQ_School表

import pymysql
db = pymysql.connect(host='124.156.102.35', user='hxycloud' , password='zz36233', port=3306, db='garbage')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS garbage_data (id INT (5) PRIMARY KEY AUTO_INCREMENT NOT NULL , name VARCHAR(255) NULL ,' \
'type INT (2) NULL ,name_pinyin VARCHAR(100) NULL)'
cursor.execute(sql)
db.close()