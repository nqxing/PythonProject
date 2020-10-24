import MySQLdb
from config.fun_api import *
from config.config import *

class MysqlSearch(object):
    def __init__(self):
        self.get_conn()
    def get_conn(self):
        try:
            self.conn = MySQLdb.connect(
                host = HOST,
                port=3306,
                user = USER,
                passwd = PWD,
                db = DB_NAME,
                charset = 'utf8'
            )
        except MySQLdb.Error as e:
            write_log(3, 'Error %d:%s' % (e.args[0], e.args[1]))
    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except MySQLdb.Error as e:
            write_log(3, 'Error: %s' % e)
    def select_var_info(self, where):
        sql = " select var_info from pub_var_list where var_name = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values[0][0]
    def up_var_info(self, where, value):
        sql = " update pub_var_list set var_info = '{}' where var_name = '{}' ".format(value, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def select_clock(self, where):
        sql = " select bind_name,wx_open_id from pub_card_users WHERE wx_note = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_clock_open1(self, where):
        sql = " select state,time_list from pub_card_users where wx_note = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def up_clock_open1(self, where):
        sql = " update pub_card_users set state = {} where wx_note = '{}' ".format(True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_clock_open2(self, where):
        sql = " update pub_card_users set state = {} where wx_note = '{}' ".format(False, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def add_clock_users(self, puid, note, name):
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        new_name = re.sub(reg, '', str(name))
        sql = "INSERT INTO pub_card_users (wx_puid, wx_note, wx_name, state, create_time, is_first) VALUES ('{}', '{}', '{}', {}, '{}', {})".format(
            puid, note, new_name, False, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), True)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_clock_times(self, where, time_list, time_num):
        sql = " update pub_card_users set time_list = '{}',time_num = {},state = {} where wx_note = '{}' ".format(time_list, time_num, True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def select_is_holiday(self, where):
        sql = " select is_holiday from pub_card_text where text_id = {} ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values[0][0]
    def select_card(self, where):
        sql = "SELECT wx_note,qq,time_num,is_first,id FROM pub_card_users WHERE state = {} and time_list LIKE '%".format(True) + "{}".format(where) + "%'"
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def up_is_first(self, where):
        sql = "UPDATE pub_card_users SET is_first = {} WHERE id = '{}'".format(False, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def select_card_text(self, where):
        sql = " select * from pub_card_text where text_id = {} ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_card_holiday(self, where):
        sql = " select id,holiday from pub_card_text where id > {} and is_holiday = {} ".format(int(where), True)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_card_text_history(self, where):
        sql = " select his_info from pub_card_text_history where his_id = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_ele_tx(self):
        sql = " select * from pub_ele_tx_urls "
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def add_ele_hb_record(self, bianhao, name, amount, esource):
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        new_name = re.sub(reg, '', str(name))
        sql = "INSERT INTO pub_ele_hb_record (bianhao, name, amount, create_time, esource) VALUES ({}, '{}', '{}', '{}', '{}')".format(
                                                bianhao, new_name, amount, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), esource)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    #饿了么签到相关语句
    def select_sign_users(self, where):
        sql = " select bind_name,wx_open_id from pub_ele_sign_users WHERE wx_note = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_sign_open1(self, where):
        sql = " select state,mobile from pub_ele_sign_users where wx_note = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def up_sign_open1(self, where):
        sql = " update pub_ele_sign_users set state = {} where wx_note = '{}' ".format(True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_sign_open2(self, where):
        sql = " update pub_ele_sign_users set state = {} where user_id = '{}' ".format(False, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def add_sign_users(self, puid, note, name):
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        new_name = re.sub(reg, '', str(name))
        sql = "INSERT INTO pub_ele_sign_users (wx_puid, wx_note, wx_name, state, create_time, is_bind, is_sign) VALUES ('{}', '{}', '{}', {}, '{}', {}, {})".format(
                puid, note, new_name,
                False, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), False, False)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_sign_sid(self, is_puid, mobile, sid, user_id, where):
        if is_puid:
            sql = " update pub_ele_sign_users set mobile = '{}',sid = '{}',state = {},user_id = '{}',is_bind = {} where wx_puid = '{}' ".format(mobile, sid, True, user_id, True, where)
        else:
            sql = " update pub_ele_sign_users set mobile = '{}',sid = '{}',state = {},user_id = '{}',is_bind = {} where wx_note = '{}' ".format(mobile, sid, True, user_id, True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def select_sign_sid(self):
        sql = " SELECT wx_open_id, wx_note, qq, sid, user_id FROM pub_ele_sign_users WHERE state = {} AND is_bind = {} ".format(True, True)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def up_is_sign(self, where):
        sql = " update pub_ele_sign_users set is_sign = {} where user_id = '{}' ".format(True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    # 更新饿了么签到和打卡状态
    def up_state(self):
        sql1 = " UPDATE pub_ele_sign_users SET is_sign = {} ".format(False)
        sql2 = " UPDATE pub_card_users SET is_first = {} ".format(True)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql1)
        self.conn.commit()
        cursor.execute(sql2)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    # 查询公众号绑定库
    def select_bind_users(self, where):
        sql = " SELECT wx_open_id,is_bind,wx_note FROM pub_bind_users WHERE bind_name = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_bind_users_bz(self, bz, where):
        sql = " SELECT bind_name FROM pub_bind_users WHERE wx_note = '{}' ".format(bz)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        if not values:
            usql1 = " update pub_bind_users set wx_note = '{}',is_bind = {} where bind_name = '{}' ".format(bz, True, where)
            # 执行SQL
            cursor.execute(usql1)
            self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def set_binds(self, bind_name, where, bz):
        sign, card = False, False
        sql1 = " SELECT * FROM pub_ele_sign_users WHERE wx_open_id = '{}' ".format(where)
        sql2 = " SELECT * FROM pub_card_users WHERE wx_open_id = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql1)
        values1 = cursor.fetchall()
        if values1:
            usql1 = " update pub_ele_sign_users set bind_name = '{}',wx_note = '{}' where wx_open_id = '{}' ".format(bind_name, bz, where)
            # 执行SQL
            cursor.execute(usql1)
            self.conn.commit()
            sign = True
        cursor.execute(sql2)
        values2 = cursor.fetchall()
        if values2:
            usql2 = " update pub_card_users set bind_name = '{}',wx_note = '{}' where wx_open_id = '{}' ".format(bind_name, bz, where)
            # 执行SQL
            cursor.execute(usql2)
            self.conn.commit()
            card = True
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return [sign, card]
    def select_bind_is_users(self, where):
        sql = " SELECT wx_open_id,is_bind FROM pub_bind_users WHERE wx_note = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_sign_is_users(self, where):
        sql = " select wx_open_id from pub_ele_sign_users where wx_note = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    # 饿么了红包库相关
    def add_ele_hb(self, bianhao, group_sn, hongbaoMax, url, state, from_name):
        sql = "INSERT INTO pub_ele_group_sn (bianhao, group_sn, yet, yet_max, url, state, from_name, create_time) VALUES ('{}', '{}', 0, {}, '{}', {}, '{}', '{}')".format(
                bianhao, group_sn, hongbaoMax,
            url, state, from_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_ele_hb_time(self, yet, group_sn, phone):
        sql1 = "UPDATE pub_ele_group_sn SET yet = {}, up_time = '{}' WHERE group_sn = '{}'".format(yet, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn)
        sql2 = "UPDATE pub_ele_id SET id_info = '身份信息正常' WHERE mobile = '{}'".format(phone)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql1)
        self.conn.commit()
        cursor.execute(sql2)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_ele_over_hb(self, group_sn):
        sql = "UPDATE pub_ele_group_sn SET state = {}, up_time = '{}' WHERE group_sn = '{}'".format(True, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), group_sn)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_ele_id_info(self, info, phone):
        sql = "UPDATE pub_ele_id SET id_info = '{}' WHERE mobile = '{}'".format(info, phone)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def del_ele_group_sn(self, group_sn):
        sql = "DELETE FROM pub_ele_group_sn WHERE group_sn = '{}'".format(group_sn)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def select_ele_id_info(self):
        sql = " SELECT * FROM pub_ele_id WHERE id_info = '身份信息正常' ORDER BY time_stamp ASC "
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def up_ele_id_time_stamp(self, time_stamp, id):
        sql = '''UPDATE pub_ele_id SET time_stamp = {} WHERE id = {} '''.format(time_stamp, id)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    # 查询王者英雄库相关
    def select_wz_wall(self, where):
        sql = "SELECT * FROM pub_wz_wall WHERE hero_name_bm LIKE '%" + "{}".format(where) + "%'"
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_win_rate(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_win_rate WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_skill(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_skill WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_equip(self, where):
        sql = "SELECT cx_value,cx_value1,hero_name FROM pub_wz_equip WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_rune(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_rune WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_kz(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_kz WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_introduce(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_introduce WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_zh(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_zh WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_wz_jq(self, where):
        sql = "SELECT cx_value,hero_name FROM pub_wz_skills WHERE cx_name = '{}'".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values