from config.fangtang import fangtang
import sqlite3
import re
import requests
import time
from config.config import ELEME_DATA_PATH, HOST, USER, PWD, DEFAULT_HB_TIME, IS_HTTPS, ID_MAX, XH_MAX
from eleme.hongbao.hongbao_cx import cx_hongbao
from eleme.hongbao.hongbao_lucky import lucky_hongbao
from eleme.login.mobile_send_code import mobile_send_code
import traceback
import datetime
import pymysql

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序
def jk_fqq_hongbao(group_sn, bianhao, alink, group, dahao, hz_group, logger, uid, is_db):
    try:
        hb_time = DEFAULT_HB_TIME
        num_url = 'https://h5.ele.me/restapi/marketing/themes/3971/group_sns/{}'.format(group_sn)  # 获取最大红包数链接
        hongbaoMax = requests.get(num_url, verify=False if IS_HTTPS else None).json()['lucky_number']
        logger.info('【红包{}】的最佳手气红包为第{}个'.format(bianhao, hongbaoMax))
        k = True
        if hongbaoMax != None:
            # uid = randint(1, 9)
            e, z, h, j = True, True, True, True
            x = -1  # 控制红包监控语句打印，确保只在有人点了红包后才进行打印输出
            num = 1
            xh_id = 10
            mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
            mysql_cursor = mysql_conn.cursor()  # 获取游标

            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
            cursor = conn.cursor()  # 获取游标

            mysql_cursor.execute('''select * from eleme_id WHERE id = {} '''.format(uid)) #查找饿了么库里的账号表，目前只取第一个账号
            values = mysql_cursor.fetchall()
            phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], values[0][5]
            # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
            begin_time = int(time.time())  # 获取运行该脚本时的时间戳

            if is_db:
                mysql_cursor.execute(
                    "INSERT INTO eleme_group_sn (bianhao, group_sn, yet, yet_max, alink, state, wx_beizhu, add_times) VALUES ('{}', '{}', 0, {}, '{}', 'no', '红包互助群', '{}')".format(
                        bianhao, group_sn, hongbaoMax,
                        alink, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                mysql_conn.commit()

            while True:
                result = cx_hongbao(phone, link, sign, sid, group_sn)
                if result['status'] == 0:
                    hongbao = len(result['value']['promotion_records'])
                    if hongbao < hongbaoMax - 1:
                        if hongbao > x:
                            logger.info('【红包{}】使用了[{}]账号进行监控'.format(bianhao, phone))
                            logger.info('【红包{}】监控中，当前已有{}人领取'.format(bianhao, hongbao))
                            mysql_cursor.execute(
                                "UPDATE eleme_group_sn SET yet = {}, up_times = '{}' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                            mysql_conn.commit()
                            mysql_cursor.execute(
                                "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
                            mysql_conn.commit()
                            x = hongbao  # 查到最新红包已领取数量后赋值
                        t_run_time = int(time.time()) - begin_time
                        if t_run_time // 60 >= 180:
                            logger.info('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                            mysql_cursor.execute(
                                "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                            mysql_conn.commit()
                            wx_msg = '【红包{}】监控已达3小时，当前已领取{}/{}\n\n{}'.format(bianhao, hongbao, hongbaoMax, alink)
                            hz_group.send(wx_msg)
                            k = False
                            break
                        if hongbao <= hongbaoMax - 3:
                            time.sleep(17)
                    elif hongbao == hongbaoMax - 1:
                        if z:
                            cursor.execute("select lucky_me from eleme_lucky WHERE id = 1")
                            lucky_status = cursor.fetchall()[0][0]
                            logger.info('【红包{}】监控中，当前已有{}人领取'.format(bianhao, hongbao))
                            msg = '【红包{}】下一个就是最佳手气红包，快去点开领取吧'.format(bianhao)
                            if lucky_status == 'yes':
                                if '&amp;' in alink:
                                    alink = alink.replace('&amp;', '&')
                                dahao.send(msg)
                                dahao.send(alink)
                            else:
                                if '&amp;' in alink:
                                    alink = alink.replace('&amp;', '&')
                                group.send(msg)
                                group.send(alink)
                            logger.info('【红包{}】下一个就是最佳手气红包，快去点开领取吧，{}'.format( bianhao, alink))
                            z = False
                    elif hongbao == hongbaoMax:
                        is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                        if num == 1 and is_lucky:
                            logger.info('【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(bianhao))
                            break
                        elif num > 1 and z == False:
                            if is_lucky:
                                lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                                lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                                lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                cursor.execute("select lucky_me from eleme_lucky WHERE id = 1")
                                lucky_status = cursor.fetchall()[0][0]
                                if lucky_status == 'yes':
                                    dahao.send(lucky_msg)
                                else:
                                    group.send(lucky_msg)

                                cursor.execute(
                                    "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'qq')".format(
                                        bianhao, lucky_name, lucky_amount, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                conn.commit()

                                reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, re.sub(reg, '', lucky_name), lucky_amount)
                                logger.info(lucky_msg_info)

                                break
                            else:
                                if e:
                                    msg = '【红包{}】最佳手气红包还未产生，快去点开领取吧'.format(bianhao)
                                    cursor.execute("select lucky_me from eleme_lucky WHERE id = 1")
                                    lucky_status = cursor.fetchall()[0][0]
                                    if lucky_status == 'yes':
                                        dahao.send(msg)
                                    else:
                                        group.send(msg)
                                    logger.info(msg)
                                    e = False
                        elif z and num > 1 and is_lucky:
                            lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                            lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                            logger.info('【红包{}】的最佳手气被[{}]领走了，金额{}元，请换个红包吧'.format(bianhao, lucky_name, lucky_amount))
                            break
                        elif z and is_lucky == False and num > 1:
                            if j:
                                msg = '【红包{}】最佳手气红包还未产生，快去点开领取吧'.format(bianhao)
                                cursor.execute("select lucky_me from eleme_lucky WHERE id = 1")
                                lucky_status = cursor.fetchall()[0][0]
                                if lucky_status == 'yes':
                                    dahao.send(msg)
                                    if '&amp;' in alink:
                                        alink = alink.replace('&amp;', '&')
                                    dahao.send(alink)
                                else:
                                    group.send(msg)
                                    if '&amp;' in alink:
                                        alink = alink.replace('&amp;', '&')
                                    group.send(alink)
                                logger.info(msg)
                                j = False
                    elif hongbao > hongbaoMax:
                        is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']
                        if num == 1 and is_lucky and z:
                            logger.info('【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(bianhao))
                            break
                        elif num > 1 and is_lucky and z:
                            lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                            lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                            logger.info('【红包{}】的最佳手气被[{}]领走了，金额{}元，请换个红包吧'.format(bianhao, lucky_name, lucky_amount))
                            break
                        elif num > 1 and is_lucky == False and z and j:
                            logger.info('【红包{}】该红包最佳为第{}个，已经领取了{}个，最佳还未出现，请换个红包吧'.format(bianhao, hongbaoMax, hongbao))
                            break
                        elif num > 1 and z == False or j == False:
                            promotion_records = result['value']['promotion_records']
                            if h == False:
                                break
                            for p in promotion_records:
                                is_lucky = p['is_lucky']  # 减一是数组从0开始读
                                if is_lucky:
                                    lucky_name = p['sns_username']
                                    lucky_amount = p['amount']
                                    lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                    cursor.execute("select lucky_me from eleme_lucky WHERE id = 1")
                                    lucky_status = cursor.fetchall()[0][0]
                                    if lucky_status == 'yes':
                                        dahao.send(lucky_msg)
                                    else:
                                        group.send(lucky_msg)

                                    cursor.execute(
                                        "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'qq')".format(
                                            bianhao, lucky_name, lucky_amount,
                                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                    conn.commit()

                                    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                    lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao,
                                                                                    re.sub(reg, '', lucky_name),
                                                                                    lucky_amount)
                                    logger.info(lucky_msg_info)
                                    h = False
                                    break
                        t_run_time = int(time.time()) - begin_time
                        if t_run_time // 60 >= 180:
                            logger.info('【红包{}】监控已达3小时，最佳手气还没查到，自动退出监控'.format(bianhao))
                            break
                    num += 1
                    time.sleep(hb_time)
                elif result['status'] == 1:
                    logger.info('【红包{}】 - {}身份信息过期，需重新验证'.format(bianhao, phone))
                    mysql_cursor.execute(
                        "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
                    mysql_conn.commit()
                    if uid == ID_MAX:
                        uid = 1
                    else:
                        uid += 1
                    mysql_cursor.execute('''select * from eleme_id WHERE id = {} '''.format(uid))  # 查找饿了么库里的账号表，目前只取第一个账号
                    values = mysql_cursor.fetchall()
                    phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], \
                                                      values[0][5]
                    logger.info('【红包{}】身份信息失效，现在更换手机号为{}监控'.format(bianhao, phone))
                elif result['status'] == 2:
                    logger.debug('【红包{}】 - 未知错误，{}'.format(bianhao, result['value']))
                    if result['value']['message'] == '领取失败，请刷新再试。':
                        mysql_cursor.execute('''select * from eleme_id WHERE id = {} '''.format(xh_id))  # 查找饿了么库里的账号表，目前只取第一个账号
                        values = mysql_cursor.fetchall()
                        phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], \
                                                          values[0][5]
                        logger.info('【红包{}】领取失败，请刷新再试。现在更换手机号为{}监控'.format(bianhao, phone))
                        if xh_id == XH_MAX:
                            xh_id = 10
                        else:
                            xh_id += 1
                    hb_time += 1
                    time.sleep(hb_time)
                    if hb_time > 15:
                        break
                elif result['status'] == -1:
                    logger.debug('【红包{}】 - {}'.format(bianhao, result['value']))
                    hb_time += 1
                    time.sleep(hb_time)
                    if hb_time > 15:
                        break
            if k:
                mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                mysql_conn.commit()
            run_time = int(time.time()) - begin_time
            logger.info('【红包{}】监控完毕~用时{}分{}秒，共查询了{}次'.format(bianhao, run_time//60, run_time%60, num))
        else:
            logger.info('【红包{}】识别出错，已退出监控'.format(bianhao))
    except:
        logger.info('【红包{}】Error : {}'.format(bianhao, traceback.format_exc()))