import sqlite3
from config.config import YXLM_PATH

def yxlm(text):
    conn = sqlite3.connect(YXLM_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute("SELECT pf_name, pf_link FROM pf_link WHERE pf_name LIKE '%" + "{}".format(text) + "%'")
    results = cursor.fetchall()
    return results

def get_yxlm(text, msg):
    if msg.is_at == True:
        new_text = text.split('@Bot')[1].strip()
        results = yxlm(new_text)
        if len(results) != 0:
            result = ''
            for i in range(len(results)):
                strs = '{}\n{}\n\n'.format(results[i][0], results[i][1])
                result += strs
            msg.reply(result.strip())