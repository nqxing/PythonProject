# -*- coding:utf-8 -*-
# from config.config import IS_HTTPS, ELEME_DATA_PATH
import requests
import traceback
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
import sqlite3
from random import randint  # 随机函数
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from fake_useragent import UserAgent
def weixin_light_app_login():
    headers = {
        'Host': 'mainsite-restapi.ele.me',
        'Referer': 'https://servicewechat.com/wxece3a9a4c82f58c9/225/page-frame.html',
        'X-UA': 'MiniAppVersion/0.7.3 DeviceId/o_PVDuEt0r2BVT2GDNGi1PXGj02A AppName/wechat Longitude/119.21212005615234 Latitude/26.037235260009766',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI ',
        # 'cookie': 'SID={}; '.format(sid)
    }
    dict = {
        "authcode":"071foP1I0nbHJf2Q7D1I0O5P1I0foP19"
    }
    # print(ua.random)
    url = 'https://mainsite-restapi.ele.me/eus/v1/weixin_light_app_login'
    r = requests.post(url, headers=headers, data=dict, verify=False)
    print(r.text)

def weixin_light_app_authorize():
    headers = {
        'Host': 'mainsite-restapi.ele.me',
        'Referer': 'https://servicewechat.com/wxece3a9a4c82f58c9/225/page-frame.html',
        'X-UA': 'MiniAppVersion/0.7.3 DeviceId/o_PVDuEt0r2BVT2GDNGi1PXGj02A AppName/wechat Longitude/119.21212005615234 Latitude/26.037235260009766',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI ',
        # 'cookie': 'SID={}; '.format(sid)
    }
    dict = {
        "authcode": "081FdWl50nLcuD1hM8l50AC9m50FdWlX", "unionid": "o_PVDuEt0r2BVT2GDNGi1PXGj02A", "user_id": 169357636
    }
    # print(ua.random)
    url = 'https://mainsite-restapi.ele.me/eus/v1/weixin_light_app_authorize'
    r = requests.post(url, headers=headers, json=dict, verify=False)
    print(r.text)

