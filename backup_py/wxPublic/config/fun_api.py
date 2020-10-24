import logging.handlers
from package import *


LOG_FILE = r'config\wx_public.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('wxPublic')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

def del_video_shuiy(link):
    try:
        url = 'https://analyse.layzz.cn//lyz/miniMsgUnLoadAnalyse'
        headers = {
            'Referer': 'https://appservice.qq.com/1110141096/1.0.0/page-frame.html',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 QQ/MiniApp',
            'content-type': 'application/json',
            'Host': 'analyse.layzz.cn'
        }
        dict = {
            "code": "060bf7148abefedc4538b360e184e142",
            "programType": 88,
            "link": link,
            "nickName": "",
            "avatarUrl": "",
            "reqSource": 1
        }
        r = requests.post(url, headers=headers, json=dict)
        if r.json()["message"] == '操作成功':
            result = {'status': 0, 'message': r.json()['data']['playAddr']}
            return result
        else:
            result = {'status': 1, 'message': r.json()['message']}
            return result
    except:
        write_log(3, traceback.format_exc())
        result = {'status': -1, 'message': '抱歉，系统出现异常，请稍后重试...'}
        return result

def get_garbage_name(text):
    try:
        url = 'https://api.66mz8.com/api/garbage.php?key={}'.format(text)
        r = requests.get(url)
        if r.json()["code"] == 200:
            result = {'status': 0, 'message': '{}属于“{}”'.format(r.json()['key'], r.json()['data'])}
            return result
        else:
            result = {'status': 1, 'message': r.json()['msg']}
            return result
    except:
        write_log(3, traceback.format_exc())
        result = {'status': -1, 'message': '抱歉，系统出现异常，请稍后重试...'}
        return result

def short_url(urls):
    url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=short_url&need_short_url=1&url={}"
    try:
        r = requests.get(url.format(urls))
        if 'ok' in r.text and 'short_url' in r.text:
            short_url = re.findall('"short_url" : "(.*?)"', r.text)[0]
            return short_url
        else:
            return -1
    except:
        write_log(3, traceback.format_exc())
        return -1

def send_fqq(message):
    try:
        dict = {"user_id": 541116212,
                "message": message}
        r = requests.post("http://127.0.0.1:5700/send_private_msg", data=dict)
        if r.json()['status'] == "ok":
            return True
        else:
            return False
    except:
        return False

def write_log(level, text):
    if level == 1:
        logger.info(text)
    elif level == 2:
        logger.debug(text)
    else:
        logger.error(text)