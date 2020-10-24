import datetime
import pymysql
import time
import requests
import traceback
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序
def update_hongbao(result, mysql_cursor, mysql_conn, group_sn, hongbaoMax, phone):
    # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
    if result['status'] == 0:
        if result['value']['promotion_records']:
            hongbao = len(result['value']['promotion_records'])
            if hongbao < hongbaoMax - 1:
                mysql_cursor.execute(
                    "UPDATE eleme_group_sn SET yet = {}, up_times = '{}', is_send = 'no' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                mysql_conn.commit()
                mysql_cursor.execute(
                    "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
                mysql_conn.commit()
                if hongbao == 0:
                    mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                    mysql_conn.commit()
                    result = {'status': 1, 'value': '[{}]-更新了该红包领取数并删除'.format(group_sn)}
                else:
                    result = {'status': 1, 'value': '[{}]-更新了该红包领取数'.format(group_sn)}
                return result
            elif hongbao == hongbaoMax - 1:
                # print(group_sn)
                mysql_cursor.execute(
                    "UPDATE eleme_group_sn SET yet = {}, up_times = '{}' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                mysql_conn.commit()
                lucky_result = lucky_hongbao(group_sn)
                if lucky_result['status'] == 0:
                    is_lucky = lucky_result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                    if is_lucky:
                        lucky_name = lucky_result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                        lucky_amount = lucky_result['value']['promotion_records'][hongbaoMax - 1]['amount']
                        mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                        mysql_conn.commit()
                        result = {'status': 0, 'value': '[{}]-领取成功,最佳红包生成成功,领取人[{}],领取金额[{}]元'.format(group_sn, lucky_name, lucky_amount)}
                        return result
                    else:
                        mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                        mysql_conn.commit()
                        result = {'status': 0, 'value': '[{}]-领取成功,但该最佳红包生成出错,已删除该红包'.format(group_sn)}
                        return result
                elif lucky_result['status'] == 1:
                    result = {'status': -1, 'value': '[{}]-领取失败,身份信息过期了'.format(group_sn)}
                    return result
                else:
                    result = {'status': 2, 'value': '[{}]-领取失败,{}'.format(group_sn, lucky_result['value'])}
                    return result
            elif hongbao == hongbaoMax:
                is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                if is_lucky:
                    mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                    mysql_conn.commit()
                result = {'status': 3, 'value': '[{}]-删除了该红包,红包最佳手气已出现'.format(group_sn)}
                return result
            elif hongbao > hongbaoMax:
                promotion_records = result['value']['promotion_records']
                for p in promotion_records:
                    is_lucky = p['is_lucky']  # 减一是数组从0开始读
                    if is_lucky:
                        mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                        mysql_conn.commit()
                        break
                result = {'status': 4, 'value': '[{}]-删除了该红包,红包最佳手气已出现'.format(group_sn)}
                return result
        else:
            result = {'status': 1, 'value': '[{}]-查询失败,{}'.format(group_sn, result)}
            return result
    elif result['status'] == 1:
        mysql_cursor.execute(
            "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
        mysql_conn.commit()
        result = {'status': -2, 'value': '[{}]-手机号[{}]身份信息过期了'.format(group_sn, phone)}
        return result
    elif result['status'] == 2 or result['status'] == -1:
        result = {'status': -3, 'value': '[{}]-{}'.format(group_sn, result['value'])}
        return result

def lucky_hongbao(group_sn):
    headers = {
        "Content-Type": "application/json",
        'X-Shard': 'loc=119.21212005615234,26.037235260009766',
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN",
        "Cookie": "SID=GKkZAu8u7DzrCdS0XbOsSpAupe098QZDchUQ"

    }
    url = 'https://mainsite-restapi.ele.me/marketing/v2/promotion/weixin/oQZUI0Wz2ndF9jFBI-sPPGr9DZFU'
    dict = {"group_sn":"{}".format(group_sn),"refer_user_id":"","weixin_uid":"","phone":"15160654911","user_id":169357636,"sns_type":6,"unionid":"o_PVDuEt0r2BVT2GDNGi1PXGj02A","platform":1,"latitude":26.037235260009766,"longitude":119.21212005615234,"weixin_username":"o","weixin_avatar":"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erp5vduKPtu6jialeCgxHTO8D5QgWapfWSwHicria4VNviarflM2fKOc8ibjLwUf0k24icrMR6IGyQ2uRKw/132"}
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

def cx_hongbao(phone, link, sign, sid, group_sn):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN" ,
        'cookie': 'SID={}; '.format(sid)
    }
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

def lucky_main():
    lucky_num = 0
    i = 0
    # mysql链接信息
    HOST = 'localhost'
    # HOST = '122.51.67.37'
    USER = 'root'
    PWD = 'MUGVHmugvtwja116ye38b1jhb'
    # PWD = 'mm123456'

    mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    mysql_cursor.execute('''select * from eleme_id WHERE is_sx = '身份信息正常' ''') #查找饿了么库里的账号表，目前只取第一个账号
    values = mysql_cursor.fetchall()
    mysql_cursor.execute(
        '''select group_sn, yet_max from eleme_group_sn WHERE state = 'yes' ''')  # 查找饿了么库里的账号表，目前只取第一个账号
    renws = mysql_cursor.fetchall()
    # print('-----本次共查询到{}个红包，可用账号数为{}个-----'.format(len(renws), len(values)))
    for k, renw in enumerate(renws):
        group_sn, yet_max = renw[0], renw[1]
        phone, link, sign, sid, = values[i][1], values[i][2], values[i][3], values[i][4]
        result = cx_hongbao(phone, link, sign, sid, group_sn)
        update_result = update_hongbao(result, mysql_cursor, mysql_conn, group_sn, yet_max, phone)
        if update_result['status'] == 0:
            # print('[{}]No.{}：{}'.format(phone, k + 1, update_result['value']))
            lucky_num += 1
            if lucky_num == 5:
                break
        elif update_result['status'] == -1:
            # print('[{}]No.{}：{}'.format(phone, k + 1, update_result['value']))
            break
        else:
            # print('[{}]No.{}：{}'.format(phone, k + 1, update_result['value']))
            pass
        i += 1
        if i == len(values):
            i = 0
        time.sleep(1)
