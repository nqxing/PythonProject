from config.config import *
from config.fun_api import *

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
    values = SQL().select_ele_tx()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; '.format(sid)
    }
    # print(ua.random)
    url = 'https://h5.ele.me/restapi/marketing/v2/promotion/weixin/{}'.format(link)
    dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(sign),
            "phone": "{}".format(phone), "device_id": "", "hardware_id": "", "platform": 0, "track_id": "undefined",
            "weixin_avatar": "{}".format(values[randint(0, len(values)-1)][1]), "weixin_username": "{}".format(values[randint(0, len(values)-1)][2]), "unionid": "fuck", "latitude": "", "longitude": ""}
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