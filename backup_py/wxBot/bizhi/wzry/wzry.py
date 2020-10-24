import sqlite3,requests,re
from config.config import WZRY_PATH
# from bizhi.wzry.index_wqg import index_wqg

def wzry(text):
    conn = sqlite3.connect(WZRY_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute("SELECT pf_name, dwz_url FROM pf_link WHERE pf_name LIKE '%" + "{}".format(text) + "%'")
    results = cursor.fetchall()
    return results

def get_wzry(text, msg):
    if msg.is_at == True:
        new_text = text.split('@Bot')[1].strip()
        results = wzry(new_text)
        if len(results) != 0:
            result = ''
            for i in range(len(results)):
                strs = '{}\n{}\n\n'.format(results[i][0], results[i][1])
                result += strs
            msg.reply(result.strip())
        else:
            msg.reply('害~ 没有找到{}的壁纸~ [委屈]'.format(new_text))
    if "邀请" in text and "加入了群聊" in text:
        msg.reply("欢迎新朋友~\n群里有全英雄高清无水印壁纸，需要请长按我头像@我英雄名字或皮肤的某个关键字获取哦~")
    # if text == '投票排行榜':
    #     result = index_wqg()
    #     msg.reply(result.strip())

def send_fqq(message):
    try:
        dict = {"group_id": 161758669,
                "message": message}
        r = requests.post("http://127.0.0.1:5700/send_group_msg", data=dict)
        if r.json()['status'] == "ok":
            return True
        else:
            return False
    except:
        return False

def short_url(urls):
    url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=short_url&need_short_url=1&url={}"
    try:
        r = requests.get(url.format(urls))
        if 'ok' in r.text and 'short_url' in r.text:
            short_url = re.findall('"short_url" : "(.*?)"', r.text)[0]
            return short_url
        else:
            return -1
    except:
        return -1