import traceback
import requests
import time
from config.config import HEADERS, PROXIES, IS_DAILI


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
            logger.info('[{}]正在识别验证码'.format(mobile))
            cap_url = 'http://www.damagou.top/apiv1/recognize.html'
            cap_dict = {
                'image': imgbase64,
                'userkey': '3079cdcefb0b4b2bad8e6e8ab7786df5',
                'type': '1001'
            }
            cap_r = requests.post(cap_url, data=cap_dict)
            captcha = cap_r.text
            if len(captcha) == 4:
                logger.info('[{}]验证码识别成功，验证码为:{}'.format(mobile, captcha))
                time.sleep(5)
                captcha_dict1 = {"scf": "ms", "mobile": "{}".format(mobile),
                                 "captcha_hash": "{}".format(captcha_hash), "captcha_value": "{}".format(captcha)}
                r2 = requests.post(mobile_send_code_url, headers=HEADERS, data=captcha_dict1,
                                   proxies=PROXIES if IS_DAILI else None, timeout=25)
                result = {'status': 0, 'message': r2}
                return result
            else:
                logger.info('[{}]验证码识别错误，识别到的内容为:{}'.format(mobile, captcha))
                time.sleep(5)
                result = {'status': 1}
                return result
        else:
            result = {'status': 2, 'message': '图形验证码获取出错~{},{}'.format(r.status_code, r.text)}
            return result
    except:
        result = {'status': 2, 'message': 'Error :{}'.format(traceback.format_exc())}
        return result