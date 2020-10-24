from wxpy import *
from config.config import ELEME_DATA_PATH
import logging.handlers
import sqlite3
import re
from wenku.wenku import get_wenku
from garbage.garbage import get_garbage, cx_garbage
from remove_bg.remove_bg import get_bg_image
from eleme.sign.add_sign import eleme_sign_open, eleme_sign_close, eleme_sign_verify_mobile, eleme_sign_verify_code
from bizhi.wzry.wzry import get_wzry
from bizhi.yxlm.yxlm import get_yxlm
from daka_warn.add_daka import daka_open, daka_close, daka_update_time
from admin.admin_zl import admin_zl
from eleme.is_eleme_vip import is_vip_true, is_vip_false


LOG_FILE = r'log\eleme_wx.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('eleme_wx')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')

@bot.register() #Friend
def print_others(msg):
    msg_type, text, sender = msg.type, msg.text, msg.sender
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    cursor.execute("select puid from eleme_vip")
    vip_puid = cursor.fetchall()
    cursor.execute("select wx_beizhu from eleme_vip")
    vip_beizhu = cursor.fetchall()
    puid = (msg.sender.puid,)
    # print(puid)
    beizhu = re.findall(':(.*?)>', str(msg.sender))[0].strip()
    beizhu = (beizhu,)
    # logger.info('{} 发送了 > {}'.format(beizhu[0], text))
    # print('{} 发送了 > {}'.format(beizhu[0], text))
    if '菜单' == text and 'Friend' in str(sender):
        cursor.execute("select text from eleme_text where id = 1")
        strs1 = '收到指令~ 老板，下面是俺目前会的一些功能，请查阅~\n\n'
        strs = cursor.fetchall()
        strs = strs[0][0].replace('|', '\n\n')
        msg.reply(strs1+strs)

    if msg_type == 'Picture' and 'Friend' in str(sender):
        get_bg_image(msg)

    if '王者荣耀壁纸群' in str(sender) and 'Group' in str(sender):
        get_wzry(text, msg)
    if '英雄联盟壁纸群' in str(sender) and 'Group' in str(sender):
        get_yxlm(text, msg)

    if 'https' in text and '//wenku.baidu.com' in text or '//wk.baidu.com' in text and 'Friend' in str(sender):
        get_wenku(text, msg)

    if len(cx_garbage(text)) != 0 and text != '使用' and len(text) != 0 and 'Friend' in str(sender):
        get_garbage(text, msg)

    if '：' in text or ':' in text and 'Friend' in str(sender):
        daka_update_time(beizhu, puid, msg, text)
    if '开启打卡提醒' == text and 'Friend' in str(sender):
        daka_open(beizhu, puid, msg, logger)
    if '关闭打卡提醒' == text and 'Friend' in str(sender):
        daka_close(beizhu, puid, msg)

    if '开启饿了么签到' == text and 'Friend' in str(sender):
        eleme_sign_open(beizhu, puid, msg, logger)
    if '关闭饿了么签到' == text and 'Friend' in str(sender):
        eleme_sign_close(beizhu, puid, msg)
    if len(text) == 11 and text.isdigit() and 'Friend' in str(sender):
        eleme_sign_verify_mobile(beizhu, puid, msg, text, logger)
    if len(text) == 6 and text.isdigit() and 'Friend' in str(sender):
        eleme_sign_verify_code(beizhu, puid, msg, text, logger)

    if puid in vip_puid or beizhu in vip_beizhu and 'Friend' in str(sender):
        is_vip_true(beizhu, puid, msg_type, msg, bot, text, logger)
    else:
        is_vip_false(beizhu, puid, msg_type, sender, msg, bot, text, logger)

    if '/大号' == beizhu[0]:
        admin_zl(bot, msg, text, logger)

    if '加入饿了么大包群' == text and 'Friend' in str(sender):
        wxpy_groups = bot.search('饿了么大包')
        logger.info(wxpy_groups)
        if len(wxpy_groups) == 1:
            group = wxpy_groups[0]
            group.add_members(msg.sender, use_invitation=True)
        else:
            fid = bot.search('/大号')[0]
            fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
            fid.send(wxpy_groups)
            logger.info('开启大红包群推送失败，未找到该群或找到了多个')
    if '英雄联盟' == text and 'Friend' in str(sender):
        wxpy_groups = bot.search('英雄联盟壁纸群')
        logger.info(wxpy_groups)
        if len(wxpy_groups) == 1:
            group = wxpy_groups[0]
            group.add_members(msg.sender, use_invitation=True)
        else:
            fid = bot.search('/大号')[0]
            fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
            fid.send(wxpy_groups)
            logger.info('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
    if '王者荣耀' == text and 'Friend' in str(sender):
        wxpy_groups = bot.search('王者荣耀壁纸群')
        logger.info(wxpy_groups)
        if len(wxpy_groups) == 1:
            group = wxpy_groups[0]
            group.add_members(msg.sender, use_invitation=True)
        else:
            fid = bot.search('/大号')[0]
            fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
            fid.send(wxpy_groups)
            logger.info('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))

    # if '充值' == text and 'Friend' in str(sender):
    #     logger.info('{} - 发送了充值'.format(sender))
    #     cursor.execute("select text from eleme_text where id = 2")
    #     strs = cursor.fetchall()[0][0]
    #     msg.reply(strs)
        # msg.sender.send_image('wxh.jpg')
        # msg.reply('如需充值次数，请加图中微信，当前充值价格为：\n1元 / 4次\n5元 / 25次（送5次）\n10元 / 50次（送10次）\n首充满（含）1元，送5次领取次数')

    # 判断好友请求中的验证文本
    if '最趣分享' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        cursor.execute("select text from eleme_text where id = 1")
        strs1 = 'Hi~ 欢迎来自公众号的朋友~\n\n下面是俺目前会的一些功能，请查阅哈~\n\n'
        strs = cursor.fetchall()
        strs = strs[0][0].replace('|', '\n\n')
        # 向新的好友发送消息
        new_friend.send(strs1+strs)
    else:
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        strs = 'Hi~ 你好啊!\n\n你加我绝对不是仅仅因为我长得好看吧[害羞]~\n\n既然不是，那你还不快发送”菜单“让我介绍下我自己~'
        new_friend.send(strs)

bot.join()

