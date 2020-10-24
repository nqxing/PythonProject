from package import *
from package.eleme.sign.sign_login import mobile_send_code,login_by_mobile

def close_sqlit(cursor, conn):
    cursor.close()
    if conn:
        conn.close()

def eleme_sign_open(openId):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT open_id FROM sign")
    openIds = cursor.fetchall()
    if (openId,) in openIds:
        cursor.execute("select mobile,state from sign where open_id = '{}'".format(openId))
        values = cursor.fetchall()
        if values[0][1] == 'yes' and values[0][0] == None:
            close_sqlit(cursor, conn)
            return '您已开启饿了么自动签到，但还未绑定手机号，现在回复数字“2”绑定吧'
        elif values[0][1] == 'no' and values[0][0] == None:
            cursor.execute("UPDATE sign SET state = 'yes' where open_id = '{}'".format(openId))
            conn.commit()
            close_sqlit(cursor, conn)
            return '您的饿了么自动签到开启成功，但还未绑定手机号，现在回复数字“2”绑定吧'
        elif values[0][1] == 'no' and values[0][0] != None:
            cursor.execute("UPDATE sign SET state = 'yes' where open_id = '{}'".format(openId))
            conn.commit()
            close_sqlit(cursor, conn)
            return '您的饿了么自动签到开启成功，当前绑定的手机号为（{}），如需更改请回复数字“2”'.format(values[0][0])
        else:
            close_sqlit(cursor, conn)
            return '您已开启饿了么自动签到，无需再次开启，若您要关闭饿了么自动签到请回复数字“3”'
    else:
        cursor.execute(
            "INSERT INTO sign (open_id, state, kt_time, is_bd) VALUES ('{}', '{}', '{}', '{}')".format(
                openId,
                'yes', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'no'))
        conn.commit()
        cursor.execute("SELECT open_id FROM sign")
        openIds = cursor.fetchall()
        if (openId,) in openIds:
            close_sqlit(cursor, conn)
            return '您的饿了么自动签到已开启，因你是首次开启需要绑定手机号，请在5分钟内回复你要签到的手机号'
        else:
            close_sqlit(cursor, conn)
            return '饿了么签到开启失败，请稍后再试'

def eleme_sign_close(openId):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT open_id FROM sign")
    openIds = cursor.fetchall()
    if (openId,) in openIds:
        cursor.execute("select state from sign where open_id = '{}'".format(openId))
        state_str = cursor.fetchall()[0][0]
        if state_str == 'yes':
            cursor.execute("UPDATE sign SET state = 'no' where open_id = '{}'".format(openId))
            conn.commit()
            close_sqlit(cursor, conn)
            return '您的饿了么自动签到已关闭，回复数字“1”可再次开启哦'
        elif state_str == 'no':
            close_sqlit(cursor, conn)
            return '您的饿了么自动签到已是关闭状态，无需重复关闭'
    else:
        close_sqlit(cursor, conn)
        return '您未开启饿了么自动签到，无需关闭，若需开通请回复数字“1”'

def eleme_sign_verify_mobile(openId, mobile):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT open_id FROM sign")
    openIds = cursor.fetchall()
    if (openId,) in openIds:
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
        if len(mobile) == 11:
            if is_mobile(mobile):
                result = mobile_send_code(openId, mobile)
                if result['status'] == 0:
                    cursor.execute("SELECT open_id FROM sign_val_token")
                    openIds = cursor.fetchall()
                    mobile = result['mobile']
                    validate_token = result['validate_token']
                    if (openId,) in openIds:
                        cursor.execute("UPDATE sign_val_token SET mobile = '{}', validate_token = '{}' where open_id = '{}'".format(mobile, validate_token, openId))
                        conn.commit()
                    else:
                        cursor.execute(
                            "INSERT INTO sign_val_token (open_id, mobile, validate_token) VALUES ('{}', '{}', '{}')".format(
                                openId, mobile, validate_token))
                        conn.commit()
                    close_sqlit(cursor, conn)
                    return result
                elif result['status'] == 1:
                    close_sqlit(cursor, conn)
                    return result
                else:
                    close_sqlit(cursor, conn)
                    return result
            else:
                close_sqlit(cursor, conn)
                result = {'status': 2, 'message': '请发送正确的手机号'}
                return result
        else:
            close_sqlit(cursor, conn)
            result = {'status': 2, 'message': '请发送正确的手机号'}
            return result
    else:
        result = {'status': 3, 'message': '您未开启饿了么自动签到，无需绑定手机，若需开通请回复数字“1”'}
        return result

def eleme_sign_verify_code(openId, validate_code):
    try:
        if len(validate_code) <= 6:
            conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
            cursor = conn.cursor()  # 获取游标
            cursor.execute("SELECT open_id FROM sign")
            openIds = cursor.fetchall()
            if (openId,) in openIds:
                cursor.execute("SELECT open_id FROM sign_val_token")
                openIds = cursor.fetchall()
                if (openId,) in openIds:
                    cursor.execute("SELECT mobile,validate_token FROM sign_val_token WHERE open_id = '{}'".format(openId))
                    values = cursor.fetchall()
                    result = login_by_mobile(validate_code, values[0][1], values[0][0])
                    if result['status'] == 0:
                        cursor.execute(
                            "UPDATE sign SET mobile = '{}',sid = '{}',users_id = '{}',is_bd = 'yes' where open_id = '{}'".format(
                                values[0][0], result['sid'], result['users_id'], openId))
                        conn.commit()
                        result = {'status': 0}
                        close_sqlit(cursor, conn)
                        return result
                    else:
                        close_sqlit(cursor, conn)
                        return result
            else:
                close_sqlit(cursor, conn)
                result = {'status': -1, 'message': '验证出现错误，请重新发送验证码试试吧'}
                return result
        else:
            result = {'status': 2, 'message': '输入错误，验证码为6位数哦，请重新发送'}
            return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证出现错误，请重新发送验证码试试吧'}
        return result