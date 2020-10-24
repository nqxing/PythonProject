from config.fun_api import *
from config.config import *
from plugins.ele_hbao.hongbao_jk import wx_index

btime = 0

def is_sharing(beizhu, sender, msg, text):
    global btime
    if '饿了么外卖超市药店鲜花' in text and '领最大红包' in text:
        strs = SQL().select_var_info("ELE_JK")
        if strs == "True":
            if 'Friend' in str(sender) or beizhu[0] == '饿了么大包':
                # global btime, id
                bianhao = datetime.datetime.now().strftime('%H%M%S')
                etime = int(time.time())
                if etime - btime < 5:
                    stime = 5 - (etime - btime)
                    write_log(1, '{} - 分享红包的速度太快，已等待{}秒'.format(msg.sender, stime))
                    msg.reply('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                    time.sleep(stime)
                btime = etime
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    write_log(1, '{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                    msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                    # if 'Friend' in str(sender):
                    #     msg.reply('检测到您可以使用一键领大包功能（无需等待，系统直接帮你点到最佳前一个），如需使用，请发送“一键领大包”即可开通此功能哦')
                    # 拿到sn码调用到红包监控方法（该方法为异步执行）
                    wx_index(group_sn, bianhao, alink, msg)
                except:
                    write_log(3, '{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
                    msg.reply('出错了，识别红包链接错误，请换个红包看看吧')

            if 'Group' in str(sender) and beizhu[0] != '饿了么大包':
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    hongbaoMax = int(re.findall('第(.*?)个', msg.text)[0])
                    bianhao = datetime.datetime.now().strftime('%H%M%S')
                    SQL().add_ele_hb(bianhao, group_sn, hongbaoMax, alink, True, "微信红包互助群")
                except:
                    write_log(3, '{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))