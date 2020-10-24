import requests
import sqlite3
import traceback
import time
from config.config import WZRY_PATH
from bizhi.wzry.wzry import send_fqq
# WZRY_PATH = r'D:\wxBot1\bizhi\wzry.db'
def cx_nid(tid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://apps.game.qq.com/wmp/v3.1/'
    dict = {
    'p0': 18,
    'p1': 'searchNewsKeywordsList',
    'order': 'sIdxTime',
    'r0': 'cors',
    'type': 'iTarget',
    'source': 'app_news_search',
    'pagesize': 12,
    'page': 1,
    'id': tid,
    }
    news_ids = []
    try:
        r = requests.post(url, data=dict, headers=headers)
        if r.status_code == 200:
            r_json = r.json()
            if r_json['status'] == '0':
                results = r_json['msg']['result']
                for res in results:
                    iNewsId = res['iNewsId']
                    if tid == 1761:
                        title = '【新闻】' + res['sTitle']
                    elif tid == 1762:
                        title = '【公告】' + res['sTitle']
                    elif tid == 1763:
                        title = '【活动】' + res['sTitle']
                    else:
                        title = '【赛事】' + res['sTitle']
                    is_state = is_send(iNewsId, title)
                    if not is_state:
                        news_ids.append({'iNewsId': iNewsId, 'sTitle': title})
        return news_ids
    except:
        print(traceback.format_exc())
        return news_ids

def get_news_wzry(groups):
    for i in range(1761, 1765):
        results = cx_nid(i)
        if results:
            url = 'https://pvp.qq.com/web201706/newsdetail.shtml?tid={}'
            for res in results:
                if is_yingdi(res['iNewsId']):
                    link = 'https://image.ttwz.qq.com/h5/webdist/info-detail.html?iInfoId=180{}'.format(res['iNewsId'])
                else:
                    link = url.format(res['iNewsId'])
                title = res['sTitle']
                # print(title, link)
                send_str = '{}\n{}'.format(title, link)
                groups[0].send(send_str)
                send_fqq(send_str)
                add_doc_id(res['iNewsId'], title, link)
                time.sleep(1)
        time.sleep(5)

def add_doc_id(iDocID, title, link):
    conn = sqlite3.connect(WZRY_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO news_history (doc_id, title, link) VALUES ('{}', '{}', '{}')".format(iDocID, title, link)
    )
    conn.commit()

def is_send(iDocID, sTitle):
    conn = sqlite3.connect(WZRY_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "SELECT doc_id FROM news_history")
    doc_values = cursor.fetchall()
    cursor.execute(
        "SELECT title FROM news_history")
    tit_values = cursor.fetchall()
    if doc_values and tit_values:
        tup_iDocID = (iDocID,)
        tup_sTitle = (sTitle,)
        if tup_iDocID in doc_values and tup_sTitle in tit_values:
            return True
    return False

def is_yingdi(iInfoId):
    url = 'https://ssl.kohsocialapp.qq.com:10001/game/detailinfov4'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    dict = {
        'iInfoId': int('180'+iInfoId),
        'cSystem': 1,
        'apiVersion': 4,
        'gameId': 20001,
        # 'msdkToken':'',
        # 'h5Get':1,
    }
    try:
        r = requests.post(url, data=dict, headers=headers)
        if r.json()['returnCode'] == 0:
            return True
        else:
            return False
    except:
        print(traceback.format_exc())
        return False