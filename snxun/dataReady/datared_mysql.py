import pymysql
from dataReady.init import *

mysql_conn = pymysql.connect(host="116.62.126.139", user="root", password="mm123456", port=3306, db='test')
mysql_cursor = mysql_conn.cursor()  # 获取游标
usernames = Rname(15000)
for u in usernames:
    bloodtype = Bloodtype[random.randint(0, len(Bloodtype) - 1)]
    age = random.randint(20, 50)
    religion = Religion[random.randint(0, len(Religion) - 1)]
    nplace = Nplace[random.randint(0, len(Nplace) - 1)]
    schoolname = Schoolname[random.randint(0, len(Schoolname) - 1)]
    phone = '{}{}'.format(phoneNum[random.randint(0, len(phoneNum) - 1)], random.randint(100000000, 999999999))
    occupation = Occupation[random.randint(0, len(Occupation) - 1)]
    major = Major[random.randint(0, len(Major) - 1)]
    majorintroduce = Majorintroduce[random.randint(0, len(Majorintroduce) - 1)]
    sql = "INSERT INTO user (username,bloodtype,age,religion,nplace,schoolname,phone,occupation,major,majorintroduce,time) VALUES ('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            u, bloodtype, age, religion, nplace, schoolname, phone, occupation, major, majorintroduce, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mysql_cursor.execute(sql)
mysql_conn.commit()