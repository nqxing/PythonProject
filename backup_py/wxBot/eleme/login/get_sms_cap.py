import requests
from bs4 import BeautifulSoup
import time
import traceback
import re
import pymysql
from PIL import Image
import base64
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# 查询饿了么账号库且是www.yinsiduanxin.com该平台的未登录账号，自动识别验证码进行获取sid

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
}

# mysql链接信息
HOST = 'localhost'
# HOST = '122.51.67.37'
USER = 'root'
PWD = 'MUGVHmugvtwja116ye38b1jhb'
# PWD = 'mm123456'



def mobile_send_code(mobile, sms_url):  # 输入手机号，获取短息验证码
    dict = {"scf": "ms", "mobile": "{}".format(mobile)}
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=HEADERS, data=dict, timeout=25)
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
                        time.sleep(15)  # 延迟15秒，确保短信已接收
                        validate_token = result['message'].json()['validate_token']
                        result = login_by_mobile(validate_token, mobile, sms_url)
                        if result['status'] == 2:
                            print('[{}]未找到饿了么验证码信息，等待10秒重试'.format(mobile))
                            time.sleep(10)
                            result = login_by_mobile(validate_token, mobile, sms_url)
                            return result
                        else:
                            return result
                    else:
                        result = {'status': 1, 'message': '1-获取短信验证码出错,{}'.format(
                            result['message'].json())}  # 这种情况一般是检测频繁操作了，后面可以在考虑这里加入代理 {"message":"您的操作太快了，请明天再来吧","name":"HERMES_CLIENT_ERROR"} 400
                        return result
                elif result['status'] == 1:
                    pass
                else:
                    return result
        else:
            if r.status_code == 200 and 'validate_token' in r.json():
                print('[{}]短信已发送，请查看手机验证码'.format(mobile))
                time.sleep(15)  # 延迟15秒，确保短信已接收
                validate_token = r.json()['validate_token']
                result = login_by_mobile(validate_token, mobile, sms_url)
                if result['status'] == 2:
                    print('[{}]未找到饿了么验证码信息，等待10秒重试'.format(mobile))
                    time.sleep(10)
                    result = login_by_mobile(validate_token, mobile, sms_url)
                    return result
                else:
                    return result
            else:
                if '您的帐号存在风险，为保护您的财产安全已冻结' in r.text:
                    conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE eleme_id SET is_sx = '账号已被冻结', sms_url = '账号已被冻结' WHERE mobile = '{}'".format(mobile))
                    conn.commit()
                    cursor.execute(
                        "UPDATE sms_mob SET note = '账号已被冻结' WHERE mobile = '{}'".format(mobile))
                    conn.commit()
                result = {'status': 1, 'message': '2-获取短信验证码出错,{}'.format(r.json())}
                return result
    except:
        result = {'status': -1, 'message': 'Error :{}'.format(traceback.format_exc())}
        return result


