from config.config import ELEME_DATA_PATH
from eleme.sign.get_sid import mobile_send_code, login_by_mobile
import sqlite3
import datetime

sign_dict = {}

def eleme_sign_open(beizhu, puid, msg, logger):
    bz_state = False
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT wx_beizhu FROM eleme_sign")
    vip_beizhu = cursor.fetchall()
    cursor.execute("SELECT puid FROM eleme_sign")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        if beizhu in vip_beizhu:
            update_sql = True
        else:
            update_sql = False
        if update_sql:
            cursor.execute("select mobile from eleme_sign where wx_beizhu = '{}'".format(beizhu[0]))
            mobile_str = cursor.fetchall()
            cursor.execute("select state from eleme_sign where wx_beizhu = '{}'".format(beizhu[0]))
            state_str = cursor.fetchall()
        else:
            cursor.execute("select mobile from eleme_sign where puid = '{}'".format(puid[0]))
            mobile_str = cursor.fetchall()
            cursor.execute("select state from eleme_sign where puid = '{}'".format(puid[0]))
            state_str = cursor.fetchall()
        if state_str[0][0] == 'yes' and mobile_str[0][0] == None:
            msg.reply('您已开启饿了么自动签到，但还未绑定手机号，现在回复手机号绑定吧')
        elif state_str[0][0] == 'no' and mobile_str[0][0] == None:
            if update_sql:
                cursor.execute("UPDATE eleme_sign SET state = 'yes' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
            else:
                cursor.execute("UPDATE eleme_sign SET state = 'yes' where puid = '{}'".format(puid[0]))
                conn.commit()
            msg.reply('您的饿了么自动签到开启成功，但还未绑定手机号，现在回复手机号绑定吧')
        elif state_str[0][0] == 'no' and mobile_str[0][0] != None:
            if update_sql:
                cursor.execute("UPDATE eleme_sign SET state = 'yes' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
            else:
                cursor.execute("UPDATE eleme_sign SET state = 'yes' where puid = '{}'".format(puid[0]))
                conn.commit()
            msg.reply('您的饿了么自动签到开启成功，当前绑定的手机号为（{}），如需更改请重新发送手机号哦'.format(mobile_str[0][0]))
        else:
            msg.reply('您已开启饿了么自动签到，无需再次开启，若您要关闭饿了么自动签到请发送“关闭饿了么签到”')
    else:
        if 'vip_' in beizhu[0]:
            bz = beizhu[0]
        else:
            cursor.execute('''SELECT count FROM eleme_count WHERE id = 2''')
            num = int(cursor.fetchall()[0][0])
            bz = 'vip_{}'.format(num)
            bz_state = True
        cursor.execute(
            "INSERT INTO eleme_sign (puid, wx_beizhu, wx_name, state, kt_time, is_bd) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                puid[0], bz, msg.sender,
                'yes', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'no'))
        conn.commit()
        cursor.execute("SELECT wx_beizhu FROM eleme_sign")
        vip_bz = str(cursor.fetchall())
        cursor.execute("SELECT puid FROM eleme_sign")
        vip_puid = str(cursor.fetchall())
        if puid[0] in vip_puid and bz in str(vip_bz):
            logger.info('有人开启了饿了么签到服务')
            if bz_state:
                logger.info('设置了新备注{}'.format(bz))
                msg.sender.set_remark_name(bz)
                cursor.execute('''SELECT count FROM eleme_count WHERE id = 2''')
                num = int(cursor.fetchall()[0][0])
                num += 1
                cursor.execute('''UPDATE eleme_count SET count = '{}' where id = 2'''.format(num))
                conn.commit()
            msg.reply('您的饿了么自动签到已开启，因你是首次开启需要绑定手机号，现在请回复你要自动签到的手机号')
        else:
            msg.reply('饿了么签到开启失败，请稍后再试')

def eleme_sign_close(beizhu, puid, msg):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select wx_beizhu from eleme_sign")
    vip_beizhu = cursor.fetchall()
    cursor.execute("select puid from eleme_sign")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        if beizhu in vip_beizhu:
            update_sql = True
        else:
            update_sql = False
        if update_sql:
            cursor.execute("select state from eleme_sign where wx_beizhu = '{}'".format(beizhu[0]))
            state_str = cursor.fetchall()[0][0]
            if state_str == 'yes':
                cursor.execute("UPDATE eleme_sign SET state = 'no' where wx_beizhu = '{}'".format(beizhu[0]))
                conn.commit()
                msg.reply('您的饿了么自动签到已关闭，发送“开启饿了么签到”可再次开启哦')
            elif state_str == 'no':
                msg.reply('您的饿了么自动签到已是关闭状态，无需重复关闭')
        else:
            cursor.execute("select state from eleme_sign where puid = '{}'".format(puid[0]))
            state_str = cursor.fetchall()[0][0]
            if state_str == 'yes':
                cursor.execute("UPDATE eleme_sign SET state = 'no' where puid = '{}'".format(puid[0]))
                conn.commit()
                msg.reply('您的饿了么自动签到已关闭，发送“开启饿了么签到”可再次开启哦')
            elif state_str == 'no':
                msg.reply('您的饿了么自动签到已是关闭状态，无需重复关闭')
    else:
        msg.reply('您未开启饿了么自动签到，无需关闭，若需开通请发送“开启饿了么签到”')

def eleme_sign_verify_mobile(beizhu, puid, msg, text, logger):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select wx_beizhu from eleme_sign")
    vip_beizhu = cursor.fetchall()
    cursor.execute("select puid from eleme_sign")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        def is_mobile(mobile):
            if '13' == mobile[0:2]:
                return True
            elif '14' == mobile[0:2]:
                return True
            elif '15' == mobile[0:2]:
                return True
            elif '16' == mobile[0:2]:
                return True
            elif '17' == mobile[0:2]:
                return True
            elif '18' == mobile[0:2]:
                return True
            elif '19' == mobile[0:2]:
                return True
            else:
                return False

        if is_mobile(text):
            logger.info('[会员]{} - 发送了手机号[{}]，正在发送验证码'.format(beizhu[0], text))
            msg.reply('正在发送验证码，请稍等...')
            result = mobile_send_code(text, logger)
            if result['status'] == 0:
                mobile_list = []
                mobile_list.append(result['validate_token'])
                mobile_list.append(result['mobile'])
                sign_dict[puid[0]] = mobile_list
                logger.info('[会员]{} - 新建了字典{}'.format(beizhu[0], sign_dict))
                logger.info('[会员]{} - {}'.format(beizhu[0], result['message']))
                msg.reply(result['message'])
            else:
                logger.info('[会员]{} - {}'.format(beizhu[0], result['message']))
                msg.reply(result['message'])
        else:
            msg.reply('请发送正确的手机号')

def eleme_sign_verify_code(beizhu, puid, msg, text, logger):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select wx_beizhu from eleme_sign")
    vip_beizhu = cursor.fetchall()
    cursor.execute("select puid from eleme_sign")
    vip_puid = cursor.fetchall()
    if beizhu in vip_beizhu or puid in vip_puid:
        if beizhu in vip_beizhu:
            update_sql = True
        else:
            update_sql = False
        if puid[0] in sign_dict:
            logger.info('[会员]{} - 发送了短信验证码[{}]，正在进行提取sid'.format(beizhu[0], text))
            values = sign_dict[puid[0]]
            result = login_by_mobile(text, values[0], values[1], logger)
            if result['status'] == 0:
                if update_sql:
                    cursor.execute(
                        "UPDATE eleme_sign SET mobile = '{}', sid = '{}', users_id = '{}' where wx_beizhu = '{}'".format(
                            values[1], result['sid'], result['users_id'], beizhu[0]))
                    conn.commit()
                    cursor.execute("UPDATE eleme_sign SET is_bd = 'yes' where wx_beizhu = '{}'".format(beizhu[0]))
                    conn.commit()
                    removed_value = sign_dict.pop(puid[0])
                    logger.info(
                        '[会员]{} - 成功开通了饿了么自动签到系统，移除了字典key[{}]，对应value为[{}]'.format(beizhu[0], puid[0],
                                                                                   removed_value))
                    msg.reply(
                        '恭喜你，手机号绑定成功，饿了么自动签到设置成功，系统会在每天上午09:00自动为你签到，签到结果将发送微信消息通知您\n\n（注：如需修改手机号请重新发送手机号即可，发送“关闭饿了么签到”可关闭每日自动签到哦）')
                else:
                    cursor.execute(
                        "UPDATE eleme_sign SET mobile = '{}', sid = '{}', users_id = '{}' where puid = '{}'".format(
                            values[1], result['sid'], result['users_id'], puid[0]))
                    conn.commit()
                    cursor.execute("UPDATE eleme_sign SET is_bd = 'yes' where puid = '{}'".format(puid[0]))
                    conn.commit()
                    removed_value = sign_dict.pop(puid[0])
                    logger.info(
                        '[会员]{} - 成功开通了饿了么自动签到系统，移除了字典key[{}]，对应value为[{}]'.format(beizhu[0], puid[0],
                                                                                   removed_value))
                    msg.reply(
                        '恭喜你，手机号绑定成功，饿了么自动签到设置成功，系统会在每天上午09:00自动为你签到，签到结果将发送微信消息通知您\n\n（注：如需修改手机号请重新发送手机号即可，发送“关闭饿了么签到”可关闭每日自动签到哦）')
            else:
                logger.info('[会员]{} - {}'.format(beizhu[0], result['message']))
                msg.reply(result['message'])