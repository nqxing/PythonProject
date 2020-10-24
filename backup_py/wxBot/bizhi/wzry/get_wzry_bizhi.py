import sqlite3
import re, time
import requests
from pyquery import PyQuery as pq
import json
import traceback
from config.config import WZRY_PATH
from bizhi.wzry.wzry import short_url
# WZRY_PATH = r'D:\wxBot1\bizhi\wzry\wzry.db'

def get_pf_num(hid):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    skin_names = []
    try:
        url = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'.format(hid)
        r = requests.get(url, headers=headers)
        r.encoding = 'gbk'
        skins = pq(r.text)('.pic-pf-list').attr('data-imgname')
        skins = skins.split('|')
        for s in skins:
            if '&' in s:
                skin_names.append(s.split('&')[0])
            else:
                skin_names.append(s)
        return skin_names
    except:
        print(traceback.format_exc())
        return skin_names

def get_wzry_link():
    print('正在更新壁纸')
    skin_names = {}
    new_bizhi = []
    pf_link = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
    try:
        r = requests.get('http://game.gtimg.cn/images/yxzj/web201706/js/heroid.js')
        r.encoding = 'gbk'
        heros = re.findall('module_exports = {(.*?)};', r.text, re.S)
        hero = '{%s}'%heros[0].replace("'", '"')
        hero_dic = json.loads('{}'.format(hero))
        # hero_dic = {'154': '花木兰', '141': '貂蝉',}
        hero_ids = list(hero_dic.keys())
        for i in hero_ids:
            if i != '155':
                pf_nums = get_pf_num(i)
                if pf_nums:
                    skin_names[i] = pf_nums
                else:
                    print('{},该英雄皮肤数量获取失败!'.format(hero_dic[i]))
            # print(i)
            time.sleep(1)
        skins = list(skin_names.keys())
        for s in skins:
            for k, p in enumerate(skin_names[s]):
                pf_name = '{} {}'.format(hero_dic[s], p)
                if not is_exist(s, pf_name):
                    pf_url = pf_link.format(s, s, k+1)
                    short_link = short_url(pf_url)
                    if short_link != -1:
                        sava_db(p, pf_url, hero_dic[s], s, short_link)
                        new_bizhi.append((pf_name, short_link))
                    else:
                        sava_db(p, pf_url, hero_dic[s], s, pf_url)
                        new_bizhi.append((pf_name, pf_url))
        return new_bizhi
    except:
        print(traceback.format_exc())
        return new_bizhi

def sava_db(pf_name, pf_link, yx_name, yx_id, short_link):
    conn = sqlite3.connect(WZRY_PATH)
    # 创建一个游标 curson
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pf_link (pf_name,pf_link,yx_name,yx_id,dwz_url) VALUES ('{} {}', '{}', '{}', {}, '{}')".format(yx_name, pf_name, pf_link, yx_name, int(yx_id), short_link))
    conn.commit()

def is_exist(yx_id, pf_name):
    conn = sqlite3.connect(WZRY_PATH)
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

# get_wzry_link()