def login_by_mobile(validate_token, mobile, sms_url):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        if len(sms_url) != 0: #该变量为空的话说明不是网上的接码平台号码 需手动输入短信验证码
            print('[{}]正在获取短信验证码'.format(mobile))
            validate_code = []
            html = requests.get(sms_url, headers=HEADERS, timeout=25)
            if html.status_code == 200:
                Soup = BeautifulSoup(html.content, 'lxml')
                trList = Soup.find_all(name='tbody')[0].find_all(name='tr')
                if trList:
                    if str(datetime.now().strftime('%Y-%m-%d')) in str(trList[0]):
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
                    r = requests.post(login_by_mobile_url, headers=HEADERS, data=dict, timeout=25)
                    if r.status_code == 200:
                        if 'SID' in r.cookies and 'USERID' in r.cookies:
                            SID = r.cookies['SID']
                            users_id = r.cookies['USERID']
                            print('[{}]获取成功，新的SID为[{}]，userid为[{}]'.format(mobile, SID, users_id))
                            result = {'status': 0, 'sid': SID}
                            conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE eleme_id SET sid = '{}', users_id = '{}' ,is_sx = '身份信息正常' WHERE mobile = '{}'".format(SID, users_id, mobile))
                            conn.commit()
                            print('[{}]新的SID已写入成功_eleme_id'.format(mobile))
                            return result
                        else:
                            result = {'status': 1, 'message': '未找到，sid获取出错~{},{}'.format(r.text, r.cookies)}
                            return result
                    else:
                        result = {'status': 1, 'message': '短信验证出错~{}'.format(
                            r.text)}  # 这种情况一般是短信验证码错误，接码网站上最新的饿了么短信不是你前15秒发的，刚好也有人用此号码接了饿了么短信
                        return result
                else:
                    result = {'status': 2, 'message': '{}该手机未找到饿了么短信'.format(mobile)}
                    return result
            else:
                result = {'status': 1, 'message': '接码平台地址访问出错了~{}，sms链接：{}'.format(html.status_code, sms_url)}
                return result
    except:
        result = {'status': 1, 'message': 'Error: {}'.format(traceback.format_exc())}
        return result

def captcha_yz(mobile, is_input):  # 获取短息验证码时出现图形验证码验证方法
    captcha_url = 'https://h5.ele.me/restapi/eus/v3/captchas'
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    captcha_dict = {"captcha_str": "{}".format(mobile)}
    try:
        r = requests.post(captcha_url, headers=HEADERS, data=captcha_dict,
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
                r2 = requests.post(mobile_send_code_url, headers=HEADERS, data=captcha_dict1,
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
                    r2 = requests.post(mobile_send_code_url, headers=HEADERS, data=captcha_dict1,
                                       timeout=25)
                    result = {'status': 0, 'message': r2}
                    return result
                else:
                    print('[{}]验证码识别错误，识别到的内容为:{}'.format(mobile, captcha))
                    time.sleep(5)
                    result = {'status': 1}
                    return result
        else:
            result = {'status': 2, 'message': '图形验证码获取出错~{},{}'.format(r.status_code, r.text)}
            return result
    except:
        result = {'status': 2, 'message': 'Error :{}'.format(traceback.format_exc())}
        return result

def main():
    conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
    cursor = conn.cursor()
    cursor.execute("select mobile, sms_url from eleme_id where is_sx = '未登录'")
    is_sxs = cursor.fetchall()
    get_mob_list = []
    get_sms_list = []
    for i in range(len(is_sxs)):
        if 'www.yinsiduanxin.com' in is_sxs[i][1]:
            get_sms_list.append(is_sxs[i][1])
            get_mob_list.append(is_sxs[i][0])
    if get_sms_list:
        for g in range(len(get_sms_list)):
            print('{} ---------本次共有{}个手机号需验证，当前为第{}个---------'.format(datetime.now(), len(get_sms_list), g + 1))
            result = mobile_send_code(get_mob_list[g], get_sms_list[g])
            if result['status'] == 0:
                print('新sid获取成功，sid为：{}'.format(result['sid']))
            elif result['status'] == -1:
                print(result)
            else:
                print(result)
                message = result['message'].replace("'", '')
                if '您的帐号存在风险，为保护您的财产安全已冻结' in message:
                    cursor.execute(
                        "UPDATE eleme_id SET is_sx = '账号已被冻结', sms_url = '账号已被冻结' WHERE mobile = '{}'".format(
                            get_mob_list[g]))
                    conn.commit()
                else:
                    cursor.execute(
                        "UPDATE eleme_id SET is_sx = '{}' WHERE mobile = '{}'".format(message, get_mob_list[g]))
                    conn.commit()
    else:
        print('{} ------当前没有失效手机号------'.format(datetime.now()))

def t1():
    main()
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(main, 'interval', hours=1)
    print('{} - 定时任务运行中，每隔1小时执行一次'.format(datetime.now()))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')

t1()