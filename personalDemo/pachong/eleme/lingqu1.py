# from config.config import IS_HTTPS, ELEME_DATA_PATH
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
    # conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    # cursor = conn.cursor()  # 获取游标
    # cursor.execute("select sns_avatar from eleme_tx")
    # sns_avatars = cursor.fetchall()
    # cursor.execute("select sns_username from eleme_tx")
    # sns_usernames = cursor.fetchall()
    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random ,
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; '.format(sid)
    }
    # print(ua.random)
    url = 'https://h5.ele.me/restapi/marketing/v2/promotion/weixin/{}'.format(link)
    dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(sign),
            "phone": "{}".format(phone), "device_id": "", "hardware_id": "", "platform": 0, "track_id": "undefined",
            "weixin_avatar": "", "weixin_username": "", "unionid": "fuck", "latitude": "", "longitude": ""}
    try:
        r = requests.post(url, headers=headers, data=dict, verify=False)
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
# r = cx_hongbao('18866674230', 'EC5ED3E1DC745444D15E87B6D7C0B306', '0e9a2166feb77688d8dcac51ddf9aa5d', 'DubcCacL3GqLItWGv18zttVgNyDUKTZspyTQ29', '2a6d38fbadbb2cfd.2')

r = cx_hongbao('15263819410', 'C27E47F19367530476F193E137E7958E', '91df0f4ceb5352e1a60bf71e2a334985', 'CgAAAOjV9tQP8gAEAADdJmT5q9_r301ojt9ZZ8fH8wHeD5qsewp0svfI', '1d7ee497c5081c20.2')
print(r)

def wx_lingqu():
    headers = {
        'referer': 'https://servicewechat.com/wxece3a9a4c82f58c9/230/page-frame.html',
        'x-ua': 'MiniAppVersion/0.7.6 DeviceId/o_PVDuAQRX9H58lzj-YF0K6O4b2I AppName/wechat Longitude/119.21190402560764 Latitude/26.03729329427083',
        'content-type': 'application/json',
        'x-shard': 'loc=119.21190402560764,26.03729329427083',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A54) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
        'cookie': 'SID=eJ1zdJr82buRY1QpcA9BOO0m283QUuZGLxAQ'
    }
    dict = {
        "group_sn":"1d7ee497c5081c20.2",
        "refer_user_id":"1817747",
        "weixin_uid":"oQZUI0cmSu81l7Scur1u2vWC2XxM",
        "phone":"15659020901",
        "user_id":36905538,
        "sns_type":6,
        "unionid":"o_PVDuAQRX9H58lzj-YF0K6O4b2I",
        "platform":2,
        "latitude":26.03729329427083,
        "longitude":119.21190402560764,
        "weixin_username":"Bot",
        "weixin_avatar":"https://wx.qlogo.cn/mmopen/vi_32/9wVIQxDlyq8FaKa3ibf3YZibcpdnvYbeKuibaXlib7ZiaO4pcHQcjMmM3cLpI3DGIY21GSNtEz6LGUFj23NKW9zgDkQ/132"
    }
    try:
        r = requests.post('https://mainsite-restapi.ele.me/marketing/v2/promotion/weixin/oQZUI0cmSu81l7Scur1u2vWC2XxM', headers=headers, json=dict, verify=False)
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
r = wx_lingqu()
print(r)
