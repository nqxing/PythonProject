from package import *

def mobile_send_code(openId, mobile):  # 输入手机号，获取短息验证码
    dict = {"scf": "ms", "mobile": "{}".format(mobile)}
    mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    # mobile_send_code_url = 'https://restapi.ele.me/eus/login/mobile_send_code'
    try:
        r = requests.post(mobile_send_code_url, headers=HEADERS, json=dict, timeout=25, verify=False)
        # if r.status_code == 400 and r.json()['message'] == '账户存在风险,需要图形验证码':
        if r.status_code == 400:
            result = get_captcha(openId, mobile)
            if result['status'] == 0:
                result = {'status': 1, 'message': result['message']}
                return result
            else:
                return result
        else:
            if r.status_code == 200 and 'validate_token' in r.json():
                result = {'status': 0, 'message': '验证码发送成功，请在5分钟内回复收到的验证码：\n\n注：若需重新发送手机号请先回复数字“2”哦', 'validate_token': r.json()['validate_token'], 'mobile': mobile}
                return result
            else:
                result = {'status': 2, 'message': r.json()['message']+'\n建议换个手机号试试哦'}
                return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证码发送失败，请重新发送手机号绑定'}
        return result

def get_captcha(openId, mobile):  # 获取短息验证码时出现图形验证码验证方法
    captcha_url = 'https://h5.ele.me/restapi/eus/v3/captchas'
    # captcha_url = 'https://restapi.ele.me/eus/v4/captchas'
    captcha_dict = {"captcha_str": "{}".format(mobile)}
    try:
        r = requests.post(captcha_url, headers=HEADERS, data=captcha_dict, verify=False, timeout=25)
        print(r.text)
        if r.status_code == 200:
            captcha_hash = r.json()['captcha_hash']
            imgbase64 = r.json()['captcha_image'].split(',')[-1]
            imagedata = base64.b64decode(imgbase64)
            img_path = '{}\{}.jpg'.format(CAPTCHA_IMG_PATH, openId)
            file = open(img_path, "wb")
            file.write(imagedata)
            file.close()
            return {'status': 0, 'message': '{}'.format(captcha_hash)}
        else:
            result = {'status': -1, 'message': '账号在获取图形验证码验证时出错了，请发送手机号重试'}
            return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '账号在获取图形验证码验证时出错了，请发送手机号重试'}
        return result
def captcha_yz(mobile, captcha_hash, captcha, openId):
    try:
        mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
        # mobile_send_code_url = 'https://restapi.ele.me/eus/login/mobile_send_code'
        captcha_dict1 = {"scf": "ms", "mobile": "{}".format(mobile),
                         "captcha_hash": "{}".format(captcha_hash), "captcha_value": "{}".format(captcha)}
        r = requests.post(mobile_send_code_url, headers=HEADERS, data=captcha_dict1, verify=False, timeout=25)
        print(r.text)
        # 死循环，直到图形验证码出入正确为止
        if r.status_code == 400 and r.json()['message'] == '图形验证码错误':
            result = {'status': 1, 'message': '验证码验证错误'}
            return result
        elif r.status_code == 200 and 'validate_token' in r.json():
            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
            cursor = conn.cursor()  # 获取游标
            cursor.execute("SELECT open_id FROM sign_val_token")
            openIds = cursor.fetchall()
            if (openId,) in openIds:
                cursor.execute(
                    "UPDATE sign_val_token SET mobile = '{}', validate_token = '{}' where open_id = '{}'".format(mobile,
                                                                                                                 r.json()['validate_token'], openId))
                conn.commit()
            else:
                cursor.execute(
                    "INSERT INTO sign_val_token (open_id, mobile, validate_token) VALUES ('{}', '{}', '{}')".format(
                        openId, mobile, r.json()['validate_token']))
                conn.commit()
            result = {'status': 0, 'message': '验证码发送成功，请在5分钟内回复收到的验证码：\n\n注：若需重新发送手机号请先发送“2”哦'}
            return result
        else:
            result = {'status': -1, 'message': '验证码验证失败，请重新发送手机号绑定'}
            return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证码验证失败，请重新发送手机号绑定'}
        return result

def login_by_mobile(validate_code, validate_token, mobile):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        dict = {"mobile": "{}".format(mobile), "validate_token": "{}".format(validate_token),
                "validate_code": "{}".format(validate_code)}
        login_by_mobile_url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
        # login_by_mobile_url = 'https://restapi.ele.me/eus/login/login_by_mobile'
        r = requests.post(login_by_mobile_url, headers=HEADERS, data=dict, verify=False, timeout=25)
        if r.status_code == 200:
            if 'SID' in r.cookies and 'USERID' in r.cookies:
                sid = r.cookies['SID']
                users_id = r.cookies['USERID']
                result = {'status': 0, 'sid': sid, 'users_id': users_id}
                return result
            else:
                result = {'status': 1, 'message': '验证失效了，请重新发送手机号'}
                return result
        elif r.status_code == 400:
            result = {'status': 2, 'message': '验证码错误，请重新发送验证码'}
            return result
        else:
            result = {'status': 1, 'message': '验证失效了，请重新发送手机号'}  # 这种情况一般是短信验证码错误，接码网站上最新的饿了么短信不是你前15秒发的，刚好也有人用此号码接了饿了么短信
            return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证出现错误，请重新发送验证码试试吧'}
        return result