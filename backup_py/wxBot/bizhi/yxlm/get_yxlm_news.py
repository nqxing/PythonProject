import requests
import sqlite3
import traceback
import time
from config.config import YXLM_PATH
import re, json
import base64
# YXLM_PATH = r'D:\wxBot1\bizhi\yxlm\yxlm.db'
def cx_nid(tid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://apps.game.qq.com/cmc/zmMcnTargetContentList?r0=jsonp&page=1&num=16&target={}&source=web_pc'.format(tid)
    news_ids = []
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r_json = re.findall('callback\((.*?)\);', r.text)
            if r_json:
                r_json = json.loads(r_json[0])
                if r_json['msg'] == 'OK':
                    results = r_json['data']['result']
                    for res in results:
                        res_dict = {}
                        # 加密
                        iDocID = bytes.decode(base64.b64encode(res['iDocID'].encode('utf-8')))
                        if tid == 23:
                            title = '【综合】' + res['sTitle']
                        elif tid == 24:
                            title = '【公告】' + res['sTitle']
                        elif tid == 25:
                            title = '【赛事】' + res['sTitle']
                        elif tid == 27:
                            title = '【攻略】' + res['sTitle']
                        else:
                            title = '【社区】' + res['sTitle']
                        is_state = is_send(iDocID)
                        if not is_state:
                            if 'sVID' in res:
                                res_dict['sVID'] = True
                            if res['sRedirectURL']:
                                res_dict['sRedirectURL'] = res['sRedirectURL']
                            res_dict['iDocID'] = iDocID
                            res_dict['sTitle'] = title
                            news_ids.append(res_dict)
        return news_ids
    except:
        print(traceback.format_exc())
        return news_ids

def get_news_yxlm(groups):
    tids = [23, 24, 25, 27, 28]
    for i in tids:
        results = cx_nid(i)
        if results:
            url = 'https://lol.qq.com/news/detail.shtml?docid={}'
            v_url = 'https://lol.qq.com/v/v2/detail.shtml?docid={}'
            for res in results:
                if 'sVID' in res:
                    link = v_url.format(bytes.decode(base64.b64decode(res['iDocID'])))
                elif 'sRedirectURL' in res:
                    link = res['sRedirectURL']
                else:
                    link = url.format(bytes.decode(base64.b64decode(res['iDocID'])))
                # print(res['sTitle'], link)
                groups[0].send('{}\n{}'.format(res['sTitle'], link))
                add_doc_id(res['iDocID'], res['sTitle'], link)
                time.sleep(1)
        time.sleep(5)

def add_doc_id(iDocID, title, link):
    conn = sqlite3.connect(YXLM_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO news_history (doc_id, title, link) VALUES ('{}', '{}', '{}')".format(iDocID, title, link)
    )
    conn.commit()

def is_send(iDocID):
    conn = sqlite3.connect(YXLM_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "SELECT doc_id FROM news_history")
    doc_values = cursor.fetchall()
    if doc_values:
        tup_iDocID = (iDocID,)
        if tup_iDocID in doc_values:
            return True
    return False


