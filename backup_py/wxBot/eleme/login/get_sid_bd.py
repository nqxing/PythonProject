import requests
from PIL import Image
import base64
import time
from bs4 import BeautifulSoup
import re
# from datetime import datetime
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pymysql
import traceback
import logging.handlers
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

LOG_FILE = r'bangd.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('bangd')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

HOST = 'localhost'
# HOST = '122.51.67.37'
USER = 'root'
PWD = 'MUGVHmugvtwja116ye38b1jhb'
# PWD = 'mm123456'
ret_time = 245

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',

}

def bangding(SID, users_id, mobile, sms_url, id):
    try:
        mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
        mysql_cursor = mysql_conn.cursor()  # 获取游标
        mysql_cursor.execute('''select interface, sign from eleme_id WHERE id = {} '''.format(id))  # 查找饿了么库里的账号表，目前只取第一个账号
        values = mysql_cursor.fetchall()
        openid, sign = values[0][0], values[0][1]
        print(openid, sign)
        url = 'https://h5.ele.me/restapi/marketing/hongbao/weixin/{}/change'.format(openid)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
            'cookie': 'SID={}; '.format(SID)
        }
        dict = {"sign":"{}".format(sign),"phone":"{}".format(mobile)}
        r = requests.post(url, data=dict, verify=False, headers=headers)
        if r.status_code == 200:
            mysql_cursor.execute(
                "UPDATE eleme_id SET mobile = '{}', sid = '{}', sms_url = '{}', users_id = '{}', is_sx = '{}' WHERE id = {}".format(mobile, SID, sms_url, users_id, '身份信息正常', id))
            mysql_conn.commit()
            result = {'status': 0, 'message': '绑定成功'}
            return result
        else:
            logger.error('{} - 绑定失败,{}'.format(mobile, r.text))
            result = {'status': 1, 'message': '绑定失败'}
            return result
    except:
        logger.error(traceback.format_exc())
        result = {'status': -1, 'message': '绑定方法调用异常'}
        return result

def mobile_send_code(mobile, sms_url, id, is_bd):  # 输入手机号，获取短息验证码
    dict = {"scf": "ms", "mobile": "{}".format(mobile)}
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=headers, data=dict, timeout=25)
        if r.status_code == 400 and r.json()['message'] == '账户存在风险,需要图形验证码':
            while True:
                result = captcha_yz(mobile, False)
                if result['status'] == 0:
                    # 死循环，直到图形验证码出入正确为止
                    if result['message'].status_code == 400 and result['message'].json()['message'] == '图形验证码错误':
                        print('[{}]{}，请重新输入'.format(mobile, result['message'].json()['message']))
                        time.sleep(5)
                    elif result['message'].status_code == 200 and 'validate_token' in result['message'].json():
                        print('[{}]验证码校验成功，短信已发送，请查看手机验证码'.format(mobile))
                        time.sleep(25)  # 延迟15秒，确保短信已接收
                        validate_token = result['message'].json()['validate_token']
                        result = login_by_mobile(validate_token, mobile, sms_url, id, is_bd)
                        if result['status'] == 2:
                            print('[{}]未找到饿了么验证码信息，等待{}秒重试 - {}'.format(mobile, ret_time, result['message']))
                            time.sleep(ret_time)
                            result = login_by_mobile(validate_token, mobile, sms_url, id, is_bd)
                            return result
                        else:
                            return result
                    else:
                        logger.error('{} - 图形验证码验证异常,{}'.format(mobile, result['message'].text))
                        result = {'status': 1, 'message': '图形验证码验证异常'}  # 这种情况一般是检测频繁操作了，后面可以在考虑这里加入代理 {"message":"您的操作太快了，请明天再来吧","name":"HERMES_CLIENT_ERROR"} 400
                        return result
                elif result['status'] == 1:
                    pass
                elif result['status'] == 2:
                    return result
                else:
                    return result
        else:
            if r.status_code == 200 and 'validate_token' in r.json():
                print('[{}]短信已发送，请查看手机验证码'.format(mobile))
                time.sleep(25)  # 延迟15秒，确保短信已接收
                validate_token = r.json()['validate_token']
                result = login_by_mobile(validate_token, mobile, sms_url, id, is_bd)
                if result['status'] == 2:
                    print('[{}]未找到饿了么验证码信息，等待{}秒重试 - {}'.format(mobile, ret_time, result['message']))
                    time.sleep(ret_time)
                    result = login_by_mobile(validate_token, mobile, sms_url, id, is_bd)
                    return result
                else:
                    return result
            else:
                if '您的帐号存在风险，为保护您的财产安全已冻结' in r.text:
                    mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
                    mysql_cursor = mysql_conn.cursor()  # 获取游标
                    mysql_cursor.execute(
                        "UPDATE sms_mob SET note = '账号已被冻结' WHERE mobile = '{}'".format(mobile))
                    mysql_conn.commit()
                    result = {'status': 1, 'message': '账号已被冻结'}
                    return result
                else:
                    logger.error('{} - 验证手机出现未知错误,{}'.format(mobile, r.text))
                    result = {'status': 1, 'message': '验证手机出现未知错误'}
                    return result
    except:
        logger.error(traceback.format_exc())
        result = {'status': -1, 'message': '验证手机方法调用异常'}
        return result