def cx_hongbao():
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
    # ua = UserAgent(verify_ssl=False)
    # headers = {
    #     # 'User-Agent': ua.random ,
    #     'Content-Type': 'application/json',
    #     'Content-Length': '445',
    #     'Connection': 'keep-alive',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-cn',
    #     'Accept': '*/*',
    #     'X-Shard': 'loc=119.21212005615234,26.037235260009766',
    #     'Host': 'mainsite-restapi.ele.me',
    #     'Referer': 'https://servicewechat.com/wxece3a9a4c82f58c9/225/page-frame.html',
    #     'X-UA': 'MiniAppVersion/0.7.3 DeviceId/o_PVDuEt0r2BVT2GDNGi1PXGj02A AppName/wechat Longitude/119.21212005615234 Latitude/26.037235260009766',
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI ',
    #     'Cookie': 'SID={}; '.format(sid)
    # }
    headers = {
        # "Host": "mainsite-restapi.ele.me",
        # "Accept": "*/*",
        # "X-Shard": "loc=119.21212005615234,26.037235260009766",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-cn",
        "Content-Type": "application/json",
        # "Content-Length": "445",
        # "X-UA": "MiniAppVersion/0.7.3 DeviceId/o_PVDuEt0r2BVT2GDNGi1PXGj02A AppName/wechat Longitude/119.21212005615234 Latitude/26.037235260009766",
        # "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN",
        # "Referer": "https://servicewechat.com/wxece3a9a4c82f58c9/225/page-frame.html",
        "Cookie": "SID=GKkZAu8u7DzrCdS0XbOsSpAupe098QZDchUQ"

    }
    # print(ua.random)
    url = 'https://mainsite-restapi.ele.me/marketing/v2/promotion/weixin/oQZUI0Wz2ndF9jFBI-sPPGr9DZFU'
    # dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(sign),
    #         "phone": "{}".format(phone), "device_id": "", "hardware_id": "", "platform": 0, "track_id": "undefined",
    #         "weixin_avatar": "", "weixin_username": "", "unionid": "fuck", "latitude": "", "longitude": ""}
    dict = {"group_sn":"2a6512cc252ee47c.2","refer_user_id":"","weixin_uid":"","phone":"15160654911","user_id":169357636,"sns_type":6,"unionid":"o_PVDuEt0r2BVT2GDNGi1PXGj02A","platform":1,"latitude":"","longitude":"","weixin_username":"o","weixin_avatar":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erp5vduKPtu6jialeCgxHTO8D5QgWapfWSwHicria4VNviarflM2fKOc8ibjLwUf0k24icrMR6IGyQ2uRKw/132"}

    # dict = {"group_sn":"{}".format(group_sn),"refer_user_id":"267910329","weixin_uid":"oQZUI0Wz2ndF9jFBI-sPPGr9DZFU",
    #         "phone":"{}".format(phone),"user_id":169357636,"sns_type":6,"unionid":"o_PVDuEt0r2BVT2GDNGi1PXGj02A","platform":1,
    #         "latitude":26.037235260009766,"longitude":119.21212005615234,"weixin_username":"o","weixin_avatar":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erp5vduKPtu6jialeCgxHTO8D5QgWapfWSwHicria4VNviarflM2fKOc8ibjLwUf0k24icrMR6IGyQ2uRKw/132"}
    try:
        r = requests.post(url, headers=headers, json=dict, verify=False)
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

# r = cx_hongbao('15659020901', '79FB0FE106935CEBA42E85648DD7B644', 'e6ed6ff59a03d84b63178ac796c4021b', 'TMgRIsG6Pm0bklLPw0fTNPL8HlvWEh8KX3Qg', '2a4b2ec053b8d0eb.2')
# r = cx_hongbao('17128240242', 'A58BE1DCB572D2C5DF77116047AF8252', '16e1b628c62becafa235e07fff2aa956', 'UaRlUF7MVzjHQ1CHwGwZrtjteBgHWn09Cn3Q', '2a4b2ec053b8d0eb.2')
# 1	17128240034	810E17565A9C7EB9F14B791C244A48B1	ca480cac0634f829def66e3b2f89e0b5	pvbooxI2xk0gQ64zaEyVTPgwbpRS4C58KX5A	https://www.pdflibr.com/SMSContent/41	3130577310	qq231798	no

# r = cx_hongbao('17128240194', 'EC5ED3E1DC745444D15E87B6D7C0B306', '0e9a2166feb77688d8dcac51ddf9aa5d', 'f0QKJ3QyduXwGJnvqKqclOmRlKtlZlQ5fYdg', '2a4b2ec053b8d0eb.2')
# r = cx_hongbao('18866674203', 'F7D18D4DD24A322D440B84898AA2625B', 'df85ed85487b18fbf72a06ca7c0f9a7e', 'TMbBo2eW7ExLMOeIv0AYQMANpckYVrZ9pyEQ', '2a4b2ec053b8d0eb.2')
# r = cx_hongbao('18866674210', 'AFB6EF1F1B2267432ABF8AC94A2D4428', 'df86e718915b79527a14c02a49c10368', 'QBlkknHfMF7xFyhaYnx058QX28Z7h8Qlg91A', '2a4b2ec053b8d0eb.2')
# r = cx_hongbao('16739465446', 'DB3A764683FA0AD6BEA3FE78AF7AFB6B', '9f0177a1903404c9d0de42a917187995', 'eGZAPu0ybiFt1sX2Rx77D6kPJpXNAu34Bwig', '2a4b2ec053b8d0eb.2')
# r = cx_hongbao('17128240041', '5FF66BD1A8C11D310BFB2A3F4E83511A', 'e889435a42cef62a2eb3fcd36ecb7168', 'RbStXSqjN8lFFOSgDg4gG9iSAj1aaVvR9j5g', '2a4b2ec053b8d0eb.2')


r = cx_hongbao()
print(r)

# weixin_light_app_authorize()
# weixin_light_app_login()