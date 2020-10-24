from config.config import ELEME_DATA_PATH
from kuq.content_get import get_hbnum_fqq
from kuq.content_get import stop_jk
from kuq.content_get import get_content, ins_stop
import sqlite3, pymysql
from eleme.is_eleme_vip import get_hbnum
from eleme.hongbao.hongbao_jk_fqq import jk_fqq_hongbao
from eleme.hongbao.hongbao_jk import jk_db_hongbao
from eleme.hongbao.hongbao_jk_over import jk_over_hongbao
import threading
from config.config import HOST, USER, PWD
from kuq.fkuq_wx import kuq_main
from bizhi.news_aps import index_news
from bizhi.wzry.get_wzry_bizhi import get_wzry_link
from bizhi.yxlm.get_yxlm_bizhi import get_yxlm_link
from bizhi.wzry.wzry import send_fqq
from eleme.hongbao.hongbao_lucky_me import lucky_main
import datetime

class jk_db_thread(threading.Thread):
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
        jk_db_hongbao(self.group_sn, self.th_id, self.alink, self.wxmsg, self.logger, self.bot)
def jk_db_index(group_sn, bianhao, alink, wxmsg, logger, bot):
    th = jk_db_thread(bianhao, group_sn, alink, wxmsg, logger, bot)  # id, name
    th.start()
    th.setName('hb_{}'.format(bianhao))

class jk_fqq_thread(threading.Thread):
    def __init__(self, bianhao, group_sn, alink, group, dahao, hz_group, logger, uid):
        threading.Thread.__init__(self)
        self.th_id = bianhao
        self.group_sn = group_sn
        self.alink = alink
        self.group = group
        self.dahao = dahao
        self.hz_group = hz_group
        self.logger = logger
        self.uid = uid
    def run(self):
        jk_fqq_hongbao(self.group_sn, self.th_id, self.alink, self.group, self.dahao, self.hz_group, self.logger, self.uid, False)
def jk_fqq_index(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid):
    th = jk_fqq_thread(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid)  # id, name
    th.start()
    th.setName('hongbao{}'.format(bianhao))