def captcha_yz(mobile, is_input):  # 获取短息验证码时出现图形验证码验证方法
    captcha_url = 'https://h5.ele.me/restapi/eus/v3/captchas'
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    captcha_dict = {"captcha_str": "{}".format(mobile)}
    try:
        r = requests.post(captcha_url, headers=headers, data=captcha_dict,
                           timeout=25)
        if r.status_code == 200:
            if is_input:
                captcha_hash = r.json()['captcha_hash']
                imgbase64 = r.json()['captcha_image'].split(',')[-1]
                imagedata = base64.b64decode(imgbase64)
                file = open('captcha.jpg', "wb")
                file.write(imagedata)
                file.close()
                img = Image.open('captcha.jpg')
                img.show()
                time.sleep(2)
                captcha = input("请手动输入验证码: ")
                captcha_dict1 = {"scf": "ms", "mobile": "{}".format(mobile),
                                 "captcha_hash": "{}".format(captcha_hash), "captcha_value": "{}".format(captcha), }
                r2 = requests.post(mobile_send_code_url, headers=headers, data=captcha_dict1,
                                   timeout=25)
                result = {'status': 0, 'message': r2}
                return result
            else:
                captcha_hash = r.json()['captcha_hash']
                imgbase64 = r.json()['captcha_image'].split(',')[-1]
                print('[{}]正在识别验证码'.format(mobile))
                cap_url = 'http://www.damagou.top/apiv1/recognize.html'
                cap_dict = {
                    'image': imgbase64,
                    'userkey': '3079cdcefb0b4b2bad8e6e8ab7786df5',
                    'type': '1001'
                }
                cap_r = requests.post(cap_url, data=cap_dict)
                captcha = cap_r.text
                if len(captcha) == 4:
                    print('[{}]验证码识别成功，验证码为:{}'.format(mobile, captcha))
                    time.sleep(5)
                    captcha_dict1 = {"scf": "ms", "mobile": "{}".format(mobile),
                                     "captcha_hash": "{}".format(captcha_hash), "captcha_value": "{}".format(captcha)}
                    r2 = requests.post(mobile_send_code_url, headers=headers, data=captcha_dict1,
                                       timeout=25)
                    result = {'status': 0, 'message': r2}
                    return result
                elif len(captcha) < 4:
                    print('[{}]验证码识别错误，识别到的内容为:{}'.format(mobile, captcha))
                    time.sleep(5)
                    result = {'status': 1}
                    return result
                elif len(captcha) > 4 and len(captcha) < 11:
                    print('[{}]验证码识别错误，识别到的内容为:{}'.format(mobile, captcha))
                    time.sleep(5)
                    result = {'status': 1}
                    return result
                else:
                    result = {'status': 2, 'message': '打码狗识别出错'}
                    return result

        else:
            logger.error('{} - 图形验证码获取出错[{}],{}'.format(mobile, r.status_code, r.text))
            result = {'status': 2, 'message': '图形验证码获取出错'}
            return result
    except:
        logger.error(traceback.format_exc())
        result = {'status': -1, 'message': '验证码方法调用异常'.format(traceback.format_exc())}
        return result

def login_by_mobile(validate_token, mobile, sms_url, id, is_bd):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        if len(sms_url) != 0: #该变量为空的话说明不是网上的接码平台号码 需手动输入短信验证码
            print('[{}]正在获取短信验证码'.format(mobile))
            validate_code = []
            html = requests.get(sms_url, headers=headers, timeout=25)
            if html.status_code == 200:
                Soup = BeautifulSoup(html.content, 'lxml')
                trList = Soup.find_all(name='tbody')[0].find_all(name='tr')
                if trList:
                    if str(datetime.datetime.now().strftime('%Y-%m-%d')) in str(trList[0]):
                        for tr in trList:
                            tr_str = str(tr)
                            if '【饿了么】' in tr_str:
                                validate_code.append(re.findall('验证码是(.*?)，', str(tr), re.S)[0])
                                break
                    else:
                        result = {'status': 1, 'message': '该号码当天没有接收短信'.format(mobile)}
                        return result
                else:
                    result = {'status': 1, 'message': 'trList列表为空'}
                    return result
                if validate_code:
                    print('[{}]短信验证码识别成功,验证码为{}'.format(mobile, validate_code[0]))
                    dict = {"mobile": "{}".format(mobile), "validate_token": "{}".format(validate_token),
                            "validate_code": "{}".format(validate_code[0])}
                    login_by_mobile_url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
                    r = requests.post(login_by_mobile_url, headers=headers, data=dict, timeout=25)
                    if r.status_code == 200:
                        if 'SID' in r.cookies and 'USERID' in r.cookies:
                            SID = r.cookies['SID']
                            users_id = r.cookies['USERID']
                            print('[{}]获取成功，新的SID为[{}]，userid为[{}]'.format(mobile, SID, users_id))
                            if is_bd:
                                bd_res = bangding(SID, users_id, mobile, sms_url, id)
                                return bd_res
                            else:
                                result = {'status': 0, 'message': 'SID获取成功'}
                                conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
                                cursor = conn.cursor()
                                cursor.execute(
                                    "UPDATE eleme_id SET sid = '{}', users_id = '{}' ,is_sx = '身份信息正常' WHERE mobile = '{}'".format(
                                        SID, users_id, mobile))
                                conn.commit()
                                print('[{}]新的SID已写入成功_eleme_id'.format(mobile))
                                return result
                        else:
                            logger.error('{} - SID获取出错,{}'.format(mobile, r.cookies))
                            result = {'status': 1, 'message': 'SID获取出错'}
                            return result
                    else:
                        logger.error('{} - 短信验证出错,{}'.format(mobile, r.text))
                        result = {'status': 2, 'message': '短信验证出错'}
                        return result
                else:
                    result = {'status': 2, 'message': '未找到饿了么短信'.format(mobile)}
                    return result
            else:
                logger.error('{} - {}访问出错[{}],{}'.format(mobile, sms_url, html.status_code, html.text))
                result = {'status': 1, 'message': '接码平台访问出错'.format(html.status_code, sms_url)}
                return result
    except:
        logger.error(traceback.format_exc())
        result = {'status': -1, 'message': '登录方法调用异常'}
        return result

