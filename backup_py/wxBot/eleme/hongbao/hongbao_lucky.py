import requests
from random import randint  # 随机函数
import traceback
from config.config import ELEME_DATA_PATH
import sqlite3
def lucky_hongbao(group_sn, cursor, id):
    '''
    领取最佳红包 从最佳红包账号表里的账号进行领取
    :param group_sn:
    :param cursor:
    :param id:
    :return:
    '''
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor1 = conn.cursor()  # 获取游标
    cursor1.execute("select sns_avatar from eleme_tx")
    sns_avatars = cursor1.fetchall()
    cursor1.execute("select sns_username from eleme_tx")
    sns_usernames = cursor1.fetchall()

    # usernames = ['缺心','释然','玩弄ご','仙女味','凝残月','藸藸^(oo)^','浅安°','胡歌']
    # username = usernames[randint(0, 7)]

    cursor.execute("select * from eleme_lucky WHERE id = {}".format(id))
    values = cursor.fetchall()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; '.format(values[0][4])
    }
    url = 'https://h5.ele.me/restapi/marketing/v2/promotion/weixin/{}'.format(values[0][2])
    dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(values[0][3]),
            "phone": "{}".format(values[0][1]), "device_id": "", "hardware_id": "", "platform": 0,
            "track_id": "undefined", "weixin_avatar":  "{}".format(sns_avatars[randint(0, len(sns_avatars)-1)][0]), "weixin_username": "{}".format(sns_usernames[randint(0, len(sns_usernames)-1)][0]), "unionid": "fuck", "latitude": "",
            "longitude": ""}
    try:
        r = requests.post(url, headers=headers, data=dict, verify=False).json()
        # print(r)
        if 'promotion_records' in r and r['ret_code'] != 5:
            promotion_records = r['promotion_records']
            result = {'status': 0, 'promotion_records': promotion_records}
            # print(promotion_records)
            return result
        elif 'promotion_records' in r and r['ret_code'] == 5:
            result = {'status': 1, 'phone': values[0][1]}
            return result
        elif r['message'] == '未登录':
            result = {'status': 3, 'message': r}
            return result
        else:
            result = {'status': 2, 'message': '最佳手气红包领取出错~{}'.format(r)}
            return result
    except:
        result = {'status': -1, 'message': 'Error :{}'.format(traceback.format_exc())}
        return result