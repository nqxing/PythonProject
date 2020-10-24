import MySQLdb
from plugins.pub_fun.fun_api import *
from config import *

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
    def select_clock(self, where):
        sql = " select bind_name,wx_open_id from pub_card_users WHERE qq = '{}'".format(where)
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
        sql = " select state,time_list from pub_card_users where qq = '{}' ".format(where)
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
        sql = " update pub_card_users set state = {} where qq = '{}' ".format(True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_clock_open2(self, where):
        sql = " update pub_card_users set state = {} where qq = '{}' ".format(False, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_clock_times(self, where, time_list, time_num):
        sql = " update pub_card_users set time_list = '{}',time_num = {},state = {} where qq = '{}' ".format(time_list, time_num, True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    # #饿了么签到相关语句
    def select_sign_users(self, where):
        sql = " select bind_name,wx_open_id from pub_ele_sign_users WHERE qq = '{}'".format(where)
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
        sql = " select state,mobile from pub_ele_sign_users where qq = '{}' ".format(where)
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
        sql = " update pub_ele_sign_users set state = {} where qq = '{}' ".format(True, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    def up_sign_open2(self, where):
        sql = " update pub_ele_sign_users set state = {} where qq = '{}' ".format(False, where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
    # # 查询公众号绑定库
    def select_bind_users(self, where):
        sql = " SELECT wx_open_id,is_bind,qq FROM pub_bind_users WHERE bind_name = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def select_bind_users_qq(self, qq, where):
        sql = " SELECT bind_name FROM pub_bind_users WHERE qq = '{}' ".format(qq)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        if not values:
            usql1 = " update pub_bind_users set qq = '{}',is_bind = {} where bind_name = '{}' ".format(qq, True, where)
            # 执行SQL
            cursor.execute(usql1)
            self.conn.commit()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values
    def set_binds(self, bind_name, where, qq):
        sign, card = False, False
        sql1 = " SELECT * FROM pub_ele_sign_users WHERE wx_open_id = '{}' ".format(where)
        sql2 = " SELECT * FROM pub_card_users WHERE wx_open_id = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql1)
        values1 = cursor.fetchall()
        if values1:
            usql1 = " update pub_ele_sign_users set bind_name = '{}',qq = '{}' where wx_open_id = '{}' ".format(bind_name, qq, where)
            # 执行SQL
            cursor.execute(usql1)
            self.conn.commit()
            sign = True
        cursor.execute(sql2)
        values2 = cursor.fetchall()
        if values2:
            usql2 = " update pub_card_users set bind_name = '{}',qq = '{}' where wx_open_id = '{}' ".format(bind_name, qq, where)
            # 执行SQL
            cursor.execute(usql2)
            self.conn.commit()
            card = True
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return [sign, card]
    def select_bind_is_users(self, where):
        sql = " SELECT wx_open_id,is_bind FROM pub_bind_users WHERE qq = '{}' ".format(where)
        # 找到cursor
        cursor = self.conn.cursor()
        # 执行SQL
        cursor.execute(sql)
        values = cursor.fetchall()
        # 关闭cursor/链接
        cursor.close()
        self.close_conn()
        return values

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