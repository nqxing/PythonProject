import sqlite3
from config.config import GARBAGE_PATH

def cx_garbage(text):
    conn = sqlite3.connect(GARBAGE_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM garbage_data WHERE name LIKE '%" + "{}".format(text) + "%'")
    results = cursor.fetchall()
    return results

def get_garbage(text, msg):
    results = cx_garbage(text)
    if len(results) != 0:
        results = cx_garbage(text)
        msg.reply('本次为您找到{}条垃圾分类结果：'.format(len(results)))
        result = ''
        rtype = None
        for i in range(len(results)):
            if results[i][2] == 1:
                rtype = '湿垃圾'
            if results[i][2] == 2:
                rtype = '干垃圾'
            if results[i][2] == 3:
                rtype = '可回收物'
            if results[i][2] == 4:
                rtype = '有害垃圾'
            result += '{}.【{}】属于【{}】\n'.format(i + 1, results[i][1], rtype)
        msg.reply(result.strip())