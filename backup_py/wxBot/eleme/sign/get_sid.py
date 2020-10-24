from config.config import PROXIES, IS_DAILI, HEADERS
import requests
import time
import traceback

def mobile_send_code(mobile, logger):  # 输入手机号，获取短息验证码
    dict = {"scf": "ms", "mobile": "{}".format(mobile)}
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=HEADERS, data=dict, timeout=25,
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
        logger.error('{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证码发送失败，请重新发送手机号绑定'}
        return result

def captcha_yz(mobile, logger):  # 获取短息验证码时出现图形验证码验证方法
    captcha_url = 'https://h5.ele.me/restapi/eus/v3/captchas'
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    captcha_dict = {"captcha_str": "{}".format(mobile)}
    try:
        r = requests.post(captcha_url, headers=HEADERS, data=captcha_dict,
                           proxies=PROXIES if IS_DAILI else None,
                           timeout=25)
        if r.status_code == 200:
            captcha_hash = r.json()['captcha_hash']
            imgbase64 = r.json()['captcha_image'].split(',')[-1]
            cap_url = 'http://www.damagou.top/apiv1/recognize.html'
            cap_dict = {
                'image': imgbase64,
                'userkey': '3079cdcefb0b4b2bad8e6e8ab7786df5',
                'type': '1001'
            }
            cap_r = requests.post(cap_url, data=cap_dict)
            captcha = cap_r.text
            if len(captcha) == 4:
                time.sleep(5)
                captcha_dict1 = {"scf": "ms", "mobile": "{}".format(mobile),
                                 "captcha_hash": "{}".format(captcha_hash), "captcha_value": "{}".format(captcha)}
                r2 = requests.post(mobile_send_code_url, headers=HEADERS, data=captcha_dict1,
                                   proxies=PROXIES if IS_DAILI else None, timeout=25)
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
        logger.error('{}'.format(traceback.format_exc()))
        result = {'status': 2, 'message': '账号在获取图形验证码验证时出错了，请发送手机号重试'}
        return result

def login_by_mobile(validate_code, validate_token, mobile, logger):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        dict = {"mobile": "{}".format(mobile), "validate_token": "{}".format(validate_token),
                "validate_code": "{}".format(validate_code)}
        login_by_mobile_url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
        r = requests.post(login_by_mobile_url, headers=HEADERS, data=dict,
                          proxies=PROXIES if IS_DAILI else None, timeout=25)
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

# mob = '17128240046'
# # r = mobile_send_code(mob)
# # print(r)
# r = login_by_mobile('072074', '469e4f7ac4e061bce9221f33414f8b31aafa01a118dbcdf471dc51b2179d40c4', mob)
# print(r)