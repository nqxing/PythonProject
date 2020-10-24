import logging.handlers
import re
import requests
import time
import traceback
import threading
from random import randint  # 随机函数
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pymysql
from threading import Thread
import os
from config.config import *
from config.sql_all import MysqlSearch as SQL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bypy import ByPy

LOG_FILE = r'config/wxBot.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('wxBot')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

# 写入签到信息
def sign_txt(openId, text):
    with open("{}.txt".format(ELMME_SIGN_TXT.format(openId)), "a", encoding='gbk') as f:
        f.write(text.strip() + "\n-------------\n")

def send_qq_private(qq, msg):
    dict = {"user_id": qq,
            "message": msg}
    r = requests.post("http://127.0.0.1:5700/send_private_msg", data=dict)
    if r.json()['status'] == "ok":
        pass

def bind_wx(text, beizhu, msg):
    bd_str = '恭喜你，和公众号(最趣分享)绑定成功！'
    bz_state = False
    if 'vip_' in beizhu[0]:
        bz = beizhu[0]
    else:
        num = int(SQL().select_var_info('WX_VIP_NUM'))
        bz = 'vip_{}'.format(num)
        bz_state = True
    values = SQL().select_bind_users(text)
    if values:
        if values[0][1]:
            bz_values = SQL().select_bind_users_bz(bz, text)
            if bz_values:
                bd_str = "你已绑定过公众号(最趣分享)，无法再次绑定！"
            else:
                if values[0][2] == None:
                    value_list = SQL().set_binds(text, values[0][0], bz)
                    if value_list[0] and not value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到，每天的签到结果我会发送给您哦".format(bd_str)
                    if value_list[1] and not value_list[0]:
                        bd_str = "{}\n\n若您在公众号开启打卡提醒，每天到点我会通知您打卡哦".format(bd_str)
                    if value_list[0] and value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到和打卡提醒，每天的签到结果和到点打卡我都会发送给您哦".format(bd_str)
                else:
                    bd_str = "该绑定信息已绑定过公众号(最趣分享)，你无法再次绑定！"
        else:
            bz_values = SQL().select_bind_users_bz(bz, text)
            if bz_values:
                bd_str = "你已绑定过公众号(最趣分享)，无法再次绑定！"
            else:
                if bz_state:
                    write_log(1, '设置了新备注{}'.format(bz))
                    msg.sender.set_remark_name(bz)
                    num = int(SQL().select_var_info('WX_VIP_NUM'))
                    num += 1
                    SQL().up_var_info('WX_VIP_NUM', num)
                if values[0][2] == None:
                    value_list = SQL().set_binds(text, values[0][0], bz)
                    if value_list[0] and not value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到，每天的签到结果我会发送给您哦".format(bd_str)
                    if value_list[1] and not value_list[0]:
                        bd_str = "{}\n\n若您在公众号开启打卡提醒，每天到点我会通知您打卡哦".format(bd_str)
                    if value_list[0] and value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到和打卡提醒，每天的签到结果和到点打卡我都会发送给您哦".format(bd_str)
                else:
                    bd_str = "该绑定信息已绑定过公众号(最趣分享)，你无法再次绑定！"
    else:
        bd_str = "绑定码无效，和公众号(最趣分享)绑定失败！"
    return bd_str

def write_log(level, text):
    if level == 1:
        logger.info(text)
    elif level == 2:
        logger.debug(text)
    else:
        logger.error(text)

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