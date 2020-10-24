import json
from xpinyin import Pinyin
import pymysql
f = open("1.txt", "r")
lists = list(f.readlines())
dic = json.loads(lists[0])
pin = Pinyin()
db = pymysql.connect(host='124.156.102.35', user='hxycloud' , password='zz36233', port=3306, db='garbage')
cursor = db.cursor()

for i in list(dic['data'].keys()):
    for s in dic['data']['{}'.format(i)]:
        name = s['n']
        type = int(i)
        name_pinyin = pin.get_pinyin(name, "")
        sql = 'INSERT INTO garbage_data(name, type, name_pinyin) values(%s, %s, %s) '
        try :
            cursor. execute ( sql, (name, type, name_pinyin))
            db.commit()
        except:
            db.rollback()
            db.close()