from threading import Thread
from config.config import ELEME_DATA_PATH,  HOST, USER, PWD, IS_HTTPS
import sqlite3
from eleme.hongbao.hongbao_cx import cx_hongbao
from eleme.login.mobile_send_code import mobile_send_code
import traceback
import pymysql
import requests
import time

# def async(f):
#     def wrapper(*args, **kwargs):
#         thr = Thread(target=f, args=args, kwargs=kwargs)
#         thr.start()
#     return wrapper
#
# @async  # 开启异步线程执行 调用一次开启一个线程
def xh_hongbao(group_sn, bianhao, alink, puid, beizhu, wxmsg, logger):
    try:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标

        mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
        mysql_cursor = mysql_conn.cursor()  # 获取游标

        mysql_cursor.execute('''select count(*) from eleme_id''')
        max = mysql_cursor.fetchall()[0][0]
        x = True
        y = True
        get_sid_list = []
        num_url = 'https://h5.ele.me/restapi/marketing/themes/3971/group_sns/{}'.format(group_sn)  # 获取最大红包数链接
        hongbaoMax = requests.get(num_url, verify=False if IS_HTTPS else None).json()['lucky_number']
        logger.info('[会员]{} - 【红包{}】的最佳手气红包为第{}个'.format(beizhu, bianhao, hongbaoMax))
        if hongbaoMax != None:
            # print('【红包{}】的最佳手气红包为第{}个'.format(bianhao, hongbaoMax))
            wxmsg.reply('【红包{}】系统正在领取中，请稍等...'.format(bianhao))
            for i in range(1, max+1):
                mysql_cursor.execute('''select is_ret_code from eleme_id WHERE id = {}'''.format(i))
                is_ret_code = mysql_cursor.fetchall()[0][0]
                if is_ret_code == 'no':
                    mysql_cursor.execute('''select * from eleme_id WHERE id = {} '''.format(i))
                    values = mysql_cursor.fetchall()
                    if x:
                        hb_time = 5
                        phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], values[0][5]
                        # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
                        while True:
                            result = cx_hongbao(phone, link, sign, sid, group_sn)
                            if result['status'] == 0:
                                # print(result['value'])
                                # print('--------------------------------------------')
                                hongbao = len(result['value']['promotion_records'])
                                promotion_items = len(result['value']['promotion_items'])
                                if hongbao < hongbaoMax - 1:
                                    mysql_cursor.execute(
                                        "UPDATE eleme_id SET is_sx = '身份信息正常' WHERE mobile = '{}'".format(phone))
                                    mysql_conn.commit()
                                    if result['value']['ret_code'] != 5:
                                        if promotion_items != 0:
                                            logger.info('[会员]{} - 【红包{}】[{}]领取红包成功，当前已有{}人领取'.format(beizhu, bianhao, phone, hongbao))
                                        else:
                                            logger.info('[会员]{} - 【红包{}】[{}]领取红包失败，当前已有{}人领取'.format(beizhu, bianhao, phone, hongbao))
                                    elif result['value']['ret_code'] == 5:
                                        # mysql_cursor = mysql_conn.cursor()  # 获取游标
                                        mysql_cursor.execute("UPDATE eleme_id SET is_ret_code = 'yes' WHERE mobile = '{}'".format(phone))
                                        mysql_conn.commit()
                                        logger.info('[会员]{} - 【红包{}】[{}]领取红包失败，当天红包领取已达5次'.format(beizhu, bianhao, phone))
                                    break
                                if hongbao == hongbaoMax - 1:
                                    logger.info('[会员]{} - 【红包{}】[{}]领取红包成功，当前已有{}人领取'.format(beizhu, bianhao, phone, hongbao))
                                    # print('【红包{}】监控中,当前已有{}人领取~~'.format(bianhao, hongbao))
                                    msg = '【红包{}】领取完毕，下一个就是最佳手气红包，快去点开领取吧（注：若该红包第{}个不是最佳手气，系统将自动退还您的次数）'.format(bianhao, hongbaoMax)
                                    wxmsg.reply(msg)
                                    wxmsg.reply(alink)
                                    cursor.execute("select num from eleme_vip WHERE puid = '{}' OR wx_beizhu = '{}'".format(puid, beizhu))
                                    vip_num = cursor.fetchall()[0][0]
                                    cursor.execute(
                                        "UPDATE eleme_vip SET num = {} WHERE puid = '{}' OR wx_beizhu = '{}'".format(vip_num - 1, puid,
                                                                                                                 beizhu))
                                    conn.commit()
                                    logger.info('[会员]{} - 【红包{}】下一个就是最佳手气红包，剩余次数{}，链接：{}'.format(beizhu, bianhao, vip_num - 1, alink))
                                    x = False
                                    y = False
                                    break
                                elif hongbao > hongbaoMax - 1:
                                    logger.info('[会员]{} - 【红包{}】的最佳手气已经被领走了，请换个红包吧'.format(beizhu, bianhao))
                                    wxmsg.reply('【红包{}】的最佳手气已经被领走了，请换个红包吧，本次不扣除次数'.format(bianhao))
                                    x = False
                                    break
                            elif result['status'] == 1:
                                sid_dict = {}
                                sid_dict['phone'] = phone
                                sid_dict['sms_url'] = sms_url
                                get_sid_list.append(sid_dict)
                                logger.info('[会员]{} - 使用账号[{}]领包时出现身份信息过期'.format(beizhu, phone))
                                break
                            elif result['status'] == 2:
                                logger.info('[会员]{} - 未知错误，{}'.format(beizhu, result['value']))
                                hb_time += 1
                                if hb_time > 6:
                                    break
                                time.sleep(hb_time)
                            elif result['status'] == -1:
                                logger.info('[会员]{} - Error: {}'.format(beizhu, result['value']))
                                break
                        # time.sleep(1)
                    else:
                        break
                    if y == False:
                        hb_time = 5
                        phone, link, sign, sid, sms_url = values[0][1], values[0][2], values[0][3], values[0][4], values[0][5]
                        # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
                        begin_time = int(time.time())  # 获取运行该脚本时的时间戳
                        while True:
                            time.sleep(10)
                            result = cx_hongbao(phone, link, sign, sid, group_sn)
                            if result['status'] == 0:
                                hongbao = len(result['value']['promotion_records'])
                                if hongbao >= hongbaoMax:
                                    is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                                    if is_lucky:
                                        lucky_amount = result['value']['promotion_records'][hongbaoMax - 1]['amount']
                                        logger.info('[会员]{} - 【红包{}】最佳手气产生正常，最佳手气红包为{}元'.format(beizhu, bianhao, lucky_amount))
                                        break
                                    else:
                                        logger.info('[会员]{} - 【红包{}】最佳手气未正常产生，现进行次数返还'.format(beizhu, bianhao))
                                        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
                                        cursor = conn.cursor()  # 获取游标
                                        cursor.execute("select num from eleme_vip WHERE puid = '{}' OR wx_beizhu = '{}'".format(puid, beizhu))
                                        num = cursor.fetchall()[0][0]
                                        logger.info('{}当前有{}次一键次数，本次操作会为Ta新增1次'.format(beizhu, num))
                                        cursor.execute(
                                            "UPDATE eleme_vip SET num = {} WHERE puid = '{}' OR wx_beizhu = '{}'".format(num + 1,
                                                                                                      puid, beizhu))
                                        conn.commit()
                                        cursor.execute("select num from eleme_vip WHERE puid = '{}' OR wx_beizhu = '{}'".format(puid, beizhu))
                                        num1 = cursor.fetchall()[0][0]
                                        logger.info('{}新增次数成功，新增后的次数为{}'.format(beizhu, num1))
                                        wxmsg.reply('【红包{}】因系统检测到第{}个并不是最佳手气红包，所以本次退还了您的一键领大包次数，请注意查收'.format(bianhao, hongbaoMax))
                                        break
                                t_run_time = int(time.time()) - begin_time
                                if t_run_time // 60 >= 60:
                                    logger.info('[会员]{} - 【红包{}】因您在1小时内未领取该红包，系统无法检测到该红包最佳手气是否产生，若最佳手气产生错误，请联系客服退还次数'.format(beizhu, bianhao))
                                    wxmsg.reply(
                                        '【红包{}】因您在1小时内未领取该红包，系统无法检测到该红包最佳手气是否产生，若最佳手气产生错误，请联系客服微信退还次数'.format(bianhao))
                                    break
                            elif result['status'] == 1:
                                logger.info('[会员]{} - 【红包{}】检测最佳时{}身份信息过期，需重新验证'.format(beizhu, bianhao, phone))
                                mysql_cursor.execute(
                                    "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
                                mysql_conn.commit()
                                break
                                # result = mobile_send_code(phone, sms_url, conn, cursor, logger)
                                # if result['status'] == 0:
                                #     sid = result['sid']
                                # else:
                                #     logger.debug('[会员]{} - 【红包{}】 - {}'.format(beizhu, bianhao, result['message']))
                                #     break
                            elif result['status'] == 2:
                                logger.info('[会员]{} - 未知错误，{}'.format(beizhu, result['value']))
                                hb_time += 1
                                if hb_time > 7:
                                    break
                                time.sleep(hb_time)
                            elif result['status'] == -1:
                                logger.info('[会员]{} - Error: {}'.format(beizhu, result['value']))
                                break
                        break
            if y and x:
                wxmsg.reply('领取太火爆啦，系统预置账号次数已用完，请过几分钟重新分享或明天再来吧（注：红包监控功能不受影响哦）')
                logger.info('[会员]{} - 【红包{}】领取太火爆啦，系统预置账号次数已用完，请过几分钟重新分享或明天再来吧'.format(beizhu, bianhao))
            if len(get_sid_list) != 0:
                logger.info('[会员]{} - 领取红包任务已完成，现对过期账号sid重新验证'.format(beizhu))
                for s in get_sid_list:
                    phone = s['phone']
                    sms_url = s['sms_url']
                    logger.info('[会员]{} - [{}]身份信息过期，需重新验证'.format(beizhu, phone))
                    mysql_cursor.execute(
                        "UPDATE eleme_id SET is_sx = '未登录' WHERE mobile = '{}'".format(phone))
                    mysql_conn.commit()

                    # result1 = mobile_send_code(phone, sms_url, conn, cursor, logger)
                    # if result1['status'] == 0:
                    #     logger.info('[会员]{} - [{}]新的sid已写入'.format(beizhu, phone))
                    # else:
                    #     logger.debug('[会员]{} - [{}]身份验证出错，{}'.format(beizhu, phone, result1['message']))
                    #     if result1['message'] == '未找到饿了么短信':
                    #         logger.info('[会员]{} - 未找到饿了么短信，正在重试'.format(beizhu))
                    #         result1 = mobile_send_code(phone, sms_url, conn, cursor, logger)
                    #         logger.info('[会员]{} - {}'.format(beizhu, result1))
            logger.info('[会员]{} - 【红包{}】退出一键领取系统'.format(beizhu, bianhao))
        else:
            logger.info('【红包{}】识别出错，请重新分享或换个红包试试吧'.format(bianhao))
            wxmsg.reply('【红包{}】识别出错，请重新分享或换个红包试试吧'.format(bianhao))
    except:
        logger.info('【红包{}】Error : {}'.format(bianhao, traceback.format_exc()))