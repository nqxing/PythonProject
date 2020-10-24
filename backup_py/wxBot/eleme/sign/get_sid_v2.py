from config.config import PROXIES, IS_DAILI, MOB_HEADERS, HEADERS
import requests
import time
import traceback

def mobile_send_code(mobile, logger):  # 输入手机号，获取短息验证码
    dict = {"mobile":"{}".format(mobile),"latitude":26.042372,"longitude":119.21364,"via_audio":False}
    mobile_send_code_url = 'https://restapi.ele.me/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=MOB_HEADERS, json=dict, verify=False, timeout=25,
                          proxies=PROXIES if IS_DAILI else None)
        if r.status_code == 400 and r.json()['message'] == '账户存在风险,需要图形验证码':
            while True:
                result = captcha_yz(mobile, logger)
                if result['status'] == 0:
                    # 死循环，直到图形验证码出入正确为止
                    if result['message'].status_code == 400 and result['message'].json()['message'] == '图形验证码错误':
                        time.sleep(5)
                    elif result['message'].status_code == 200 and 'validate_token' in result['message'].json():
                        result = {'status': 0, 'message': '验证码发送成功，现在请回复收到的验证码（注：若5分钟内未收到验证码请重新发送手机号）',
                                  'validate_token': result['message'].json()['validate_token'], 'mobile': mobile}
                        return result
                    else:
                        result = {'status': 1, 'message': '验证码发送失败，请重新发送手机号绑定'}
                        return result
                elif result['status'] == 1:
                    pass
                else:
                    return result
        else:
            if r.status_code == 200 and 'validate_token' in r.json():
                result = {'status': 0, 'message': '验证码发送成功，现在请回复收到的验证码（注：若5分钟内未收到验证码请重新发送手机号）', 'validate_token': r.json()['validate_token'], 'mobile': mobile}
                return result
            else:
                result = {'status': 1, 'message': r.json()['message']}
                return result
    except:
        print(traceback.format_exc())
        # logger.error('{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证码发送失败，请重新发送手机号绑定'}
        return result

def captcha_yz(mobile, logger):  # 获取短息验证码时出现图形验证码验证方法
    captcha_url = 'https://restapi.ele.me/eus/v4/captchas?captcha_str={}'.format(mobile)
    mobile_send_code_url = 'https://restapi.ele.me/eus/login/mobile_send_code'
    try:
        r = requests.get(captcha_url, headers=HEADERS, verify=False,
                           proxies=PROXIES if IS_DAILI else None,
                           timeout=25)
        # print(r.text)
        if r.status_code == 200:
            captcha_hash = r.json()['captcha_hash']
            imgbase64 = r.json()['captcha_image']
            cap_url = 'http://www.damagou.top/apiv1/recognize.html'
            cap_dict = {
                'image': imgbase64,
                'userkey': '3079cdcefb0b4b2bad8e6e8ab7786df5',
                'type': '1001'
            }
            cap_r = requests.post(cap_url, data=cap_dict)
            captcha = cap_r.text
            print(captcha)
            if len(captcha) == 4:
                time.sleep(5)
                captcha_dict1 = {"captcha_hash":"{}".format(captcha_hash),"captcha_value":"{}".format(captcha),
                                 "mobile":"{}".format(mobile),"latitude":26.041218,"longitude":119.2118,"via_audio":False}
                r2 = requests.post(mobile_send_code_url, headers=HEADERS,  verify=False, data=captcha_dict1,
                                   proxies=PROXIES if IS_DAILI else None, timeout=25)
                print(r2.text)
                result = {'status': 0, 'message': r2}
                return result
            else:
                time.sleep(5)
                result = {'status': 1}
                return result
        else:
            result = {'status': 2, 'message': '[{}]账号在获取图形验证码验证时出错了，请发送手机号重试'.format(r.status_code)}
            return result
    except:
        print(traceback.format_exc())
        # logger.error('{}'.format(traceback.format_exc()))
        result = {'status': 2, 'message': '账号在获取图形验证码验证时出错了，请发送手机号重试'}
        return result

def login_by_mobile(validate_code, validate_token, mobile, logger):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        dict = {"validate_token":"{}".format(validate_token),"validate_code":"{}".format(validate_code),"latitude":26.041218303143978,"longitude":119.21180058270693}
        login_by_mobile_url = 'https://restapi.ele.me/eus/login/login_by_mobile'
        import uuid
        import time
        MOB_HEADERS['X-Eleme-RequestID'] = '{}|{}'.format(''.join(str(uuid.uuid1()).split('-')).upper(), int(round(time.time() * 1000)))
        print(MOB_HEADERS)
        r = requests.post(login_by_mobile_url, headers=MOB_HEADERS, verify=False, json=dict,
                          proxies=PROXIES if IS_DAILI else None, timeout=25)
        print(r.text)
        print(r.cookies)
        if r.status_code == 200:
            if 'SID' in r.cookies and 'USERID' in r.cookies:
                sid = r.cookies['SID']
                users_id = r.cookies['USERID']
                result = {'status': 0, 'sid': sid, 'users_id': users_id}
                return result
            else:
                result = {'status': 1, 'message': '{}'.format(r.json()['message'])}
                return result
        else:
            result = {'status': 1, 'message': '{}'.format(r.json()['message'])}  # 这种情况一般是短信验证码错误，接码网站上最新的饿了么短信不是你前15秒发的，刚好也有人用此号码接了饿了么短信
            return result
    except:
        logger.error('{}'.format(traceback.format_exc()))
        result = {'status': 1, 'message': '验证出现错误，请发送验证码重试'}
        return result

mob = '15160654911'
# r = mobile_send_code(mob, 1)
# print(r)
r = login_by_mobile('364668', 'e07e8d9c0e818b9bfb9e48bef70427268604a6eb643c2eec3e80a67ad61d1a12', mob, 1)
print(r)