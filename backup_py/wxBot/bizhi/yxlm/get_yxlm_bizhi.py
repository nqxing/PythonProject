import sqlite3
import requests
import json
import traceback
from config.config import YXLM_PATH
# YXLM_PATH = r'D:\wxBot1\bizhi\yxlm\yxlm.db'

def get_pf_num(hid):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    skins = []
    try:
        url = 'http://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(hid)
        r = requests.get(url, headers=headers)
        skins = json.loads('{}'.format(r.text))['skins']
        return skins
    except:
        print(traceback.format_exc())
        return skins

def get_yxlm_link():
    print('正在更新壁纸')
    new_bizhi = []
    try:
        r = requests.get('https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js')
        hero_dic = json.loads('{}'.format(r.text))
        hero_ids = hero_dic['hero']
        for i in hero_ids:
            pf_nums = get_pf_num(i['heroId'])
            if pf_nums:
                for p in pf_nums:
                    if i['title'] in p['name']:
                        pf_name = p['name']
                    else:
                        pf_name = p['name'] + ' {}'.format(i['title'])
                    if p['mainImg']:
                        if not is_exist(i['heroId'], pf_name):
                            sava_db(pf_name, p['mainImg'], i['title'], i['heroId'])
                            new_bizhi.append((pf_name, p['mainImg']))
            else:
                print('{},该英雄皮肤数量获取失败!'.format(hero_dic[i]))
            # print(i)
            # time.sleep(1)
        return new_bizhi
    except:
        print(traceback.format_exc())
        return new_bizhi

def sava_db(pf_name, pf_link, yx_name, yx_id):
    conn = sqlite3.connect(YXLM_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pf_link (pf_name,pf_link,yx_name,yx_id) VALUES ('{}', '{}', '{}', {})".format(pf_name, pf_link, yx_name, int(yx_id)))
    conn.commit()

def is_exist(yx_id, pf_name):
    conn = sqlite3.connect(YXLM_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pf_name FROM pf_link WHERE yx_id = {}".format(int(yx_id)))
    values = cursor.fetchall()
    if values:
        tup_pf_name = (pf_name,)
        if tup_pf_name in values:
            return True
    return False

# get_yxlm_link()