def mobile_bd(values):
    try:
        mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
        mysql_cursor = mysql_conn.cursor()  # 获取游标
        mysql_cursor.execute('''select ids from mob_count WHERE id = 1 ''')  # 查找饿了么库里的账号表，目前只取第一个账号
        ids = mysql_cursor.fetchall()[0][0]
        if values:
            for v in range(len(values)):
                print('---------本次共有{}个手机号需重新绑定，当前为第{}个---------'.format(len(values), v+1))
                id = values[v][0]
                while True:
                    mysql_cursor.execute(
                        '''select * from sms_mob WHERE id = {} '''.format(ids))  # 查找饿了么库里的账号表，目前只取第一个账号
                    values1 = mysql_cursor.fetchall()[0]
                    mobile, sms_url = values1[1], values1[2]
                    print('正在验证第{}个手机号[{} - {}]'.format(ids, mobile, sms_url))
                    mob_res = mobile_send_code(mobile, sms_url, id, True)
                    ids += 1
                    mysql_cursor.execute(
                        "UPDATE mob_count SET ids = {}".format(ids))
                    mysql_conn.commit()
                    print('手机号[{}] - {}'.format(mobile, mob_res['message']))
                    if mob_res['status'] == 0:
                        mysql_cursor.execute(
                            "UPDATE sms_mob SET note = '已绑定ID[{}]' WHERE mobile = '{}'".format(id, mobile))
                        mysql_conn.commit()
                        break
                    else:
                        mysql_cursor.execute(
                            "UPDATE sms_mob SET note = '{}' WHERE mobile = '{}'".format(mob_res['message'], mobile))
                        mysql_conn.commit()
    except:
        pass

def main():
    conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
    cursor = conn.cursor()
    cursor.execute("select mobile, sms_url from eleme_id where is_sx in('未登录','短信验证出错','未找到饿了么短信','验证手机方法调用异常','登录方法调用异常','打码狗识别出错')")
    is_sxs = cursor.fetchall()
    get_mob_list = []
    get_sms_list = []
    for i in range(len(is_sxs)):
        if 'www.yinsiduanxin.com' in is_sxs[i][1]:
            get_sms_list.append(is_sxs[i][1])
            get_mob_list.append(is_sxs[i][0])
    if get_sms_list:
        for g in range(len(get_sms_list)):
            print('{} ---------本次共有{}个手机号需验证，当前为第{}个---------'.format(datetime.datetime.now(), len(get_sms_list), g + 1))
            result = mobile_send_code(get_mob_list[g], get_sms_list[g], 0, False)
            if result['status'] == 0:
                print('新sid获取成功')
            elif result['status'] == -1:
                print(result)
            else:
                print(result)
                message = result['message']
                if '账号已被冻结' == message:
                    cursor.execute(
                        "UPDATE eleme_id SET is_sx = '账号已被冻结', sms_url = '账号已被冻结' WHERE mobile = '{}'".format(
                            get_mob_list[g]))
                    conn.commit()
                elif '该号码当天没有接收短信' == message:
                    cursor.execute(
                        "UPDATE sms_mob SET note = '该号码当天没有接收短信' WHERE mobile = '{}'".format(
                            get_mob_list[g]))
                    conn.commit()
                else:
                    cursor.execute(
                        "UPDATE eleme_id SET is_sx = '{}' WHERE mobile = '{}'".format(message, get_mob_list[g]))
                    conn.commit()
    else:
        print('{} ------当前没有失效手机号------'.format(datetime.datetime.now()))

    # cursor.execute('''select * from eleme_id WHERE sms_url = '账号已被冻结' ''')
    # values = cursor.fetchall()
    # if values:
    #     mobile_bd(values)


def t1():
    main()
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(main, 'interval', hours=1)
    print('{} - 定时任务运行中，每隔1小时执行一次'.format(datetime.datetime.now()))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')

t1()