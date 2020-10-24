import traceback
from config.config import *
import sqlite3

def cb_hongbao(group_sn, owner_id, alink, puid, beizhu, wxmsg, logger):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标

def set_sid(mobile, sms_url, ):
    pass