from config.config import IS_HTTPS
import requests
import time
import traceback
from random import randint  # 随机函数
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sign(sid, users_id, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id)
    }
    sign_url = 'https://h5.ele.me/restapi/member/v1/users/{}/sign_in?channel=app&captcha_code=&captcha_hash=&source=main'.format(users_id)
    try:
        sign_r = requests.post(sign_url, headers = headers, verify=False if IS_HTTPS else None)
        # print(sign_r.text)
        def fanpai():
            try:
                url = 'https://h5.ele.me/restapi/member/v2/users/{}/sign_in/daily/prize?channel=app&index={}'.format(users_id,
                                                                                                                    randint(0, 2))
                fanp_r = requests.post(url, headers=headers, verify=False if IS_HTTPS else None)
                if fanp_r.status_code == 200:
                    fanp_list = fanp_r.json()
                    if type(fanp_list).__name__ == 'list':
                        for f in fanp_list:
                            if f['status'] == 1:
                                name = f['prizes'][0]['name']
                                sum_condition = f['prizes'][0]['sum_condition']
                                amount = f['prizes'][0]['amount']
                                return '【{}】满{}减{}'.format(name, sum_condition, amount)
                    else:
                        return fanp_r.text
                else:
                    message = fanp_r.json()['message']
                    return message
            except:
                logger.debug('{}'.format(traceback.format_exc()))
                return "翻牌出错了"
        def fenx():
            try:
                url = 'https://h5.ele.me/restapi/member/v1/users/{}/sign_in/wechat?channel=app'.format(users_id)
                r = requests.post(url, headers=headers, verify=False if IS_HTTPS else None)
                return r
            except:
                logger.debug('{}'.format(traceback.format_exc()))
                return "Error"
        if sign_r.status_code == 200 and len(sign_r.json()) == 0:
            hb_list = []
            fanp_result = fanpai()
            hb_list.append(fanp_result)
            time.sleep(2)
            fenx_r = fenx()
            time.sleep(2)
            if fenx_r != 'Error':
                if fenx_r.status_code == 200:
                    fanp_result = fanpai()
                    hb_list.append(fanp_result)
                else:
                    hb_list.append('分享朋友圈失败，翻牌失败')
            else:
                hb_list.append('分享朋友圈失败，翻牌失败')
            return hb_list
        elif sign_r.status_code == 200 and len(sign_r.json()) != 0:
            hb_list = []
            if type(sign_r.json()).__name__ == 'list':
                for f in sign_r.json():
                    name = f['name']
                    sum_condition = f['sum_condition']
                    amount = f['amount']
                    hb_list.append('【{}】满{}减{}'.format(name, sum_condition, amount))
                return hb_list
            else:
                return sign_r.text
        else:
            logger.debug('{}'.format(sign_r.json()))
            message = sign_r.json()['message']
            return message
    except:
        logger.debug('{}'.format(traceback.format_exc()))
        return "签到失败，请手动签到试试"

def cx_sign(sid, users_id, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id)
    }
    try:
        url = 'https://h5.ele.me/restapi/member/v1/users/{}/sign_in/info?'.format(users_id)
        r = requests.get(url, headers=headers, verify=False if IS_HTTPS else None)
        if r.status_code == 200:
            statuses = r.json()['statuses']
            num = 0
            for s in statuses:
                if s == 1:
                    num += 1
            return '\n--你已签到{}天'.format(num)
        else:
            logger.debug('{}'.format(r.json()))
            return "\n--查询已签天数异常"
    except:
        logger.debug('{}'.format(traceback.format_exc()))
        return "\n--查询已签天数异常"

def sign_in_award(sid, users_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id)
    }
    url = 'https://h5.ele.me/restapi/notify/subscription/push?channel=eleme&business=sign_in_award'
    r = requests.get(url, headers=headers, verify=False if IS_HTTPS else None)
    print(r.status_code)
    print(r.text)

def addresses(sid, users_id):
    def timeStamp(timeNum):
        timeStamp = float(timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id)
    }
    url = 'https://restapi.ele.me/member/v1/users/{}/addresses?extras[]=is_brand_member'.format(users_id)
    r = requests.get(url, headers=headers, verify=False if IS_HTTPS else None)
    print(r.json())
    for j in r.json():
        address = '{},{}'.format(j['address'], j['address_detail'])
        name = j['name']
        sex = j['sex']
        phone = j['phone']
        created_at = j['created_at']
        created_date = timeStamp(created_at)
        tag = j['tag']
        if sex == 1:
            sex = '男'
        if sex == 2:
            sex = '女'
        userstr = '[{}]{} {}[{}] {} {}'.format(tag, address, name, sex, phone, created_date)
        print(userstr)

# r = cx_sign('GIUeV57TT6B4yCi8hYkesXdZupaUg1JPGznw', '169357636') #goushun
# print(r)
# r = sign('6y7GOT6EPaqsGEq0xJBiSEPPfE608QQUyF4A', '1000004270110') # 16739465442  签到出现 图形验证码输入错误
# r = sign('ePWbqrWXM0C8TbXWQIrUsRoFVKX57t76As9Q', '6084251522') # 16739465441  ['【品质联盟专享】满35减3']
# r = sign('ULjk4R3AqHPpXGlUZFQ3Db86v0pI3nAKazuQ', '6380309994') # 15263819409  #['【品质联盟专享】满50减5', '【新零售新客红包】满29减10']
# r = sign('cYRCjZ17PruKN1G6SnCrwPmeQbvquisPTgkg', '2000007372910') # 15263819409  #['【品质联盟专享】满30减1', '【品质联盟专享】满30减1']
# sign_in_award('cYRCjZ17PruKN1G6SnCrwPmeQbvquisPTgkg', '2000007372910')
# addresses('MDrklP7ppEl4q2sCB6Y4xjJjBdxRbaa4ghSQ', '932327410')


