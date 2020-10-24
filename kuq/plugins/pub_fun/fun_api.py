import logging.handlers
import re
import requests
import traceback
import time
from threading import Thread
from random import randint
from plugins.pub_fun.sql_all import MysqlSearch as SQL

LOG_FILE = r'qqBot.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('qqBot')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

def bind_wx(text, qq):
    bd_str = '恭喜你，和公众号(最趣分享)绑定成功！'
    values = SQL().select_bind_users(text)
    if values:
        if values[0][1]:
            bz_values = SQL().select_bind_users_qq(qq, text)
            if bz_values:
                bd_str = "你已绑定过公众号(最趣分享)，无法再次绑定！"
            else:
                if values[0][2] == None:
                    value_list = SQL().set_binds(text, values[0][0], qq)
                    if value_list[0] and not value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到，每天的签到结果我会发送给您哦".format(bd_str)
                    if value_list[1] and not value_list[0]:
                        bd_str = "{}\n\n若您在公众号开启打卡提醒，每天到点我会通知您打卡哦".format(bd_str)
                    if value_list[0] and value_list[1]:
                        bd_str = "{}\n\n若您在公众号开启饿了么签到和打卡提醒，每天的签到结果和到点打卡我都会发送给您哦".format(bd_str)
                else:
                    bd_str = "该绑定信息已绑定过公众号(最趣分享)，你无法再次绑定！"
        else:
            bz_values = SQL().select_bind_users_qq(qq, text)
            if bz_values:
                bd_str = "你已绑定过公众号(最趣分享)，无法再次绑定！"
            else:
                if values[0][2] == None:
                    value_list = SQL().set_binds(text, values[0][0], qq)
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