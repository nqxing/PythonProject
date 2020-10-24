import sqlite3
import requests
import time
import re
from config.config import ELEME_DATA_PATH, HOST, USER, PWD, DEFAULT_HB_TIME, IS_HTTPS, ID_MAX, XH_MAX
from eleme.hongbao.hongbao_cx import cx_hongbao
from eleme.login.mobile_send_code import mobile_send_code
import traceback
import datetime
import pymysql

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序

def jk_hongbao(group_sn, bianhao, alink, wxmsg, logger, bot):
    try:
        hb_time = DEFAULT_HB_TIME
        num_url = 'https://h5.ele.me/restapi/marketing/themes/3971/group_sns/{}'.format(group_sn)  # 获取最大红包数链接
        hongbaoMax = requests.get(num_url, verify=False if IS_HTTPS else None).json()['lucky_number']
        k = True
        if hongbaoMax != None:
            logger.info('{} - 【红包{}】的最佳手气红包为第{}个'.format(wxmsg.sender, bianhao, hongbaoMax))
            x = -1  # 控制红包监控语句打印，确保只在有人点了红包后才进行打印输出
            num = 1
            z = True

            mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
            mysql_cursor = mysql_conn.cursor()  # 获取游标

            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
            cursor = conn.cursor()  # 获取游标

            values = get_eleid()
            if values == '暂无可用账号':
                logger.info('当前已无饿了么可用账号，请赶紧添加')
            else:
                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], values[5]
                # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
                begin_time = int(time.time())  # 获取运行该脚本时的时间戳

                wx_beizhu = re.findall(':(.*?)>', str(wxmsg.sender))[0].strip()
                mysql_cursor.execute(
                    "INSERT INTO eleme_group_sn (bianhao, group_sn, yet, yet_max, alink, state, wx_beizhu, add_times) VALUES ('{}', '{}', 0, {}, '{}', 'no', '{}', '{}')".format(
                        bianhao, group_sn, hongbaoMax,
                        alink, wx_beizhu, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                mysql_conn.commit()

                cursor.execute("select text from eleme_text where id = 3")
                strs = cursor.fetchall()[0][0]
                if strs:
                    wxmsg.reply('【红包{}】福利天天领，复制这条信息{}，到[手机淘宝]立刻领红包'.format(bianhao, strs))
                while True:
                    result = cx_hongbao(phone, link, sign, sid, group_sn)
                    if result['status'] == 0:
                        if result['value']['promotion_records'] != None:
                            hongbao = len(result['value']['promotion_records'])
                            if hongbao < hongbaoMax - 1:
                                if x == -1:
                                    wxmsg.reply('【红包{}】监控中，该红包最佳手气为第{}个，当前已有{}人领取，请留意微信消息（注：红包监控周期为3小时，请记得将红包分享至人多的群聊中哦）'.format(bianhao, hongbaoMax, hongbao))
                                if hongbao > x:
                                    logger.info('{} - 【红包{}】使用了[{}]账号进行监控'.format(wxmsg.sender, bianhao, phone))
                                    logger.info('{} - 【红包{}】监控中，当前已有{}人领取'.format(wxmsg.sender, bianhao, hongbao))
                                    mysql_cursor.execute(
                                        "UPDATE eleme_group_sn SET yet = {}, up_times = '{}' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                    mysql_conn.commit()
                                    mysql_cursor.execute(
                                        "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
                                    mysql_conn.commit()
                                    x = hongbao  # 查到最新红包已领取数量后赋值
                                num += 1
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    mysql_cursor.execute(
                                        "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                    mysql_conn.commit()
                                    logger.info('{} - 【红包{}】监控已达3小时，系统将自动关闭监控'.format(wxmsg.sender, bianhao))
                                    k = False
                                    break
                                if hongbao <= hongbaoMax - 3:
                                    time.sleep(17)
                                    # logger.info('{} - 【红包{}】等待{}秒'.format(wxmsg.sender, bianhao, default_cxtime + 10))
                            elif hongbao == hongbaoMax - 1:
                                if z:
                                    logger.info('{} - 【红包{}】监控中，当前已有{}人领取'.format(wxmsg.sender, bianhao, hongbao))
                                    # msg = '【红包{}】下一个就是最佳手气红包，快去点开领取吧'.format(bianhao)
                                    msg = '【红包{}】下一个就是最佳手气红包，请翻阅消息点击源红包领取'.format(bianhao)
                                    wxmsg.reply(msg)
                                    # wxmsg.reply(alink)
                                    logger.info('{} - 【红包{}】下一个就是最佳手气红包，快去点开领取吧，{}'.format(wxmsg.sender, bianhao, alink))
                                    z = False
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    mysql_cursor.execute(
                                        "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                    mysql_conn.commit()
                                    logger.info('{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wxmsg.sender, hongbao, bianhao))
                                    # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                    k = False
                                    break
                                # break
                            elif hongbao > hongbaoMax - 1:
                                is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                                if num == 1 and is_lucky and z:
                                    logger.info('{} - 【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(wxmsg.sender, bianhao))
                                    wxmsg.reply('【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(bianhao))
                                    break
                                if num == 1 and is_lucky == False and z:
                                    logger.info('{} - 【红包{}】已领取{}个，但最佳手气还未产生，快去领取试试吧'.format(wxmsg.sender, bianhao, hongbao))
                                    wxmsg.reply('【红包{}】已领取{}个，但最佳手气还未产生，快去领取试试吧'.format(bianhao, hongbao))
                                    wxmsg.reply(alink)
                                    break
                                if num > 1 and z == False:
                                    if is_lucky:
                                        lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                                        lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                                        lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                        wxmsg.reply(lucky_msg)

                                        cursor.execute(
                                            "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'wx')".format(
                                                bianhao, lucky_name, lucky_amount, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                        conn.commit()

                                        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                        lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, re.sub(reg, '', lucky_name), lucky_amount)
                                        logger.info(lucky_msg_info)
                                        break
                                    else:
                                        promotion_records = result['value']['promotion_records']
                                        for p in promotion_records:
                                            is_lucky = p['is_lucky']  # 减一是数组从0开始读
                                            if is_lucky:
                                                lucky_name = p['sns_username']
                                                lucky_amount = p['amount']
                                                lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                                wxmsg.reply(lucky_msg)

                                                cursor.execute(
                                                    "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'wx')".format(
                                                        bianhao, lucky_name, lucky_amount,
                                                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                                conn.commit()

                                                reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                                lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao,
                                                                                                re.sub(reg, '', lucky_name),
                                                                                                lucky_amount)
                                                logger.info(lucky_msg_info)
                                                break
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 180:
                                    mysql_cursor.execute(
                                        "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                    mysql_conn.commit()
                                    logger.info('{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wxmsg.sender, bianhao, hongbao))
                                    # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                    k = False
                                    break
                            time.sleep(hb_time)
                        else:
                            logger.info('{} - 【红包{}】[{}]查询该红包数量为空了，{}'.format(wxmsg.sender, bianhao, phone, alink))
                            break
                    elif result['status'] == 1:
                        # if num == 1:
                        #     wxmsg.reply('系统正在调度账号中，请稍等')
                        logger.info('{} - 【红包{}】{}身份信息过期，需重新验证'.format(wxmsg.sender, bianhao, phone))
                        mysql_cursor.execute(
                                "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
                        mysql_conn.commit()
                        values = get_eleid()
                        if values:
                            phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                              values[5]
                            logger.info('{} - 【红包{}】身份信息失效，现在更换手机号为{}监控'.format(wxmsg.sender, bianhao, phone))
                        else:
                            logger.info('{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wxmsg.sender, bianhao))
                            break
                    elif result['status'] == 2:
                        logger.debug('{} - 未知错误，{}'.format(wxmsg.sender, result['value']))
                        if result['value']['message'] == '领取失败，请刷新再试。':
                            values = get_eleid()
                            if values:
                                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                                  values[5]
                                logger.info('{} - 【红包{}】领取失败，请刷新再试。现在更换手机号为{}监控'.format(wxmsg.sender, bianhao, phone))
                            else:
                                logger.info('{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wxmsg.sender, bianhao))
                                break
                        hb_time += 1
                        time.sleep(hb_time)
                        if hb_time > 15:
                            wxmsg.reply('【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                            break
                    elif result['status'] == -1:
                        logger.debug('{} - {}'.format(wxmsg.sender, result['value']))
                        hb_time += 1
                        time.sleep(hb_time)
                        if hb_time > 15:
                            wxmsg.reply('【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                            break
                run_time = int(time.time()) - begin_time
                logger.info('{} - 【红包{}】监控完毕~用时{}分{}秒，共查询了{}次'.format(wxmsg.sender, bianhao, run_time//60, run_time%60, num))
                if k:
                    mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                    mysql_conn.commit()
                    # wxmsg.reply('【红包{}】退出监控，用时{}分{}秒'.format(bianhao, run_time//60, run_time%60))
        else:
            logger.info('【红包{}】识别出错，已退出监控'.format(bianhao))
            wxmsg.reply('【红包{}】识别出错，已退出监控'.format(bianhao))
    except:
        logger.info('【红包{}】Error : {}'.format(bianhao, traceback.format_exc()))

def jk_db_hongbao(group_sn, bianhao, alink, wx_bz, logger, bot):
    try:
        hb_time = DEFAULT_HB_TIME
        num_url = 'https://h5.ele.me/restapi/marketing/themes/3971/group_sns/{}'.format(group_sn)  # 获取最大红包数链接
        hongbaoMax = requests.get(num_url, verify=False if IS_HTTPS else None).json()['lucky_number']
        k = True
        if hongbaoMax != None:
            logger.info('{} - 【红包{}】的最佳手气红包为第{}个'.format(wx_bz, bianhao, hongbaoMax))
            x = -1  # 控制红包监控语句打印，确保只在有人点了红包后才进行打印输出
            num = 1
            z = True

            mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
            mysql_cursor = mysql_conn.cursor()  # 获取游标

            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
            cursor = conn.cursor()  # 获取游标

            values = get_eleid()
            if values == '暂无可用账号':
                logger.info('当前已无饿了么可用账号，请赶紧添加')
            else:
                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], values[5]
                # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
                begin_time = int(time.time())  # 获取运行该脚本时的时间戳

                while True:
                    result = cx_hongbao(phone, link, sign, sid, group_sn)
                    if result['status'] == 0:
                        hongbao = len(result['value']['promotion_records'])
                        if hongbao < hongbaoMax - 1:
                            if hongbao > x:
                                logger.info('{} - 【红包{}】使用了[{}]账号进行监控'.format(wx_bz, bianhao, phone))
                                logger.info('{} - 【红包{}】监控中，当前已有{}人领取'.format(wx_bz, bianhao, hongbao))
                                mysql_cursor.execute(
                                    "UPDATE eleme_group_sn SET yet = {}, up_times = '{}' WHERE group_sn = '{}'".format(hongbao, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                mysql_conn.commit()
                                mysql_cursor.execute(
                                    "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
                                mysql_conn.commit()
                                x = hongbao  # 查到最新红包已领取数量后赋值
                            num += 1
                            t_run_time = int(time.time()) - begin_time
                            if t_run_time // 60 >= 180:
                                mysql_cursor.execute(
                                    "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                mysql_conn.commit()
                                logger.info('{} - 【红包{}】监控已达3小时，系统将自动关闭监控'.format(wx_bz, bianhao))
                                k = False
                                break
                            if hongbao <= hongbaoMax - 3:
                                time.sleep(17)
                                # logger.info('{} - 【红包{}】等待{}秒'.format(wxmsg.sender, bianhao, default_cxtime + 10))
                        elif hongbao == hongbaoMax - 1:
                            if z:
                                logger.info('{} - 【红包{}】监控中，当前已有{}人领取'.format(wx_bz, bianhao, hongbao))
                                # msg = '【红包{}】下一个就是最佳手气红包，快去点开领取吧'.format(bianhao)
                                msg = '【红包{}】下一个就是最佳手气红包，请翻阅消息点击源红包领取'.format(bianhao)
                                send_wxmsg(bot, wx_bz, msg)
                                # send_wxmsg(bot, wx_bz, alink)
                                logger.info('{} - 【红包{}】下一个就是最佳手气红包，快去点开领取吧，{}'.format(wx_bz, bianhao, alink))
                                z = False
                            t_run_time = int(time.time()) - begin_time
                            if t_run_time // 60 >= 180:
                                mysql_cursor.execute(
                                    "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                mysql_conn.commit()
                                logger.info('{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wx_bz, hongbao, bianhao))
                                # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                k = False
                                break
                            # break
                        elif hongbao > hongbaoMax - 1:
                            is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                            if num == 1 and is_lucky and z:
                                logger.info('{} - 【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(wx_bz, bianhao))
                                break
                            if num == 1 and is_lucky == False and z:
                                logger.info('{} - 【红包{}】已领取{}个，但最佳手气还未产生，快去领取试试吧'.format(wx_bz, bianhao, hongbao))
                                break
                            if num > 1 and z == False:
                                if is_lucky:
                                    lucky_name = result['value']['promotion_records'][hongbaoMax - 1]['sns_username']
                                    lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                                    lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                    send_wxmsg(bot, wx_bz, lucky_msg)
                                    cursor.execute(
                                        "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'wx')".format(
                                            bianhao, lucky_name, lucky_amount, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                    conn.commit()
                                    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                    lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, re.sub(reg, '', lucky_name), lucky_amount)
                                    logger.info(lucky_msg_info)
                                    break
                                else:
                                    promotion_records = result['value']['promotion_records']
                                    for p in promotion_records:
                                        is_lucky = p['is_lucky']  # 减一是数组从0开始读
                                        if is_lucky:
                                            lucky_name = p['sns_username']
                                            lucky_amount = p['amount']
                                            lucky_msg = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao, lucky_name, lucky_amount)
                                            send_wxmsg(bot, wx_bz, lucky_msg)
                                            cursor.execute(
                                                "INSERT INTO eleme_amount (bianhao, ename, amount, amount_time, esource) VALUES ('{}', '{}', '{}', '{}', 'wx')".format(
                                                    bianhao, lucky_name, lucky_amount,
                                                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                            conn.commit()

                                            reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                                            lucky_msg_info = '【红包{}】被[{}]抢走啦，金额为{}元'.format(bianhao,
                                                                                            re.sub(reg, '', lucky_name),
                                                                                            lucky_amount)
                                            logger.info(lucky_msg_info)
                                            break
                            t_run_time = int(time.time()) - begin_time
                            if t_run_time // 60 >= 180:
                                mysql_cursor.execute(
                                    "UPDATE eleme_group_sn SET state = 'yes', add_times = '{}' WHERE group_sn = '{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn))
                                mysql_conn.commit()
                                logger.info('{} - 【红包{}】监控已达3小时还未被领取，当前已领取{}个，系统将自动关闭监控'.format(wx_bz, bianhao, hongbao))
                                # wxmsg.reply('【红包{}】监控已达3小时，系统将自动关闭监控'.format(bianhao))
                                k = False
                                break
                        time.sleep(hb_time)
                    elif result['status'] == 1:
                        # if num == 1:
                        #     wxmsg.reply('系统正在调度账号中，请稍等')
                        logger.info('{} - 【红包{}】{}身份信息过期，需重新验证'.format(wx_bz, bianhao, phone))
                        mysql_cursor.execute(
                                "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
                        mysql_conn.commit()
                        values = get_eleid()
                        if values:
                            phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                              values[5]
                            logger.info('{} - 【红包{}】身份信息失效，现在更换手机号为{}监控'.format(wx_bz, bianhao, phone))
                        else:
                            logger.info('{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wx_bz, bianhao))
                            break
                    elif result['status'] == 2:
                        logger.debug('{} - 未知错误，{}'.format(wx_bz, result['value']))
                        if result['value']['message'] == '领取失败，请刷新再试。':
                            values = get_eleid()
                            if values:
                                phone, link, sign, sid, sms_url = values[1], values[2], values[3], values[4], \
                                                                  values[5]
                                logger.info('{} - 【红包{}】领取失败，请刷新再试。现在更换手机号为{}监控'.format(wx_bz, bianhao, phone))
                            else:
                                logger.info('{} - 【红包{}】当前已无饿了么可用账号，请赶紧添加'.format(wx_bz, bianhao))
                                break
                        hb_time += 1
                        time.sleep(hb_time)
                        if hb_time > 15:
                            send_wxmsg(bot, wx_bz, '【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                            break
                    elif result['status'] == -1:
                        logger.debug('{} - {}'.format(wx_bz, result['value']))
                        send_wxmsg(bot, wx_bz, '【红包{}】抱歉，系统出现异常，请重新分享试试'.format(bianhao))
                        break
                run_time = int(time.time()) - begin_time
                logger.info('{} - 【红包{}】监控完毕~用时{}分{}秒，共查询了{}次'.format(wx_bz, bianhao, run_time//60, run_time%60, num))
                if k:
                    mysql_cursor.execute("DELETE FROM eleme_group_sn WHERE group_sn = '{}'".format(group_sn))
                    mysql_conn.commit()
                    # send_wxmsg(bot, wx_bz, '【红包{}】退出监控，用时{}分{}秒'.format(bianhao, run_time//60, run_time%60))
        else:
            logger.info('【红包{}】识别出错，已退出监控'.format(bianhao))
    except:
        logger.info('【红包{}】Error : {}'.format(bianhao, traceback.format_exc()))

def send_wxmsg(bot, wx_bz, wx_str):
    fids = bot.search(wx_bz)
    if fids:
        if len(fids) == 1:
            fids[0].send(wx_str)
        else:
            for f in fids:
                f_str = re.findall(':(.*?)>', str(f))[0].strip()
                if wx_bz == f_str:
                    f.send(wx_str)

def get_eleid():
    conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM eleme_id WHERE is_sx = '身份信息正常' ORDER BY times_int ASC ")
    ele_ids = cursor.fetchall()
    if ele_ids:
        tup_id = ele_ids[0]
        t = time.time()
        cursor.execute(
            '''UPDATE eleme_id SET times_int = {} WHERE id = {} '''.format(int(round(t * 1000)), tup_id[0]))  # 查找饿了么库
        conn.commit()
        return tup_id
    else:
        return '暂无可用账号'