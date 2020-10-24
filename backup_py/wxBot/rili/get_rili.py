import sqlite3

def get_rili(date):
    conn = sqlite3.connect(r"rili\rili.db")
    # conn = sqlite3.connect(r'D:\eleme\rili\rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute('''select * from rilibiao where date_id = %s ''' % (date))
    results = cursor.fetchall()
    return results

def get_jishi(id):
    conn = sqlite3.connect(r"rili\rili.db")
    # conn = sqlite3.connect(r'D:\eleme\rili\rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute("select id, holiday from rilibiao where id > {} and is_jishi = 'yes' ".format(int(id)))
    results = cursor.fetchall()
    return results

def get_lishi_jt(date):
    conn = sqlite3.connect(r"rili\rili.db")
    # conn = sqlite3.connect(r'D:\eleme\rili\rili.db')
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute("select date_str from lishi_jt where date_id = '{}' ".format(date))
    results = cursor.fetchall()
    return results

# r = get_lishi_jt('0729')
# print(r)