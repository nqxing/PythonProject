import sqlite3
from config.config import ELEME_DATA_PATH, HOST, USER, PWD, DEFAULT_HB_TIME, IS_HTTPS, ID_MAX, XH_MAX
from eleme.hongbao.hongbao_cx import cx_hongbao
import datetime
import pymysql
import time
import logging.handlers

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序
def jk_fover_hongbao(mysql_cursor, mysql_conn, cursor, conn, group_sn, bianhao, alink, hongbaoMax, dahao, uid):
    mysql_cursor.execute('''select * from eleme_id WHERE id = {} '''.format(uid)) #查找饿了么库里的账号表，目前只取第一个账号
    values = mysql_cursor.fetchall()
    phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], values[0][5]
    # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
    result = cx_hongbao(phone, link, sign, sid, group_sn)
    if result['status'] == 0:
        hongbao = len(result['value']['promotion_records'])
        if hongbao < hongbaoMax - 1:
            mysql_cursor.execute(
                "UPDATE eleme_group_sn SET yet = {}, up_times = '{}', is_send = 'no' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
            mysql_conn.commit()
            mysql_cursor.execute(
                "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
            mysql_conn.commit()
        elif hongbao == hongbaoMax - 1:
            mysql_cursor.execute(
                "UPDATE eleme_group_sn SET yet = {}, up_times = '{}' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
            mysql_conn.commit()
            mysql_cursor.execute(
                '''select is_send from eleme_group_sn WHERE group_sn = '{}' '''.format(
                    group_sn))  # 查找饿了么库里的账号表，目前只取第一个账号
            values = mysql_cursor.fetchall()
            if values[0][0] == 'no':
                msg = '【红包{}】下一个就是最佳手气红包，快去点开领取吧'.format(bianhao)
                if '&amp;' in alink:
                    alink = alink.replace('&amp;', '&')
                dahao.send(msg)
                dahao.send(alink)
                mysql_cursor.execute(
                    "UPDATE eleme_group_sn SET is_send = 'yes' WHERE group_sn = '{}'".format(group_sn))
                mysql_conn.commit()
        elif hongbao == hongbaoMax:
            is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
            if is_lucky:
                lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                mysql_conn.commit()
                cursor.execute(
                    "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'over')".format(
                        bianhao, lucky_name, lucky_amount, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
        elif hongbao > hongbaoMax:
            promotion_records = result['value']['promotion_records']
            for p in promotion_records:
                is_lucky = p['is_lucky']  # 减一是数组从0开始读
                if is_lucky:
                    lucky_name = p['sns_username']
                    lucky_amount = p['amount']
                    mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                    mysql_conn.commit()
                    cursor.execute(
                        "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'over')".format(
                            bianhao, lucky_name, lucky_amount,
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    break
    elif result['status'] == 1:
        mysql_cursor.execute(
            "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
        mysql_conn.commit()
    elif result['status'] == 2 or result['status'] == -1:
        mysql_cursor.execute(
            '''select retry_num from eleme_group_sn WHERE group_sn = '{}' '''.format(
                group_sn))  # 查找饿了么库里的账号表，目前只取第一个账号
        values = mysql_cursor.fetchall()
        if values[0][0] == None:
            mysql_cursor.execute(
                "UPDATE eleme_group_sn SET retry_num = 1 WHERE group_sn = '{}'".format(group_sn))
            mysql_conn.commit()
        else:
            mysql_cursor.execute(
                "UPDATE eleme_group_sn SET retry_num = {} WHERE group_sn = '{}'".format(values[0][0]+1, group_sn))
            mysql_conn.commit()
            if values[0][0] > 7:
                mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                mysql_conn.commit()

def jk_over_hongbao(dahao):
    LOG_FILE = r'log\eleme_over.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5,
                                                   encoding='utf-8')  # 实例化handler
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger('eleme_over')  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)

    mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标

    print('过期红包监控系统运行中...')
    while True:
        mysql_cursor.execute('''select id from eleme_id WHERE is_sx = '身份信息正常' and id between 1 and 9''') #查找饿了么库里的账号表，目前只取第一个账号
        zhengc_ids = list(mysql_cursor.fetchall())
        mysql_cursor.execute(
            '''select bianhao, group_sn, yet_max, alink from eleme_group_sn WHERE state = 'yes' ''')  # 查找饿了么库里的账号表，目前只取第一个账号
        renws = mysql_cursor.fetchall()

        if len(renws) > len(zhengc_ids):
            a = len(renws) // len(zhengc_ids)
            b = len(renws) % len(zhengc_ids)
            new_ids = zhengc_ids * a
            for i in range(b):
                new_ids.append(zhengc_ids[i])
            if len(new_ids) == len(renws):
                for i in range(len(renws)):
                    jk_fover_hongbao(mysql_cursor, mysql_conn, cursor, conn, renws[i][1], renws[i][0], renws[i][3], renws[i][2], dahao, new_ids[i][0])
            logger.info('过期红包状态更新完毕，本次更新了{}个红包'.format(len(renws)))
        else:
            for i in range(len(renws)):
                jk_fover_hongbao(mysql_cursor, mysql_conn, cursor, conn, renws[i][1], renws[i][0], renws[i][3], renws[i][2], dahao, zhengc_ids[i][0])
            logger.info('过期红包状态更新完毕，本次更新了{}个红包'.format(len(renws)))
        time.sleep(60)