from package import *

def return_keyInfo(key_path, key_text):
    try:
        conn = sqlite3.connect(key_path)
        # 创建一个游标 curson
        cursor = conn.cursor()
        # cursor.execute("SELECT text_note FROM keywords WHERE text = '{}'".format(key_text))
        cursor.execute("SELECT text,text_note FROM keywords WHERE text LIKE '%" + "{}".format(key_text) + "%'")
        results = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        if conn:
            conn.close()
        if len(results) != 0:
            result = '恭喜~ 找到了{}个和({})有关的资源\n\n'.format(len(results), key_text)
            for i in range(len(results)):
                strs = '{}\n\n'.format(results[i][1])
                result += strs
            return result.strip()
        else:
            return 0
    except:
        return "抱歉~ 查询出错了，请重试~"