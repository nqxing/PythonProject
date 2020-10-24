from config.fun_api import *
from plugins.ele_sign.sign_v2 import sign, cx_sign


class my_thread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    def run(self):
        send_sign(self.bot)
def send_sign_index(bot):
    th = my_thread(bot)  # id, name
    th.start()

def send_sign(bot):
    values = SQL().select_sign_sid()
    if values:
        for v in values:
            wx_open_id, wx_bz, qq, sid, users_id = v[0], v[1], v[2], v[3], v[4]
            results = sign(sid, users_id)
            # print(results)
            if type(results).__name__ == 'list':
                wx_str = '【{}饿了么签到结果：签到成功】\n\n今日签到红包领取如下：\n'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
                SQL().up_is_sign(users_id)
                for r in range(len(results)):
                    r_str = '{}.{}\n'.format(r + 1, results[r])
                    wx_str += r_str
                result = cx_sign(sid, users_id)
                wx_str += result
                strs = SQL().select_var_info('ELE_KL')
                if strs:
                    ad_str = '\n\n-------------\n没有心意红包？复制这条信息[{}]，到【手机淘宝】试试，最高领31元'.format(strs)
                    wx_str += ad_str
                if wx_bz != None:
                    fids = bot.search(wx_bz)
                    if fids:
                        if len(fids) == 1:
                            fids[0].send(wx_str)
                        else:
                            for f in fids:
                                f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                if wx_bz == f_str:
                                    f.send(wx_str)
                if qq != None:
                    send_qq_private(int(qq), wx_str)
                sign_txt(wx_open_id, wx_str)
            else:
                wx_str = '【{}饿了么签到结果：{}】'.format(datetime.datetime.now().strftime('%Y-%m-%d'), results)
                if results == '未登录':
                    dl_str = '\n\n身份验证过期了，请发送关键字“修改手机号”进行重新绑定，为避免打扰本次已默认为您关闭饿了么自动签到，重新绑定身份后，你可继续使用签到功能哦'
                    wx_str += dl_str
                    SQL().up_sign_open2(users_id)
                if '昨天还没有签到' in results:
                    dl_str = '\n\n请今天去APP手动签到下，明天即可正常签到了哦，发送“关闭饿了么签到”可停止签到'
                    wx_str += dl_str
                if '签到失败' in results:
                    dl_str = '\n\n请确认今天是否已手动签到过哦，若没有请去APP手动签到下试试'
                    wx_str += dl_str
                strs = SQL().select_var_info('ELE_KL')
                if strs:
                    ad_str = '\n\n-------------\n没有心意红包？复制这条信息{}，到【手机淘宝】试试，最高领31元'.format(strs)
                    wx_str += ad_str
                if wx_bz != None:
                    fids = bot.search(wx_bz)
                    if fids:
                        if len(fids) == 1:
                            fids[0].send(wx_str)
                        else:
                            for f in fids:
                                f_str = re.findall(':(.*?)>', str(f))[0].strip()
                                if wx_bz == f_str:
                                    f.send(wx_str)
                if qq != None:
                    send_qq_private(int(qq), wx_str)
                sign_txt(wx_open_id, wx_str)