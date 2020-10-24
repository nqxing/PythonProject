from config.config import ELEME_DATA_PATH, HOST, PWD, USER
import sqlite3
import datetime
import re
import time
import threading
from eleme.hongbao.hongbao_jk import jk_hongbao
from eleme.hongbao.hongbao_xh import xh_hongbao
from kuq.content_get import wxGroup_jk
import pymysql

class my_thread(threading.Thread):
    def __init__(self, bianhao, group_sn, alink, wxmsg, logger, bot):
        threading.Thread.__init__(self)
        self.th_id = bianhao
        # self.th_name = th_name
        self.group_sn = group_sn
        self.alink = alink
        self.wxmsg = wxmsg
        self.logger = logger
        self.bot = bot
    def run(self):
        jk_hongbao(self.group_sn, self.th_id, self.alink, self.wxmsg, self.logger, self.bot)
def wx_index(group_sn, bianhao, alink, wxmsg, logger, bot):
    th = my_thread(bianhao, group_sn, alink, wxmsg, logger, bot)  # id, name
    th.start()
    th.setName('hb_{}'.format(bianhao))

def get_hbnum():
    hbList = threading.enumerate()
    hbNameList = []
    for hb in hbList:
        if 'hb_' in hb.name:
            hbNameList.append(hb.name)
    return hbNameList

vip_dict = {}
btime = 0