def admin_zl(bot, msg, text, logger):
    # print('进入大号')
    if '/查看任务数' == text:
        hbNameList = get_hbnum()
        msg.reply('当前后台共有{}个红包在监控'.format(len(hbNameList)))
        msg.reply(hbNameList)
    elif '/查看群聊任务数' == text:
        hbNameList = get_hbnum_fqq()
        msg.reply('当前群聊后台共有{}个红包在监控'.format(len(hbNameList)))
        msg.reply(hbNameList)
    elif '/开启消息转发' == text:
        kuq_main(bot)
    elif '/领红包' == text:
        msg.reply('红包领取中')
        lucky_main()
        msg.reply('领取完毕')
    elif '/菜单信息' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("select text from eleme_text where id = 1")
        strs = cursor.fetchall()
        msg.reply(strs[0][0])
    elif '/修改菜单信息' in text and '-' in text:
        values = text.split('-')
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_text SET text = '{}' where id = 1".format(values[1]))
        conn.commit()
        cursor.execute("select text from eleme_text where id = 1")
        strs = cursor.fetchall()
        msg.reply('已更新为：\n\n{}'.format(strs[0][0]))
    elif '/修改淘口令' in text and '-' in text:
        values = text.split('-')
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_text SET text = '{}' where id = 3".format(values[1]))
        conn.commit()
        cursor.execute("select text from eleme_text where id = 3")
        strs = cursor.fetchall()
        msg.reply('已更新为：\n\n{}'.format(strs[0][0]))
    elif '/开启过期监控' == text:
        dahao = bot.search('/大号')[0]
        jk_over_hongbao(dahao)
        logger.info('已开启过期红包监控')
    elif '/开启新闻监控' == text:
        wzry_groups = bot.search('王者荣耀壁纸群')
        yxlm_groups = bot.search('英雄联盟壁纸群')
        if len(wzry_groups) == 1 and len(yxlm_groups) == 1:
            index_news({'wzry': wzry_groups, 'yxlm': yxlm_groups})
        else:
            fid = bot.search('/大号')[0]
            fid.send('未找到该群或找到了多个{}{}'.format(wzry_groups, yxlm_groups))
    elif '/更新王者壁纸' == text:
        wzry_group = bot.search('王者荣耀壁纸群')
        if len(wzry_group) == 1:
            print('收到指令，正在更新壁纸')
            results = get_wzry_link()
            # print(results)
            if results:
                result = ''
                for i in results:
                    strs = '{}\n{}\n\n'.format(i[0], i[1])
                    result += strs
                send_str = '【{}更新】新增了如下英雄壁纸：\n\n{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), result.strip())
                wzry_group[0].send(send_str)
                send_fqq(send_str)
            print('壁纸更新完毕')
        else:
            fid = bot.search('/大号')[0]
            fid.send('未找到该群或找到了多个{}'.format(wzry_group))
    elif '/更新lol壁纸' == text:
        wzry_group = bot.search('英雄联盟壁纸群')
        if len(wzry_group) == 1:
            print('收到指令，正在更新壁纸')
            results = get_yxlm_link()
            # print(results)
            if results:
                result = ''
                for i in results:
                    strs = '{}\n{}\n\n'.format(i[0], i[1])
                    result += strs
                wzry_group[0].send('【{}更新】新增了如下英雄壁纸：\n\n{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), result.strip()))
            print('壁纸更新完毕')
        else:
            fid = bot.search('/大号')[0]
            fid.send('未找到该群或找到了多个{}'.format(wzry_group))
    elif '/开启群聊监控' == text:
        # wxpy_groups = bot.search('饿了么大包')
        # wxpy_groups1 = bot.search('饿了么红包互助')
        dahao = bot.search('/大号')[0]
        # logger.info(wxpy_groups)
        # if len(wxpy_groups) == 1 and len(wxpy_groups1) == 1:
        #     group = wxpy_groups[0]
        #     hz_group = wxpy_groups1[0]

        mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='eleme')
        mysql_cursor = mysql_conn.cursor()  # 获取游标
        mysql_cursor.execute(
            '''select bianhao, group_sn, alink, wx_beizhu, add_times from eleme_group_sn WHERE state = 'no' ''')  # 查找饿了么库里的账号表，目前只取第一个账号
        values = mysql_cursor.fetchall()
        db_num = 0
        if len(values) != 0:
            logger.info('查询到有未完成监控的红包，现进行重新监控')
            for v in values:
                if datetime.datetime.now().strftime('%Y-%m-%d') in v[4]:
                    if v[3] == '红包互助群':
                        pass
                        # jk_fqq_index(v[0], v[1], v[2], group, dahao, hz_group, logger, uid)
                    else:
                        jk_db_index(v[1], v[0], v[2], v[3], logger, bot)
                    db_num += 1
            logger.info('查询到{}个红包，但只有{}个红包符合条件重新加入监控系统'.format(len(values), db_num))
            dahao.send('查询到{}个红包，但只有{}个红包符合条件重新加入监控系统'.format(len(values), db_num))

        logger.info('已开启大红包群推送')
        get_content(True, bot)

        # else:
        #     fid = bot.search('/大号')[0]
        #     fid.send('开启大红包群推送失败，未找到该群或找到了多个')
        #     fid.send(wxpy_groups)
        #     fid.send(wxpy_groups1)
        #     logger.info('开启大红包群推送失败，未找到该群或找到了多个')
    elif '/关闭群聊监控' == text:
        msg.reply('收到指令，正在执行..')
        ins_stop()
        stop_jk()
        msg.reply('群聊监控推送已关闭')
    elif '/开启账号1自动抢包' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_lucky SET lucky_me = 'yes' WHERE id = 1")
        conn.commit()
        msg.reply('当前预置账号1自动抢包功能已开启')
    elif '/开启账号2自动抢包' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_lucky SET lucky_me = 'yes' WHERE id = 2")
        conn.commit()
        msg.reply('当前预置账号2自动抢包功能已开启')
    elif '/关闭账号1自动抢包' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_lucky SET lucky_me = 'no' WHERE id = 1")
        conn.commit()
        msg.reply('当前预置账号1自动抢包功能已关闭')
    elif '/关闭账号2自动抢包' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_lucky SET lucky_me = 'no' WHERE id = 2")
        conn.commit()
        msg.reply('当前预置账号2自动抢包功能已关闭')
    elif '/查看当前抢包状态' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("SELECT lucky_me FROM eleme_lucky WHERE id = 1")
        lucky_status = cursor.fetchall()[0][0]
        cursor.execute("SELECT lucky_me FROM eleme_lucky WHERE id = 2")
        lucky_status1 = cursor.fetchall()[0][0]
        msg.reply('收到指令，当前预置账号1抢包状态为：{} 账号2状态为：{}'.format(lucky_status, lucky_status1))
    elif '/测试' == text:
        # msg.reply('消息已接收，回复成功')
        fid = bot.search('/大号')[0]
        fid.send('消息已接收，回复成功')
    elif '/删除vip' in text and '-' in text:  # /删除vip-beizhu
        values = text.split('-')
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("DELETE FROM eleme_vip WHERE wx_beizhu = '{}'".format(values[1]))
        conn.commit()
        cursor.execute("SELECT wx_beizhu FROM eleme_vip")
        vip_beizhu = str(cursor.fetchall())
        if values[1] in vip_beizhu:
            msg.reply('{}，删除失败，请检查备注名是否输入错误'.format(values[1]))
        else:
            msg.reply('{}，删除成功'.format(values[1]))
            logger.info('{} - 收到指令，删除了{}'.format(msg.sender, values[1]))
    elif '/新增次数' in text and '-' in text:  # /新增次数-5-beizhu
        values = text.split('-')
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("select num from eleme_vip WHERE wx_beizhu = '{}'".format(values[2]))
        num = cursor.fetchall()[0][0]
        msg.reply('{}当前有{}次一键次数，本次操作会为Ta新增{}次'.format(values[2], num, values[1]))
        cursor.execute(
            "UPDATE eleme_vip SET num = {} WHERE wx_beizhu = '{}'".format(num + int(values[1]), values[2]))
        conn.commit()
        cursor.execute("select num from eleme_vip WHERE wx_beizhu = '{}'".format(values[2]))
        num1 = cursor.fetchall()[0][0]
        msg.reply('{}新增次数成功，新增后的次数为{}'.format(values[2], num1))
        logger.info('[会员]{} - 新增了{}次次数，新增前次数为{}，新增后的次数为{}'.format(values[2], values[1], num, num1))
    elif '/减少次数' in text and '-' in text:  # /减少次数-5-beizhu
        values = text.split('-')
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("select num from eleme_vip WHERE wx_beizhu = '{}'".format(values[2]))
        num = cursor.fetchall()[0][0]
        msg.reply('{}当前有{}次一键次数，本次操作会为Ta减少{}次'.format(values[2], num, values[1]))
        if int(values[1]) > num:
            msg.reply('{}减少次数失败，减少的次数大于该用户当前次数'.format(values[2]))
            logger.info('[会员]{} - 减少次数失败，减少的次数大于该用户当前次数'.format(values[2]))
        else:
            cursor.execute(
                "UPDATE eleme_vip SET num = {} WHERE wx_beizhu = '{}'".format(num - int(values[1]), values[2]))
            conn.commit()
            cursor.execute("select num from eleme_vip WHERE wx_beizhu = '{}'".format(values[2]))
            num1 = cursor.fetchall()[0][0]
            msg.reply('{}减少次数成功，减少后的次数为{}'.format(values[2], num1))
            logger.info('[会员]{} - 减少{}次次数成功，减少前次数为{}，减少后的次数为{}'.format(values[2], values[1], num, num1))
    elif '/更新次数' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("UPDATE eleme_xh SET is_ret_code = 'no'")
        conn.commit()
        msg.reply('更新成功')
    elif '/查看剩余小号' == text:
        conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
        cursor = conn.cursor()  # 获取游标
        cursor.execute("SELECT is_ret_code FROM eleme_xh")
        is_ret_code = cursor.fetchall()
        nums = []
        for i in is_ret_code:
            if i[0] == 'no':
                nums.append(i[0])
        msg.reply('系统当前剩余{}个小号有领取次数'.format(len(nums)))
