from config.fun_api import *
from plugins.clock_in.rili.get_rili import get_rili, get_jishi, get_lishi_jt

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
    date_id = datetime.datetime.now().strftime('%Y%m%d')
    value = SQL().select_is_holiday(date_id)
    if value == False:
        dq_time = datetime.datetime.now().strftime('%H:%M')
        hours = datetime.datetime.now().strftime('%H')
        results = SQL().select_card(dq_time)
        if len(results) != 0:
            riqi_str, week_str, tx_str = None, None, None
            if int(hours) > 22 or int(hours) <= 4:
                tx_str = "辛苦了~ 这么晚了还要工作~ 记得打卡哦~"
            if int(hours) > 4 and int(hours) <= 10:
                tx_str = "早啊~ 今天也是美美的一天~ 记得打卡哦~"
            if int(hours) > 10 and int(hours) <= 13:
                if int(hours) == 11:
                    tx_str = "一天已快过半, 饿不饿呀~ 记得打卡哦~"
                else:
                    tx_str = "一天已经过半了, 饿不饿呀~ 记得打卡哦~"
            if int(hours) > 13 and int(hours) <= 15:
                tx_str = "好困啊啊! 不想上班，我要睡觉~ 记得打卡哦~"
            if int(hours) > 15 and int(hours) <= 22:
                tx_str = "忙碌一天了, 好好犒劳下自己吧~ 记得打卡哦~"
            times = datetime.datetime.now().strftime('%Y%m%d')
            riqi_list = get_rili(times)
            if riqi_list:
                riqi_str = riqi_list[0][2]
                if riqi_list[0][4] == 1:
                    week_str = '星期一'
                elif riqi_list[0][4] == 2:
                    week_str = '星期二'
                elif riqi_list[0][4] == 3:
                    week_str = '星期三'
                elif riqi_list[0][4] == 4:
                    week_str = '星期四'
                elif riqi_list[0][4] == 5:
                    week_str = '星期五'
                elif riqi_list[0][4] == 6:
                    week_str = '星期六'
                elif riqi_list[0][4] == 7:
                    week_str = '星期天'
            jishis = get_jishi(riqi_list[0][0])
            lishi_jt = datetime.datetime.now().strftime('%m%d')
            lishi_jt_str = get_lishi_jt(lishi_jt)
            lishi_list = lishi_jt_str[0][0].split('#')
            lishi_jt_list = lishi_list[randint(0, len(lishi_list) - 1)].split("|")
            year = lishi_jt_list[0].split('年')
            sub_str = '{}({},{})\n{}年的今天{}，距离{}还有{}天。'.format(riqi_str, week_str, riqi_list[0][5], year[0],
                                                              lishi_jt_list[1], jishis[0][1],
                                                              int(jishis[0][0]) - int(riqi_list[0][0]))
            yuju = riqi_list[0][3]
            for r in results:
                if r[2] == 1:
                    wx_str = '{}\n\n{}\n\n{}\n-------------\n发送“关闭打卡提醒”可停止提醒打卡，如需修改提醒时间请发送“修改时间”'.format(tx_str, sub_str, yuju)
                    if r[0] != None:
                        fids = bot.search(r[0])
                        if fids:
                            if len(fids) == 1:
                                fids[0].send(wx_str)
                            else:
                                print(fids)
                                for f in fids:
                                    f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                    if r[0] == f_str:
                                        f.send(wx_str)
                    if r[1] != None:
                        send_qq_private(int(r[1]), wx_str)
                else:
                    if r[3] == True:
                        wx_str = '{}\n\n{}\n\n{}\n-------------\n发送“关闭打卡提醒”可停止提醒打卡，如需修改提醒时间请发送“修改时间”'.format(tx_str, sub_str, yuju)
                        SQL().up_is_first(r[4])
                    else:
                        wx_str = tx_str
                    if r[0] != None:
                        fids = bot.search(r[0])
                        if fids:
                            if len(fids) == 1:
                                fids[0].send(wx_str)
                            else:
                                for f in fids:
                                    f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                    if r[0] == f_str:
                                        f.send(wx_str)
                    if r[1] != None:
                        send_qq_private(int(r[1]), wx_str)
                time.sleep(0.3)