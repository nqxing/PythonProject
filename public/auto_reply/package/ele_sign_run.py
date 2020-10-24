from auto_reply.package import *
from robot.models import pubEleSignUsers, pubEleSignInfo

class my_thread(threading.Thread):
    def __init__(self, openId, state):
        threading.Thread.__init__(self)
        self.openId = openId
        self.state = state
    def run(self):
        send_sign(self.openId, self.state)
def send_sign_index(openId, state):
    th = my_thread(openId, state)  # id, name
    th.start()

def send_sign(openId, state):
    sign_txt(openId, "正在为您签到，请稍后..")
    if state:
        ele_values = pubEleSignUsers.objects.filter(state=True, is_bind=True)
        values = ele_values
    else:
        ele_values = pubEleSignUsers.objects.filter(wx_open_id=openId)
        values = ele_values
    if values:
        for v in values:
            sid, users_id = v.sid, v.user_id
            results = sign(sid, users_id)
            # print(results)
            if type(results).__name__ == 'list':
                wx_str = '【{}饿了么签到结果：签到成功】\n\n今日签到红包领取如下：\n'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
                v.is_sign = True
                v.save()
                for r in range(len(results)):
                    r_str = '{}.{}\n'.format(r + 1, results[r])
                    wx_str += r_str
                result = cx_sign(sid, users_id)
                wx_str += result
            else:
                wx_str = '【{}饿了么签到结果：{}】'.format(datetime.datetime.now().strftime('%Y-%m-%d'), results)
                if results == '未登录':
                    dl_str = '\n\n身份验证过期了，请在公众号进入饿了么自动签到功能发送数字“2”重新发送手机号绑定'
                    wx_str += dl_str
                if '昨天还没有签到' in results:
                    dl_str = '\n\n请今天去APP手动签到下，明天即可正常签到了哦'
                    wx_str += dl_str
                if '签到失败' in results:
                    dl_str = '\n\n请确认今天是否已手动签到过哦，若没有请去APP手动签到下试试'
                    wx_str += dl_str
            eleInfo = pubEleSignInfo()
            eleInfo.wx_open_id = openId
            eleInfo.sign_info = wx_str.strip()
            eleInfo.save()
            sign_txt(openId, wx_str)
    else:
        send_fqq('未找到签到用户')

def sign(sid, users_id):
    headers = {
        'User-Agent': 'Rajax/1 16th/meizu_16th_CN Android/8.1.0 Display/Flyme_8.0.0.0A Eleme/8.27.4 Channel/meizu ID/db0f7c28-eb3d-3548-97c0-196205639927; KERNEL_VERSION:4.9.65-perf+ API_Level:27 Hardware:6c8be58e32dfebacddf1a397548ad297 Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; 16th Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.27.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    sign_url = 'https://h5.ele.me/restapi/member/v2/users/{}/sign_in'.format(users_id)
    dict = {
        "channel":"app",
        "captcha_code":"",
        "source":"main",
        "longitude":"119.21204097568989",
        "latitude":"26.037406884133816"
    }
    try:
        sign_r = requests.post(sign_url, headers=headers, json=dict, verify=False)
        # print(sign_r.text)
        def fanpai():
            try:
                url = 'https://h5.ele.me/restapi/member/v2/users/{}/sign_in/daily/prize'.format(users_id)
                dict1 = {
                    "channel":"app",
                    "index":randint(0, 2),
                    "longitude":"119.21204097568989",
                    "latitude":"26.037406884133816"
                }
                fanp_r = requests.post(url, headers=headers, json=dict1, verify=False)
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
                write_log(3, '{}'.format(traceback.format_exc()))
                return "翻牌出错了"
        def fenx():
            try:
                url = 'https://h5.ele.me/restapi/member/v1/users/{}/sign_in/wechat'.format(users_id)
                dict2 = {
                    "channel":"app"
                }
                r = requests.post(url, headers=headers, json=dict2, verify=False)
                return r
            except:
                write_log(3, '{}'.format(traceback.format_exc()))
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
            write_log(3, '{}'.format(sign_r.json()))
            message = sign_r.json()['message']
            return message
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        return "签到失败，请手动签到试试"

def cx_sign(sid, users_id):
    headers = {
        'User-Agent': 'Rajax/1 16th/meizu_16th_CN Android/8.1.0 Display/Flyme_8.0.0.0A Eleme/8.27.4 Channel/meizu ID/db0f7c28-eb3d-3548-97c0-196205639927; KERNEL_VERSION:4.9.65-perf+ API_Level:27 Hardware:6c8be58e32dfebacddf1a397548ad297 Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; 16th Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.27.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        url = 'https://h5.ele.me/restapi/member/v1/users/{}/sign_in/info?longitude=119.21204097568989&latitude=26.037406884133816'.format(users_id)
        r = requests.get(url, headers=headers, verify=False)
        if r.status_code == 200:
            statuses = r.json()['statuses']
            num = 0
            for s in statuses:
                if s == 1:
                    num += 1
            return '--你已签到{}天'.format(num)
        else:
            write_log(3, '{}'.format(r.json()))
            return "--查询已签天数异常"
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        return "--查询已签天数异常"