def is_vip_true(beizhu, puid, msg_type, msg, bot, text, logger):
    global btime, vip_dict
    # print('是vip')
    # print(msg.sender)
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select num from eleme_vip WHERE puid = '{}' OR wx_beizhu = '{}'".format(puid[0], beizhu[0]))
    vip_num = cursor.fetchall()[0][0]
    if '查看次数' == text:
        msg.reply('您当前还有{}次一键领大包次数哦'.format(vip_num))
    if vip_num > 0:
        # print('有次数')
        if 'https://h5.ele.me/hongbao/' in text and '&sn=' in text:
            logger.info('[会员]{} - 分享了红包链接，是vip，还有剩余次数{}'.format(beizhu[0], vip_num))
            bianhao = datetime.datetime.now().strftime('%H%M%S')
            try:
                alink = text
                group_sn = re.findall('sn=(.*?)&', alink)[0]
                logger.info('[会员]{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(beizhu[0], group_sn, bianhao))
                # print('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                vip_dict[puid[0]] = '{}|{}|{}'.format(group_sn, bianhao, alink)
                # print(vip_dict)
                msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                msg.reply('您当前有一键领大包次数，若本次需要使用一键领大包功能，请回复“使用”，不需要则回复“不使用”')
            except:
                logger.debug('[会员]{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(beizhu[0], msg.url))
                msg.reply('出错了，识别红包链接错误，请换个红包看看吧')
        if msg_type == 'Sharing':
            if '饿了么拼手气，第' in text or '【饿了么】第' in text:
                logger.info('[会员]{} - 分享了红包，是vip，还有剩余次数{}'.format(beizhu[0], vip_num))
                # global btime, id, vip_dict
                bianhao = datetime.datetime.now().strftime('%H%M%S')
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    logger.info('[会员]{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(beizhu[0], group_sn, bianhao))
                    # print('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                    vip_dict[puid[0]] = '{}|{}|{}'.format(group_sn, bianhao, alink)
                    # print(vip_dict)
                    msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                    msg.reply('您当前有一键领大包次数，若本次需要使用一键领大包功能，请回复“使用”，不需要则回复“不使用”')
                except:
                    logger.debug('[会员]{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(beizhu[0], msg.url))
                    msg.reply('出错了，识别红包链接错误，请换个红包看看吧')
        # elif '美团外卖' in text:
        #     msg.reply('目前只支持饿了么红包哦')
        #     logger.info('[会员]{} - 目前只支持饿了么红包哦'.format(beizhu[0]))
        elif '使用' == text and puid[0] in vip_dict:
            logger.info('[会员]{} - 使用了次数，进入一键领大包功能'.format(beizhu[0]))
            values = vip_dict[puid[0]]
            value = values.split('|')
            # 拿到sn码调用到红包监控方法（该方法为异步执行）
            # index(value[0], value[1], value[2], msg, logger, id)
            xh_hongbao(value[0], value[1], value[2], puid[0], beizhu[0], msg, logger)
            removed_value = vip_dict.pop(puid[0])
            # print(vip_dict)
            logger.info('[会员]{} - 【红包{}】使用了一键领大包系统，移除了字典key[{}]，对应value为[{}]'.format(beizhu[0], value[1], puid[0],
                                                                                     removed_value))
        elif '不使用' == text and puid[0] in vip_dict:
            logger.info('[会员]{} - 不使用次数，进入监控功能'.format(beizhu[0]))
            values = vip_dict[puid[0]]
            value = values.split('|')
            # 拿到sn码调用到红包监控方法（该方法为异步执行）
            wx_index(value[0], value[1], value[2], msg, logger, bot)
            removed_value = vip_dict.pop(puid[0])
            # print(vip_dict)
            logger.info(
                '[会员]{} - 【红包{}】已加入监控系统，移除了字典key[{}]，对应value为[{}]'.format(beizhu[0], value[1], puid[0], removed_value))
        elif '使用' == text or '不使用' == text:
            msg.reply('请先分享红包哦')
            logger.info('[会员]{} - 请先分享红包哦'.format(beizhu[0]))
    else:
        # print('是vip,没有次数')
        if 'https://h5.ele.me/hongbao/' in text and '&sn=' in text:
            logger.info('[会员]{} - 分享了红包链接，是vip，但是没有次数了'.format(beizhu[0]))
            # global btime, id
            bianhao = datetime.datetime.now().strftime('%H%M%S')
            etime = int(time.time())
            if etime - btime < 5:
                stime = 5 - (etime - btime)
                logger.info('[会员]{} - 分享红包的速度太快，已等待{}秒'.format(beizhu[0], stime))
                # print('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                msg.reply('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                time.sleep(stime)
            btime = etime
            try:
                alink = text
                group_sn = re.findall('sn=(.*?)&', alink)[0]
                logger.info(
                    '[会员]{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】，该会员没有次数了，使用红包监控功能'.format(beizhu[0], group_sn, bianhao))
                # print('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                msg.reply('您的一键领大包次数已经用完，本次默认为您使用监控功能，如需充值次数请发送“充值”')
                # 拿到sn码调用到红包监控方法（该方法为异步执行）
                wx_index(group_sn, bianhao, alink, msg, logger, bot)
            except:
                logger.debug('{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
                msg.reply('出错了，识别红包链接错误，请换个红包看看吧')

        if msg_type == 'Sharing':
            if '饿了么拼手气，第' in text or '【饿了么】第' in text:
                logger.info('[会员]{} - 分享了红包，是vip，但是没有次数了'.format(beizhu[0]))
                # global btime, id
                bianhao = datetime.datetime.now().strftime('%H%M%S')
                etime = int(time.time())
                if etime - btime < 5:
                    stime = 5 - (etime - btime)
                    logger.info('[会员]{} - 分享红包的速度太快，已等待{}秒'.format(beizhu[0], stime))
                    # print('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                    msg.reply('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                    time.sleep(stime)
                btime = etime
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    logger.info(
                        '[会员]{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】，该会员没有次数了，使用红包监控功能'.format(beizhu[0], group_sn, bianhao))
                    # print('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                    msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                    # msg.reply('您的一键领大包次数已经用完，本次默认为您使用监控功能，如需充值次数请发送“充值”')
                    # 拿到sn码调用到红包监控方法（该方法为异步执行）
                    wx_index(group_sn, bianhao, alink, msg, logger, bot)
                except:
                    logger.debug('{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
                    msg.reply('出错了，识别红包链接错误，请换个红包看看吧')
            # elif '美团外卖' in text:
            #     logger.info('[会员]{} - 目前只支持饿了么红包哦'.format(beizhu[0]))
            #     msg.reply('目前只支持饿了么红包哦')

def is_vip_false(beizhu, puid, msg_type, sender, msg, bot, text, logger):
    global btime, id, vip_dict
    mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306,
                                 db='eleme')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    # conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    # cursor = conn.cursor()  # 获取游标
    # print('不是vip')
    if msg_type == 'Sharing':
        if '饿了么拼手气，第' in text or '【饿了么】第' in text:
            if 'Friend' in str(sender) or beizhu[0] == '饿了么大包':
                # global btime, id
                bianhao = datetime.datetime.now().strftime('%H%M%S')
                etime = int(time.time())
                if etime - btime < 5:
                    stime = 5 - (etime - btime)
                    logger.info('{} - 分享红包的速度太快，已等待{}秒'.format(msg.sender, stime))
                    msg.reply('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                    time.sleep(stime)
                btime = etime
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    logger.info('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                    msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                    # if 'Friend' in str(sender):
                    #     msg.reply('检测到您可以使用一键领大包功能（无需等待，系统直接帮你点到最佳前一个），如需使用，请发送“一键领大包”即可开通此功能哦')
                    # 拿到sn码调用到红包监控方法（该方法为异步执行）
                    wx_index(group_sn, bianhao, alink, msg, logger, bot)
                except:
                    logger.debug('{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
                    msg.reply('出错了，识别红包链接错误，请换个红包看看吧')

            elif 'Group' in str(sender) and beizhu[0] != '饿了么大包':
                conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
                cursor = conn.cursor()  # 获取游标
                cursor.execute('''select count from eleme_count WHERE id = 1 ''')  # 查找饿了么库
                bianhao = int(cursor.fetchall()[0][0])
                try:
                    alink = msg.url
                    group_sn = re.findall('sn=(.*?)&', alink)[0]
                    hongbaoMax = int(re.findall('第(.*?)个', msg.text)[0])

                    # wxpy_groups = bot.search('饿了么大包')
                    # wxpy_groups1 = bot.search('饿了么红包互助')
                    # dahao = bot.search('/大号')[0]
                    # if len(wxpy_groups) == 1 and len(wxpy_groups1) == 1:
                    #     group = wxpy_groups[0]
                    #     hz_group = wxpy_groups1[0]
                    # else:
                    #     group = dahao
                    #     hz_group = dahao
                    # 拿到sn码调用到红包监控方法（该方法为异步执行）

                    mysql_cursor.execute(
                        "INSERT INTO eleme_group_sn (bianhao, group_sn, yet, yet_max, alink, state, wx_beizhu, add_times) VALUES ('{}', '{}', 0, {}, '{}', 'yes', '红包互助群', '{}')".format(
                            bianhao, group_sn, hongbaoMax,
                            alink, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    )
                    mysql_conn.commit()

                    # wxGroup_jk(bianhao, group_sn, alink, group, dahao, hz_group, id)
                    # if id == ID_MAX:
                    #     id = 1
                    # else:
                    #     id += 1
                except:
                    logger.debug('{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
        # elif '美团外卖' in text:
        #     logger.info('{} - 目前只支持饿了么红包哦'.format(msg.sender))
        #     msg.reply(u'目前只支持饿了么红包哦')
    elif 'https://h5.ele.me/hongbao/' in text and '&sn=' in text:
        if 'Friend' in str(sender) or beizhu[0] == '饿了么大包':
            bianhao = datetime.datetime.now().strftime('%H%M%S')
            etime = int(time.time())
            if etime - btime < 5:
                stime = 5 - (etime - btime)
                logger.info('{} - 分享红包的速度太快，已等待{}秒'.format(msg.sender, stime))
                msg.reply('分享红包的速度太快啦，等待{}秒开始监控'.format(stime))
                time.sleep(stime)
            btime = etime
            try:
                alink = text
                group_sn = re.findall('sn=(.*?)&', alink)[0]
                logger.info('{} - 已捕获到饿了么红包sn[{}]，标记为【红包{}】'.format(msg.sender, group_sn, bianhao))
                msg.reply('已捕获到饿了么红包，标记为【红包{}】'.format(bianhao))
                # if 'Friend' in str(sender):
                #     msg.reply('检测到您可以使用一键领大包功能（无需等待，系统直接帮你点到最佳前一个），如需使用，请发送“一键领大包”即可开通此功能哦')
                # 拿到sn码调用到红包监控方法（该方法为异步执行）
                wx_index(group_sn, bianhao, alink, msg, logger, bot)
            except:
                logger.debug('{} - 出错了，识别红包链接错误，请换个红包看看吧，{}'.format(msg.sender, msg.url))
                msg.reply('出错了，识别红包链接错误，请换个红包看看吧')
    elif '一键领大包' == text and 'Friend' in str(sender):
        msg.reply('该功能已关闭')
    # elif '一键领大包' == text and 'Friend' in str(sender):
    #     bz_state = False
    #     num = None
    #     if 'vip_' in beizhu[0]:
    #         bz = beizhu[0]
    #     else:
    #         conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    #         cursor = conn.cursor()  # 获取游标
    #         # cursor.execute('''select count(*) from eleme_vip''')
    #         cursor.execute('''select count from eleme_count where id = 2''')
    #         num = int(cursor.fetchall()[0][0])
    #         bz = 'vip_{}'.format(num)
    #         bz_state = True
    #     cursor.execute(
    #         "INSERT INTO eleme_vip (puid, num, wx_beizhu, wx_name, kt_time) VALUES ('{}', {}, '{}', '{}', '{}')".format(
    #             puid[0], 1,
    #             bz, msg.sender, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #     conn.commit()
    #     cursor.execute("select puid from eleme_vip")
    #     vip_puid = str(cursor.fetchall())
    #     cursor.execute("select wx_beizhu from eleme_vip")
    #     vip_bz = cursor.fetchall()
    #     if puid[0] in vip_puid and bz in str(vip_bz):
    #         logger.info('{} 开启了一键领大包功能，请记得在两边设置Ta的唯一备注为：{}，Ta的puid为：{}'.format(msg.sender, bz, puid[0]))
    #         msg.reply('您的一键领大包功能开通成功，当前有1次一键领大包次数，快去分享红包给我吧\n注：发送“查看次数”可查看当前剩余次数哦')
    #         if bz_state:
    #             msg.sender.set_remark_name(bz)
    #             num += 1
    #             cursor.execute('''UPDATE eleme_count SET count = '{}' where id = 2'''.format(num))
    #             conn.commit()
    #         # fid = bot.search('/大号')[0]
    #         # fid.send('{} 开启了一键领大包功能\n请记得在两边设置Ta的唯一备注为：{}\nTa的puid为：{}'.format(msg.sender, bz, puid[0]))
    #     else:
    #         msg.reply('一键领大包功能开通失败，请稍后再试')
    # elif '查看次数' == text and 'Friend' in str(sender):
    #     msg.reply('请先发送“一键领大包”，开通此功能哦')