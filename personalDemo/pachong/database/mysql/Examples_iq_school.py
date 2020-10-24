import requests
import pymysql

def login_admin(page):
    params = {
        'page': page,
        'rows': 10
    }
    headers = {
        'Cookie': 'IQ_SSO_Token=5112C129BFE33F09F5F9D5115DDBABA1'
    }
    global uid
    url = 'http://base.iqcedu.com/student/student!pageStudent.do'
    r1 = requests.post(url,data=params,headers=headers)
    json = r1.json()
    items = json.get('rows')
    for item in items:
        save_sql(item,uid)
        uid = uid + 1
    page = json.get('total')
    return page
def save_sql(item,uid):
    id = item.get('id')
    stunum = item.get('studentNumber')
    classname = item.get('className')
    stuname = item.get('name')
    stuid = item.get('idCardNumber')
    # 插入或更新数据，如果主键存在，则更新数据
    sql = 'INSERT INTO iq_school(id, stunum, classname,stuname,stuid) values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=%s, stunum=%s, classname=%s,stuname=%s,stuid=%s'
    try:
        cursor.execute(sql, (id, stunum, classname, stuname, stuid) * 2)
        db.commit()
        print('已成功抓取%s条数据~~'% uid)
    except:
        db.rollback()
        db.close()
        print('数据写入失败~~')
def main(max):
    for page in range(2,max+1):
        login_admin(page)
    print('程序执行完毕~~')
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='mysql231798', port=3306, db='nqxing') # 连接数据库
    cursor = db.cursor()
    uid = 1
    nummax = login_admin(1)
    if nummax > 9:
        if nummax % 10 == 0:
            max = nummax / 10
            main(int(max))
        else:
            max = nummax / 10
            main(int(max) + 1)
    else:
        main(1)