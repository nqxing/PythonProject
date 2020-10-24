import sqlite3
# from eleme.sign.sign import sign, cx_sign
from eleme.sign.sign_v2 import sign, cx_sign
from config.config import ELEME_DATA_PATH
import re
import threading

class my_thread(threading.Thread):
    def __init__(self, bot, logger):
        threading.Thread.__init__(self)
        self.bot = bot
        self.logger = logger
    def run(self):
        send_sign(self.bot, self.logger)
def send_sign_index(bot, logger):
    th = my_thread(bot, logger)  # id, name
    th.start()

def send_sign(bot, logger):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute(
        '''SELECT wx_beizhu, sid, users_id FROM eleme_sign WHERE state = 'yes' AND is_bd = 'yes' ''')  # 查找饿了么库里的账号表，目前只取第一个账号
    values = cursor.fetchall()
    # cursor.execute(
    #     ''' SELECT wx_beizhu, sid, users_id FROM eleme_sign WHERE id in(1,2,3) ''')  # 查找饿了么库里的账号表，目前只取第一个账号
    # values = cursor.fetchall()
    if values:
        for v in values:
            wx_bz, sid, users_id = v[0], v[1], v[2]
            results = sign(sid, users_id, logger)
            # print(results)
            if type(results).__name__ == 'list':
                wx_str = '【饿了么签到结果：签到成功】\n\n今日签到红包领取如下：\n'
                cursor.execute("UPDATE eleme_sign SET is_qd = 'yes' where wx_beizhu = '{}'".format(wx_bz))
                conn.commit()
                for r in range(len(results)):
                    r_str = '{}.{}\n'.format(r + 1, results[r])
                    wx_str += r_str
                result = cx_sign(sid, users_id, logger)
                wx_str += result
                cursor.execute("select text from eleme_text where id = 3")
                strs = cursor.fetchall()[0][0]
                if strs:
                    ad_str = '\n\n-------------\n没有心意红包？复制这条信息[{}]，到【手机淘宝】试试，最高领31元'.format(strs)
                    wx_str += ad_str
                fids = bot.search(wx_bz)
                if fids:
                    if len(fids) == 1:
                        fids[0].send(wx_str)
                    else:
                        for f in fids:
                            f_str = re.findall(':(.*?)>', str(f))[0].strip()
                            if wx_bz == f_str:
                                f.send(wx_str)
            else:
                wx_str = '【饿了么签到结果：{}】'.format(results)
                if results == '未登录':
                    dl_str = '\n\n身份验证过期了，请重新发送手机号进行绑定，为避免打扰本次已默认为您关闭饿了么自动签到\n请发送手机号重新绑定身份后，发送“开启饿了么签到”继续使用签到功能'
                    wx_str += dl_str
                    cursor.execute("UPDATE eleme_sign SET state = 'no' where wx_beizhu = '{}'".format(wx_bz))
                    conn.commit()
                if '昨天还没有签到' in results:
                    dl_str = '\n\n请今天去APP手动签到下，明天即可正常签到了哦，发送“关闭饿了么签到”可停止签到'
                    wx_str += dl_str
                if '签到失败' in results:
                    dl_str = '\n\n请去APP手动签到下试试'
                    wx_str += dl_str
                cursor.execute("select text from eleme_text where id = 3")
                strs = cursor.fetchall()[0][0]
                if strs:
                    ad_str = '\n\n-------------\n没有心意红包？复制这条信息[{}]，到【手机淘宝】试试，最高领31元'.format(strs)
                    wx_str += ad_str
                fids = bot.search(wx_bz)
                if fids:
                    if len(fids) == 1:
                        fids[0].send(wx_str)
                    else:
                        for f in fids:
                            f_str = re.findall(':(.*?)>', str(f))[0].strip()
                            if wx_bz == f_str:
                                f.send(wx_str)