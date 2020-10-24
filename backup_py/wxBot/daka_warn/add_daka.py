import sqlite3
import datetime
from config.config import ELEME_DATA_PATH

def daka_open(beizhu, puid, msg, logger):
    bz_state = False
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT wx_beizhu FROM daka_vip")
    vip_beizhu = cursor.fetchall()
    cursor.execute("SELECT puid FROM daka_vip")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        if beizhu in vip_beizhu:
            update_sql = True
        else:
            update_sql = False
        if update_sql:
            cursor.execute("select tx_time from daka_vip where wx_beizhu = '{}'".format(beizhu[0]))
            tx_time_str = cursor.fetchall()
            cursor.execute("select state from daka_vip where wx_beizhu = '{}'".format(beizhu[0]))
            state_str = cursor.fetchall()
        else:
            cursor.execute("select tx_time from daka_vip where puid = '{}'".format(puid[0]))
            tx_time_str = cursor.fetchall()
            cursor.execute("select state from daka_vip where puid = '{}'".format(puid[0]))
            state_str = cursor.fetchall()
        if state_str[0][0] == 'yes' and tx_time_str[0][0] == None:
            msg.reply('您已开启打卡提醒，但还未设置提醒时间，现在回复时间设置吧')
        elif state_str[0][0] == 'no' and tx_time_str[0][0] == None:
            if update_sql:
                cursor.execute("UPDATE daka_vip SET state = 'yes' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
            else:
                cursor.execute("UPDATE daka_vip SET state = 'yes' where puid = '{}'".format(puid[0]))
                conn.commit()
            msg.reply('您的打卡提醒开启成功，但还未设置提醒时间，现在回复时间设置吧')
        elif state_str[0][0] == 'no' and tx_time_str[0][0] != None:
            if update_sql:
                cursor.execute("UPDATE daka_vip SET state = 'yes' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
            else:
                cursor.execute("UPDATE daka_vip SET state = 'yes' where puid = '{}'".format(puid[0]))
                conn.commit()
            msg.reply('您的打卡提醒开启成功，当前设置的提醒时间为（{}），如需更改请重新发送时间哦'.format(tx_time_str[0][0]))
        else:
            msg.reply('您已开启打卡提醒，无需再次开启，若您要关闭提醒请发送“关闭打卡提醒”')
    else:
        if 'vip_' in beizhu[0]:
            bz = beizhu[0]
        else:
            # cursor.execute('''select count(*) from eleme_vip''')
            cursor.execute('''SELECT count FROM eleme_count WHERE id = 2''')
            num = int(cursor.fetchall()[0][0])
            bz = 'vip_{}'.format(num)
            bz_state = True
        cursor.execute(
            "INSERT INTO daka_vip (puid, wx_beizhu, wx_name, state, kt_time, is_shouci) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                puid[0], bz, msg.sender,
                'yes', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'yes'))
        conn.commit()
        cursor.execute("SELECT wx_beizhu FROM daka_vip")
        vip_bz = str(cursor.fetchall())
        cursor.execute("SELECT puid FROM daka_vip")
        vip_puid = str(cursor.fetchall())
        if puid[0] in vip_puid and bz in str(vip_bz):
            logger.info('有人开启了打卡提醒')
            msg.reply('您的打卡提醒服务已开启，现在请回复你要提醒的时间点哦\n\n1：只提醒上班或下班请回复单个时间，如：18:00'
                      '\n\n2：若上班和下班都要提醒请回复多个时间，如：09:00,18:00（注：多个时间之间用逗号隔开哦，最多可设置4个时间）'
                      '\n\n3：发送“关闭打卡提醒”即可关闭打卡提醒服务')
            if bz_state:
                logger.info('设置了新备注{}'.format(bz))
                msg.sender.set_remark_name(bz)
                cursor.execute('''SELECT count FROM eleme_count WHERE id = 2''')
                num = int(cursor.fetchall()[0][0])
                num += 1
                cursor.execute('''UPDATE eleme_count SET count = '{}' where id = 2'''.format(num))
                conn.commit()
        else:
            msg.reply('打卡提醒开通失败，请稍后再试')

def daka_close(beizhu, puid, msg):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select wx_beizhu from daka_vip")
    vip_beizhu = cursor.fetchall()
    cursor.execute("select puid from daka_vip")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        if beizhu in vip_beizhu:
            update_sql = True
        else:
            update_sql = False
        if update_sql:
            cursor.execute("select state from daka_vip where wx_beizhu = '{}'".format(beizhu[0]))
            state_str = cursor.fetchall()[0][0]
            if state_str == 'yes':
                cursor.execute("UPDATE daka_vip SET state = 'no' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
                msg.reply('您的打卡提醒已关闭，发送“开启打卡提醒”可再次开启哦')
            elif state_str == 'no':
                msg.reply('您的打卡提醒已是关闭状态，无需重复关闭')
        else:
            cursor.execute("select state from daka_vip where puid = '{}'".format(puid[0]))
            state_str = cursor.fetchall()[0][0]
            if state_str == 'yes':
                cursor.execute("UPDATE daka_vip SET state = 'no' where puid = '{}'".format(puid[0]))
                conn.commit()
                msg.reply('您的打卡提醒已关闭，发送“开启打卡提醒”可再次开启哦')
            elif state_str == 'no':
                msg.reply('您的打卡提醒已是关闭状态，无需重复关闭')
    else:
        msg.reply('您未开启打卡提醒，无需关闭，若需开通请发送“开启打卡提醒”')

def daka_update_time(beizhu, puid, msg, text):
    text = text.replace(' ', '')
    text = text.replace('：', ':')
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select puid from daka_vip")
    vip_puid = cursor.fetchall()
    cursor.execute("select wx_beizhu from daka_vip")
    vip_beizhu = cursor.fetchall()
    if puid in vip_puid or beizhu in vip_beizhu:
        text = text.replace(' ', '')
        if beizhu in vip_beizhu:
            update_sql = True
            cursor.execute("select state from daka_vip where wx_beizhu = '{}'".format(beizhu[0]))
            state_str = cursor.fetchall()[0][0]
        else:
            update_sql = False
            cursor.execute("select state from daka_vip where puid = '{}'".format(puid[0]))
            state_str = cursor.fetchall()[0][0]
        if state_str == 'yes':
            if '，' in text and '：' in text:
                text = text.replace('，', ',')
                text = text.replace('：', ':')
            if '，' in text:
                text = text.replace('，', ',')
            if '：' in text:
                text = text.replace('：', ':')
            if ',' in text:
                tx_time_list = []
                tx_times = text.split(',')
                if len(tx_times) < 5:
                    for tx in tx_times:
                        if ':' in tx:
                            tx_list = tx.split(':')
                            if len(tx_list) == 2 and len(tx_list[0]) < 3 and len(tx_list[1]) < 3:
                                txs = is_time(tx)
                                if len(txs) == 5:
                                    tx_time_list.append(txs)
                                else:
                                    msg.reply(txs)
                                    break
                            else:
                                # msg.reply('时间格式不正确，请修改后重新发送')
                                break
                        else:
                            # msg.reply('时间格式不正确，请修改后重新发送')
                            break
                    if len(tx_times) == len(tx_time_list):
                        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
                        cursor = conn.cursor()  # 获取游标
                        tx_time_list = ','.join(tx_time_list)
                        if update_sql:
                            cursor.execute(
                                "UPDATE daka_vip SET tx_time = '{}',tx_time_num = '{}' WHERE wx_beizhu = '{}'".format(
                                    tx_time_list, len(tx_times), beizhu[0]))
                            conn.commit()
                            cursor.execute("select tx_time from daka_vip WHERE wx_beizhu = '{}'".format(beizhu[0]))
                            tx_time_str = str(cursor.fetchall())
                        else:
                            cursor.execute(
                                "UPDATE daka_vip SET tx_time = '{}',tx_time_num = '{}' WHERE puid = '{}'".format(
                                    tx_time_list, len(tx_times), puid[0]))
                            conn.commit()
                            cursor.execute("select tx_time from daka_vip WHERE puid = '{}'".format(puid[0]))
                            tx_time_str = str(cursor.fetchall())
                        if tx_time_list in tx_time_str:
                            msg.reply('恭喜你，时间设置成功，到点您会收到打卡提醒哦（注：如需修改请重新发送时间即可）')
                        else:
                            msg.reply('抱歉，出现未知错误，请稍后重试')
                else:
                    msg.reply('最多只能设置4个时间哦')
            else:
                if ':' in text:
                    text_list = text.split(':')
                    if len(text_list) == 2 and len(text_list[0]) < 3 and len(text_list[1]) < 3:
                        txs = is_time(text)
                        if len(txs) == 5:
                            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
                            cursor = conn.cursor()  # 获取游标
                            if update_sql:
                                cursor.execute(
                                    "UPDATE daka_vip SET tx_time = '{}',tx_time_num = '1' WHERE wx_beizhu = '{}'".format(
                                        txs, beizhu[0]))
                                conn.commit()
                                cursor.execute("select tx_time from daka_vip WHERE wx_beizhu = '{}'".format(beizhu[0]))
                                tx_time_str = str(cursor.fetchall())
                            else:
                                cursor.execute(
                                    "UPDATE daka_vip SET tx_time = '{}',tx_time_num = '1' WHERE puid = '{}'".format(txs,
                                                                                                                    puid[
                                                                                                                        0]))
                                conn.commit()
                                cursor.execute("select tx_time from daka_vip WHERE puid = '{}'".format(puid[0]))
                                tx_time_str = str(cursor.fetchall())
                            if txs in tx_time_str:
                                msg.reply('恭喜你，时间设置成功，到点您会收到打卡提醒哦（注：如需修改请重新发送时间即可）')
                            else:
                                msg.reply('抱歉，出现未知错误，请稍后重试')
                        else:
                            msg.reply(txs)
                    else:
                        pass
                        # msg.reply('时间格式不正确，请修改后重新发送')
                else:
                    pass
                    # msg.reply('时间格式不正确，请修改后重新发送')
        elif state_str == 'no':
            msg.reply('您已关闭打卡提醒，不可以修改提醒时间哦')

def is_time(tx_time):
    hours = None
    min = None
    nums = tx_time.split(':')
    if nums[0].isdigit():
        if len(nums[0]) == 1:
            hours = '0{}'.format(nums[0])
        elif len(nums[0]) == 2 and int(nums[0]) < 24:
            hours = nums[0]
        else:
            return '小时格式不正确，请修改后重新发送'
    else:
        return '小时格式不正确，请修改后重新发送'
    if nums[1].isdigit():
        if len(nums[1]) == 1:
            min = '0{}'.format(nums[1])
        elif len(nums[1]) == 2 and int(nums[1]) < 60:
            min = nums[1]
        else:
            return '分钟格式不正确，请修改后重新发送'
    else:
        return '分钟格式不正确，请修改后重新发送'
    if hours != None and min != None:
        return '{}:{}'.format(hours, min)