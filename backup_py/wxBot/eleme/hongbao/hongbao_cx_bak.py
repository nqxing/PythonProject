from config.config import IS_HTTPS, ELEME_DATA_PATH
import requests
import traceback
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
import sqlite3
from random import randint  # 随机函数
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from fake_useragent import UserAgent


def cx_hongbao(phone, link, sign, sid, group_sn):
    '''
     查询红包领取情况，第一次访问默认领取一个红包（已达5次后只查询）
    :param phone:
    :param link:
    :param sign:
    :param sid:
    :param group_sn:
    :return:
    '''
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select sns_avatar from eleme_tx")
    sns_avatars = cursor.fetchall()
    cursor.execute("select sns_username from eleme_tx")
    sns_usernames = cursor.fetchall()
    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random,
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; '.format(sid)
    }
    # print(ua.random)
    # aurl = 'https://h5.ele.me/restapi/marketing/v1/hongbao/weixin/{}/activities?weixin_uid={}&sign={}&sns_type=3&latitude=&longitude='.format(link, link, sign)
    # r1 = requests.get(aurl, headers=headers).json()
    # print(r1)
    # burl = 'https://h5.ele.me/restapi/marketing/themes/4307/group_sns/{}'.format(group_sn)
    # r2 = requests.get(burl, headers=headers).json()
    # print(r2)

    url = 'https://h5.ele.me/restapi/marketing/v2/promotion/weixin/{}'.format(link)
    dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(sign),
            "phone": "{}".format(phone), "device_id": "", "hardware_id": "", "platform": 0, "track_id": "undefined",
            "weixin_avatar": "{}".format(sns_avatars[randint(0, len(sns_avatars)-1)][0]), "weixin_username": "{}".format(sns_usernames[randint(0, len(sns_usernames)-1)][0]), "unionid": "fuck", "latitude": "", "longitude": ""}
    try:
        r = requests.post(url, headers=headers, data=dict, verify=False if IS_HTTPS else None)
        if r.status_code == 200 and 'promotion_records' in r.json():
            result = {'status': 0, 'value': r.json()}
            return result
        elif r.json()['message'] == '未登录':
            result = {'status': 1, 'value': r.json()}
            return result
        else:
            result = {'status': 2, 'value': r.json()}
            return result
    except:
        result = {'status': -1, 'value': 'Error :{}'.format(traceback.format_exc())}
        return result