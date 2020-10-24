import logging.handlers
import requests
import traceback
import re
import os
import string, random
# import win32gui
from wxpy import *
from auto_reply.config.config import ELMME_SIGN_TXT, QQ_WZ_GROUPS, ERROR_QQ, QR_IMG_PATH
from robot.models import pubBindUsers, pubCardUsers, pubEleSignUsers
from io import BytesIO
from PIL import Image

INFO_LOG_FILE = r'auto_reply/config/info.log'
handler_info = logging.handlers.RotatingFileHandler(INFO_LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt_info = '%(asctime)s - %(levelname)s - %(message)s'
formatter_info = logging.Formatter(fmt_info)  # 实例化formatter
handler_info.setFormatter(formatter_info)  # 为handler添加formatter
logger_info = logging.getLogger('wxPublic_info')  # 获取名为tst的logger
logger_info.addHandler(handler_info)  # 为logger添加handler
logger_info.setLevel(logging.DEBUG)

ERROR_LOG_FILE = r'auto_reply/config/error.log'
handler_error = logging.handlers.RotatingFileHandler(ERROR_LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt_error = '%(asctime)s - %(levelname)s - %(message)s'
formatter_error = logging.Formatter(fmt_error)  # 实例化formatter
handler_error.setFormatter(formatter_error)  # 为handler添加formatter
logger_error = logging.getLogger('wxPublic_error')  # 获取名为tst的logger
logger_error.addHandler(handler_error)  # 为logger添加handler
logger_error.setLevel(logging.DEBUG)

# 获取随机绑定别名
def get_bind_name(openId, num):
    # num为检测绑定另一业务前是否已经在其他业务上绑定过了，如果绑过了就直接更新绑过的微信备注名
    bind_str = '复制这条信息，${}$，发送给机器人即可完成绑定\n\n[必看]机器人绑定教程：https://url.cn/5VXTApU'
    up_value = None
    values = pubBindUsers.objects.filter(wx_open_id=openId)
    if values.exists():
        value = values[0]
        passwd = value.bind_name
        if value.is_bind:
            if num == 1:
                up_values = pubCardUsers.objects.filter(wx_open_id=openId)
                if up_values.exists():
                    up_value = up_values[0]
            if num == 2:
                up_values = pubEleSignUsers.objects.filter(wx_open_id=openId)
                if up_values.exists():
                    up_value = up_values[0]
            if value.wx_note != None and value.qq == None:
                if up_value != None:
                    if up_value.wx_note == None:
                        up_value.bind_name = passwd
                        up_value.wx_note = value.wx_note
                        up_value.save()
                bind_str = '你已绑定微信，还可绑定QQ\n\n{}'.format(bind_str.format(passwd))
            if value.qq != None and value.wx_note == None:
                if up_value != None:
                    if up_value.qq == None:
                        up_value.bind_name = passwd
                        up_value.qq = value.qq
                        up_value.save()
                bind_str = '你已绑定QQ，还可绑定微信\n\n{}'.format(bind_str.format(passwd))
            if value.wx_note != None and value.qq != None:
                if up_value != None:
                    if up_value.wx_note == None and up_value.qq == None:
                        up_value.bind_name = passwd
                        up_value.wx_note = value.wx_note
                        up_value.qq = value.qq
                        up_value.save()
                bind_str = '你已绑定微信和QQ，无需再次绑定'
        else:
            bind_str = bind_str.format(passwd)
    else:
        passwd = random.sample(string.ascii_letters + string.digits, 8)
        passwd = ''.join(passwd)
        values = pubBindUsers.objects.filter(bind_name=passwd)
        if values.exists():
            passwd = random.sample(string.ascii_letters + string.digits, 8)
            passwd = ''.join(passwd)
        else:
            pub = pubBindUsers()
            pub.bind_name = passwd
            pub.wx_open_id = openId
            pub.save()
            bind_str = bind_str.format(passwd)
    return bind_str

# # 获取任务里谷歌浏览器数量
# def get_chromes():
#     hwnd_title = dict()
#     num = 0
#     def get_all_hwnd(hwnd, mouse):
#         if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
#             hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
#     win32gui.EnumWindows(get_all_hwnd, 0)
#     for h, t in hwnd_title.items():
#         if t is not "":
#             if "Google Chrome" in t:
#                 num += 1
#     return num

# 获取图片分辨率
def get_size(urls):
    try:
        response = requests.get(urls)
        f = BytesIO(response.content)
        img = Image.open(f)
        return img.size
    except:
        write_log(3, traceback.format_exc())
        return "(0, 0)"

# 写入签到信息
def sign_txt(openId, text):
    with open("{}/{}.txt".format(ELMME_SIGN_TXT, openId), "a", encoding='gbk') as f:
        f.write(text.strip() + "\n-------------\n")

# 下载壁纸
def down_wall(skin_name, skin_url, mob_skin_url, hero_name, game, skin_size):
    try:
        if game == 'wzry':
            save_path = r'static/wall/wzry/{}'
        elif game == 'yxlm':
            save_path = r'static/wall/yxlm/{}'
        else:
            save_path = r'static/wall'
        if '掌盟#' in hero_name:
            hero_name = "掌盟壁纸合集"
        hero_path = save_path.format(hero_name)
        folder = os.path.exists(hero_path)
        if not folder:
            os.makedirs(hero_path)
        if '/' in skin_name:
            skin_name = skin_name.replace('/', '')
        if '\\' in skin_name:
            skin_name = skin_name.replace('\\', '')
        if game == 'yxlm':
            if skin_size != None:
                skin_path = r'{}/{} {}.jpg'.format(hero_path, skin_name, skin_size)
            else:
                skin_path = r'{}/{}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(skin_path):
                img = requests.get(skin_url)
                with open(skin_path, "wb") as f:
                    f.write(img.content)
        elif game == 'wzry':
            skin_path = r'{}/[电脑] {}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(skin_path):
                if skin_url != None:
                    img = requests.get(skin_url)
                    with open(skin_path, "wb") as f:
                        f.write(img.content)
            mob_skin_path = r'{}/[手机] {}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(mob_skin_path):
                if mob_skin_url != None:
                    img = requests.get(mob_skin_url)
                    with open(mob_skin_path, "wb") as f:
                        f.write(img.content)
        else:
            pass
    except:
        write_log(3, traceback.format_exc())

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
        result = {'status': -1, 'message': '抱歉，系统出现异常，请稍后重试'}
        return result

def get_garbage_name(text):
    try:
        # url = 'https://api.66mz8.com/api/garbage.php?key={}'.format(text)
        url = 'https://tenapi.cn/laji/?keyword={}'.format(text)
        r = requests.get(url)
        if r.json()["msg"] == "查询成功！":
            result = {'status': 0, 'message': '{}属于“{}”'.format(text, r.json()['data'])}
            return result
        else:
            result = {'status': 1, 'message': r.json()['msg']}
            return result
    except:
        write_log(3, traceback.format_exc())
        result = {'status': -1, 'message': '抱歉，系统出现异常，请稍后重试'}
        return result

def qr_url(text, times):
    try:
        url = 'https://tenapi.cn/qr?txt={}'.format(text)
        r = requests.get(url)
        if r.status_code == 200:
            with open(r"{}/{}.png".format(QR_IMG_PATH, times).format(r), "wb") as f:
                f.write(r.content)
            return True
        else:
            return False
    except:
        write_log(3, traceback.format_exc())
        return False

# def short_url(urls):
#     url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=short_url&need_short_url=1&url={}"
#     try:
#         r = requests.get(url.format(urls))
#         if 'ok' in r.text and 'short_url' in r.text:
#             short_url = re.findall('"short_url" : "(.*?)"', r.text)[0]
#             if len(short_url) == 0:
#                 return "生成短网址错误，确认网址正确"
#             return short_url
#         else:
#             return -1
#     except:
#         write_log(3, traceback.format_exc())
#         return -1

# 转换短网址 腾讯的转换失败就转成新浪
def short_url_new(urls):
    # short_link = short_url(urls)
    # if short_link != -1:
    #     return short_link
    # else:
    #     short_link = short_turl(urls)
    #     if short_link != -1:
    #         return short_link
    #     else:
    #         return urls

    short_link = short_souurl(urls)
    if short_link != -1:
        return short_link
    else:
        return urls

def short_souurl(urls):
    url = "http://suo.im/api.htm?url={}&key=5d68979fb1a9c70269346191@8b1adc61fdc362158a352a191513e054&expireType=6".format(urls)
    try:
        r = requests.get(url).text
        return r
    except:
        write_log(3, traceback.format_exc())
        return -1

def short_url(urls):
    url = "http://shorturl.8446666.sojson.com/qq/shorturl?url={}"
    try:
        r = requests.get(url.format(urls))
        if r.json()["status"] == 200:
            short_url = r.json()["shorturl"]
            return short_url
        else:
            write_log(3, r.text)
            return -1
    except:
        write_log(3, traceback.format_exc())
        return -1

def short_turl(urls):
    url = "http://shorturl.8446666.sojson.com/sina/shorturl?url={}"
    try:
        r = requests.get(url.format(urls))
        if r.json()["status"] == 200:
            short_url = r.json()["shorturl"]
            return short_url
        else:
            write_log(3, r.text)
            return -1
    except:
        write_log(3, traceback.format_exc())
        return -1

# def short_turl(urls):
#     url = 'https://service.weibo.com/share/share.php?url={}&pic=pic&appkey=key&title={}'.format(urls, urls)
#     try:
#         r = requests.get(url)
#         r.encoding = 'utf-8'
#         if 'scope.short_url' in r.text:
#             short_url = re.findall('scope.short_url = "(.*?)";', r.text, re.S)[0].strip()
#             if len(short_url) == 0:
#                 return "生成短网址错误，确认网址正确"
#             return short_url
#         else:
#             return -1
#     except:
#         write_log(3, traceback.format_exc())
#         return -1

def send_fqq(message):
    try:
        dict = {"user_id": ERROR_QQ,
                "message": message}
        r = requests.post("http://127.0.0.1:5700/send_private_msg", data=dict)
        if r.json()['status'] == "ok":
            return True
        else:
            return False
    except:
        write_log(3, traceback.format_exc())
        return False

def send_fqq_group(message):
    message = message.replace('|', '\n')
    try:
        dict = {"group_id": QQ_WZ_GROUPS,
                "message": message}
        r = requests.post("http://127.0.0.1:5700/send_group_msg", data=dict)
        if r.json()['status'] == "ok":
            return True
        else:
            return False
    except:
        write_log(3, traceback.format_exc())
        return False

# def send_fwx_group(names, message, type):
#     try:
#         bot = Bot(cache_path=WXBOT_PATH)
#         if type:
#             wxpy_groups = bot.groups().search(names)
#             if wxpy_groups:
#                 wxpy_groups[0].send(message)
#                 write_log(1, '发送了微信消息[{}]给[{}]'.format(message, names))
#             else:
#                 write_log(3, '未找到接收者名字{}'.format(wxpy_groups))
#         else:
#             my_friend = bot.friends().search(names)
#             if my_friend:
#                 if len(my_friend) == 1:
#                     my_friend[0].send(message)
#                 else:
#                     for f in my_friend:
#                         f_str = re.findall(':(.*?)>', str(f))[0].strip()
#                         if names == f_str:
#                             f.send(message)
#                 write_log(1, '发送了微信消息[{}]给[{}]'.format(message, names))
#             else:
#                 write_log(3, '未找到接收者名字{}'.format(my_friend))
#     except:
#         write_log(3, '微信消息发送异常 - {}'.format(traceback.format_exc()))

def write_log(level, text):
    if level == 1:
        logger_info.info(text)
    elif level == 2:
        logger_error.debug(text)
    else:
        logger_error.error(text)

def fangtang(title, content):
    api = "https://sc.ftqq.com/SCU38261T75506f6dfae8ea68797927f27f59830e5c2340b46b2f6.send"
    data = {
        # "sendkey": "7639-5d73449e8a2a1db47195cfc57210c07a",
        "text": title,
        "desp": content
    }
    try:
        res = requests.post(api, data=data)
        if res.status_code == 200:
            pass
        else:
            print('发送失败')
    except:
        print('Error: 发送出错')