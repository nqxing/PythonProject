from eleme.login.captcha_yz import captcha_yz
from eleme.login.login_by_mobile import login_by_mobile
import traceback
import requests
import time
from config.config import HEADERS, PROXIES, IS_DAILI

def mobile_send_code(mobile, sms_url, conn, cursor, logger):  # 输入手机号，获取短息验证码
    dict = {"scf": "ms", "mobile": "{}".format(mobile)}
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=HEADERS, data=dict, timeout=25,
                          proxies=PROXIES if IS_DAILI else None)
        if r.status_code == 400 and r.json()['message'] == '账户存在风险,需要图形验证码':
            logger.info('[{}]{}'.format(mobile, r.json()['message']))
            while True:
                result = captcha_yz(mobile, logger)
                if result['status'] == 0:
                    # 死循环，直到图形验证码出入正确为止
                    if result['message'].status_code == 400 and result['message'].json()['message'] == '图形验证码错误':
                        logger.info('[{}]{}，请重新输入'.format(mobile, result['message'].json()['message']))
                        time.sleep(5)
                    elif result['message'].status_code == 200 and 'validate_token' in result['message'].json():
                        logger.info('[{}]验证码校验成功，短信已发送，请查看手机验证码'.format(mobile))
                        time.sleep(15)  # 延迟15秒，确保短信已接收
                        result = login_by_mobile(result['message'].json()['validate_token'], mobile, sms_url,
                                                 conn, cursor, logger)
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
                logger.info('[{}]短信已发送，请查看手机验证码'.format(mobile))
                time.sleep(15)  # 延迟15秒，确保短信已接收
                result = login_by_mobile(r.json()['validate_token'], mobile, sms_url, conn, cursor, logger)
                return result
            else:
                result = {'status': 1, 'message': '2-获取短信验证码出错,{}'.format(r.json())}
                return result
    except:
        result = {'status': -1, 'message': 'Error :{}'.format(traceback.format_exc())}
        return result