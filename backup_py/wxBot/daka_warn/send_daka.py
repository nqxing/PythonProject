import time
import datetime
import sqlite3
from config.config import ELEME_DATA_PATH, RILI_PATH
from random import randint  # 随机函数
from rili.get_rili import get_rili, get_jishi, get_lishi_jt
import re
import threading

class my_thread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    def run(self):
        send_daka(self.bot)
def send_daka_index(bot):
    th = my_thread(bot)  # id, name
    th.start()

def send_daka(bot):
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    conn_rl = sqlite3.connect(RILI_PATH)
    cursor_rl = conn_rl.cursor()

    date_id = datetime.datetime.now().strftime('%Y%m%d')
    cursor_rl.execute(
        '''select is_jishi from rilibiao WHERE date_id = '{}' '''.format(date_id))
    values = cursor_rl.fetchall()
    if values[0][0] == 'no':
        dq_time = datetime.datetime.now().strftime('%H:%M')
        hours = datetime.datetime.now().strftime('%H')
        cursor.execute(
            "SELECT wx_beizhu,tx_time_num,is_shouci FROM daka_vip WHERE state = 'yes' and tx_time LIKE '%" + "{}".format(
                dq_time) + "%'")
        results = cursor.fetchall()
        if len(results) != 0:
            riqi_str, week_str, tx_str = None, None, None
            if int(hours) > 22 or int(hours) <= 4:
                cursor.execute("SELECT text1 FROM daka_text")
                text1_list = cursor.fetchall()
                tx_str = text1_list[randint(0, len(text1_list) - 1)][0]
            if int(hours) > 4 and int(hours) <= 10:
                cursor.execute("SELECT text2 FROM daka_text")
                text2_list = cursor.fetchall()
                tx_str = text2_list[randint(0, len(text2_list) - 1)][0]
            if int(hours) > 10 and int(hours) <= 13:
                if int(hours) == 11:
                    cursor.execute("SELECT text3 FROM daka_text")
                    text3_list = cursor.fetchall()
                    tx_str = text3_list[randint(0, len(text3_list) - 1)][0]
                else:
                    cursor.execute("SELECT text4 FROM daka_text")
                    text4_list = cursor.fetchall()
                    tx_str = text4_list[randint(0, len(text4_list) - 1)][0]
            if int(hours) > 13 and int(hours) <= 15:
                cursor.execute("SELECT text5 FROM daka_text")
                text5_list = cursor.fetchall()
                tx_str = text5_list[randint(0, len(text5_list) - 1)][0]
            if int(hours) > 15 and int(hours) <= 22:
                cursor.execute("SELECT text6 FROM daka_text")
                text6_list = cursor.fetchall()
                tx_str = text6_list[randint(0, len(text6_list) - 1)][0]
            times = datetime.datetime.now().strftime('%Y%m%d')
            riqi_list = get_rili(times)
            if riqi_list:
                riqi_str = riqi_list[0][2]
                if riqi_list[0][3] == '1':
                    week_str = '星期一'
                elif riqi_list[0][3] == '2':
                    week_str = '星期二'
                elif riqi_list[0][3] == '3':
                    week_str = '星期三'
                elif riqi_list[0][3] == '4':
                    week_str = '星期四'
                elif riqi_list[0][3] == '5':
                    week_str = '星期五'
                elif riqi_list[0][3] == '6':
                    week_str = '星期六'
                elif riqi_list[0][3] == '7':
                    week_str = '星期天'
            jishis = get_jishi(riqi_list[0][0])
            lishi_jt = datetime.datetime.now().strftime('%m%d')
            lishi_jt_str = get_lishi_jt(lishi_jt)
            lishi_list = lishi_jt_str[0][0].split('#')
            lishi_jt_list = lishi_list[randint(0, len(lishi_list) - 1)].split("|")
            year = lishi_jt_list[0].split('年')
            sub_str = '{}({},{})\n{}年的今天{}，距离{}还有{}天。'.format(riqi_str, week_str, riqi_list[0][4], year[0],
                                                              lishi_jt_list[1], jishis[0][1],
                                                              int(jishis[0][0]) - int(riqi_list[0][0]))
            yuju = riqi_list[0][6]
            for r in results:
                if r[1] == '1':
                    wx_str = '{}\n\n{}\n\n{}\n-------------\n发送“关闭打卡提醒”可停止提醒打卡'.format(tx_str, sub_str, yuju)
                    fids = bot.search(r[0])
                    if fids:
                        if len(fids) == 1:
                            fids[0].send(wx_str)
                        else:
                            for f in fids:
                                f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                if r[0] == f_str:
                                    f.send(wx_str)
                else:
                    if r[2] == 'yes':
                        wx_str = '{}\n\n{}\n\n{}\n-------------\n发送“关闭打卡提醒”可停止提醒打卡'.format(tx_str, sub_str, yuju)
                        cursor.execute("UPDATE daka_vip SET is_shouci = 'no' where wx_beizhu = '{}'".format(r[0]))
                        conn.commit()
                    else:
                        wx_str = tx_str
                    fids = bot.search(r[0])
                    if fids:
                        if len(fids) == 1:
                            fids[0].send(wx_str)
                        else:
                            for f in fids:
                                f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                if r[0] == f_str:
                                    f.send(wx_str)
                time.sleep(0.3)