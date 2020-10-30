from wxpy import *
from plugins.ele_sign.sign_base import *
from plugins.ele_sign.send_sign import send_sign_index
from plugins.clock_in.clock_base import daka_open, daka_close, daka_update_time
from plugins.clock_in.run_clock import mon_clock
from plugins.ele_hbao.is_ele import is_sharing
from plugins.wz_amesvr import index_wqg

eleme_sign_dict = {}
card_dict = {}

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        # thr.setName(args[-1])
        thr.start()
    return wrapper

@asyncs
def del_action_dict(num, bz):
    time.sleep(300)
    if num == 1:
        if bz in eleme_sign_dict:
            value = eleme_sign_dict.pop(bz)
            write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(bz, value, len(eleme_sign_dict)))
    if num == 2:
        if bz in card_dict:
            value = card_dict.pop(bz)
            write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(bz, value, len(card_dict)))

def ruturn_tip(name):
    value = ''
    tips_list = list(TIPS.keys())
    for i in range(50):
        if name in TIPS:
            s = randint(0, len(tips_list)) - 1
            if name == tips_list[s]:
                pass
            else:
                value = TIPS[tips_list[s]]
                break
        else:
            break
    return value

# 初始化机器人，扫码登陆
# bot = Bot(cache_path=True)
bot = Bot(console_qr=True, cache_path=True)
# bot = Bot()
bot.enable_puid('wxpy_puid.pkl')

def reply(text, msg, beizhu, sender):
    try:
        if '菜单' == text and 'Friend' in str(sender):
            # "or '帮助' == text or '指令' == text"
            # write_log(1, 'test [{}]发送了微信消息[{}]'.format(sender, text))
            strs1 = SQL().select_var_info('WX_MENU')
            strs1 = strs1.replace('|', '\n')
            msg.reply(strs1)
            return 1

        if '$' in text:
            bd_code = re.findall('\$(.*?)\$', text)
            if bd_code:
                if len(bd_code[0]) == 8:
                    bd_str = bind_wx(bd_code[0], beizhu, msg)
                    msg.reply(bd_str)
                    return 1

        if 'Group' in str(sender):
            if msg.is_at == True:
                texts = text.split('@Bot')
                if texts[1].strip():
                    text = texts[1].strip()
                elif texts[0].strip():
                    text = texts[0].strip()
                else:
                    pass
                if '英雄联盟壁纸群' in str(sender):
                    try:
                        result = requests.get(GET_LOL_WALL_HOST.format(text))
                        msg.reply(result.text)
                    except:
                        msg.reply("系统异常，请联系群主处理")
                    # if "邀请" in text and "加入了群聊" in text:
                    #     msg.reply("欢迎新朋友~\n群里有全英雄高清无水印壁纸，需要请长按我头像@我英雄名字或皮肤的某个关键字获取哦")
                # try:
                #     result = requests.get(GET_WZ_WALL_HOST.format(new_text))
                #     msg.reply(result.text)
                # except:
                #     msg.reply("系统异常，请联系群主处理")
            # if "邀请" in text and "加入了群聊" in text:
            #     msg.reply("欢迎新朋友~\n群里有全英雄高清无水印壁纸，需要请长按我头像@我英雄名字或皮肤的某个关键字获取哦")
            elif '英雄联盟壁纸群' in str(sender):
                pass
            elif '壁纸' in text:
                text = text.strip().replace('壁纸', '')
                if text:
                    results = SQL().select_wz_wall(text)
                    if len(results) != 0:
                        result = '找到了{}张({})的壁纸:\n\n'.format(len(results), text)
                        for res in results:
                            mob_skin = res[6]
                            if mob_skin == None:
                                strs = '{}\n[电脑] {}\n\n'.format(res[1], res[5])
                            else:
                                strs = '{}\n[电脑] {}\n[手机] {}\n\n'.format(res[1], res[5],
                                                                         res[6])
                            result += strs
                        result = result.strip()
                        if len(result) > 1365:
                            msg.reply('该关键字信息量太大了，请换个详细点的关键字吧')
                        else:
                            t = ruturn_tip('bz')
                            rep_str = '{}||{}'.format(result, t.format(results[0][3], results[0][3])).replace('|', '\n')
                            msg.reply(rep_str.strip())
                    # else:
                    #     # return "没有找到({})的壁纸，请确认名字输入正确哦~".format(name) + end_str
                    #     pass
            elif '菜单' == text:
                strs1 = SQL().select_var_info('WZ_GROUP_MENU')
                strs1 = strs1.replace('|', '\n')
                msg.reply(strs1)
            elif '胜率' in text:
                results = SQL().select_wz_win_rate(text.strip())
                if results:
                    t = ruturn_tip('sl')
                    wins = SQL().select_wz_win_rates()
                    rep_str = '{}{}||{}'.format(results[0][0], wins, t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '技能' in text:
                results = SQL().select_wz_skill(text.strip())
                if results:
                    t = ruturn_tip('jn')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '出装' in text:
                results = SQL().select_wz_equip(text.strip())
                if results:
                    t = ruturn_tip('cz')
                    rep_str = '{}{}||{}'.format(results[0][0], results[0][1], t.format(results[0][2], results[0][2])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '铭文' in text:
                results = SQL().select_wz_rune(text.strip())
                if results:
                    t = ruturn_tip('mw')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '克制' in text:
                results = SQL().select_wz_kz(text.strip())
                if results:
                    t = ruturn_tip('kz')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '介绍' in text:
                results = SQL().select_wz_introduce(text.strip())
                if results:
                    t = ruturn_tip('js')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '组合' in text:
                results = SQL().select_wz_zh(text.strip())
                if results:
                    t = ruturn_tip('zh')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            elif '技巧' in text:
                results = SQL().select_wz_jq(text.strip())
                if results:
                    t = ruturn_tip('jq')
                    rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                    msg.reply(rep_str.strip())
            # elif '投票排行榜' == text:
            #     msg.reply(index_wqg())
            else:
                pass


        # if '修改手机号' == text and 'Friend' in str(sender):
        #     if "vip_" in beizhu[0]:
        #         values = SQL().select_sign_users(beizhu[0])
        #         if values and values[0][0] != None and values[0][1] != None:
        #             eleme_sign_dict[beizhu[0]] = 'mobile'
        #             del_action_dict(1, beizhu[0])
        #             msg.reply('请在5分钟内回复你要修改的手机号')
        #             return 0
        #         else:
        #             msg.reply(
        #                 '您未开启饿了么签到或未与公众号绑定，无法直接修改手机号\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
        #             return 1
        #     else:
        #         msg.sender.send_image('public.jpg')
        #         msg.reply(
        #             '您未开启饿了么签到或未与公众号绑定，无法直接修改手机号\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
        #         return 1

        # 打卡提醒功能20201016关闭

        # if '修改时间' == text and 'Friend' in str(sender):
        #     if "vip_" in beizhu[0]:
        #         values = SQL().select_clock(beizhu[0])
        #         if values and values[0][0] != None and values[0][1] != None:
        #             card_dict[beizhu[0]] = 'up_time'
        #             del_action_dict(2, beizhu[0])
        #             msg.reply('请在5分钟内回复你要修改的时间')
        #             return 0
        #         else:
        #             msg.reply(
        #                 '您未开启打卡提醒或未与公众号绑定，无法直接修改时间\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“打卡提醒”进行开启或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
        #             return 1
        #     else:
        #         msg.sender.send_image('public.jpg')
        #         msg.reply(
        #             '您未开启打卡提醒或未与公众号绑定，无法直接修改时间\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“打卡提醒”进行开启或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
        #         return 1

        # if '开启打卡提醒' == text and 'Friend' in str(sender):
        #     daka_open(card_dict, beizhu, msg)
        #     return 1
        # if '关闭打卡提醒' == text and 'Friend' in str(sender):
        #     daka_close(beizhu, msg)
        #     return 1
        #
        # if '开启饿了么签到' == text and 'Friend' in str(sender):
        #     eleme_sign_open(eleme_sign_dict, beizhu, msg)
        #     return 1
        #
        # if '关闭饿了么签到' == text and 'Friend' in str(sender):
        #     eleme_sign_close(beizhu, msg)
        #     return 1

        if '公众号' == text:
            msg.sender.send_image('public.jpg')
            msg.reply('更多好玩功能，请识别二维码关注公众号查看')
            return 1

        if 'vip_大号' == beizhu[0]:
            if '测试' == text:
                # msg.reply('消息已接收，回复成功')
                fid = bot.search('vip_大号')[0]
                fid.send('消息已接收，回复成功')
                return 1
            if '饿了么签到' == text:
                msg.reply('收到指令，开始执行')
                send_sign_index(bot)
                return 1
            if '开启监控' == text:
                msg.reply('收到指令，开始执行')
                mon_clock(bot)
                return 1
            if '字典' == text:
                msg.reply('{}\n{}'.format(eleme_sign_dict, card_dict))
                return 1

        if '加入饿了么大包群' == text or "红包群" == text and 'Friend' in str(sender):
            wxpy_groups = bot.search('美团饿了么红包互点')
            if len(wxpy_groups) == 1:
                group = wxpy_groups[0]
                group.add_members(msg.sender, use_invitation=True)
            else:
                fid = bot.search('vip_大号')[0]
                fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
                fid.send(wxpy_groups)
            return 1
        if '英雄联盟' == text and 'Friend' in str(sender):
            wxpy_groups = bot.search('英雄联盟壁纸群')
            if len(wxpy_groups) == 1:
                group = wxpy_groups[0]
                group.add_members(msg.sender, use_invitation=True)
            else:
                fid = bot.search('vip_大号')[0]
                fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
                fid.send(wxpy_groups)
            return 1
        if '王者荣耀' == text and 'Friend' in str(sender):
            wxpy_groups = bot.search('王者荣耀壁纸群')
            if len(wxpy_groups) == 1:
                group = wxpy_groups[0]
                group.add_members(msg.sender, use_invitation=True)
            else:
                fid = bot.search('vip_大号')[0]
                fid.send('邀请[{}]入群失败，未找到该群或找到了多个'.format(msg.sender))
                fid.send(wxpy_groups)
            return 1

        return -1
    except:
        write_log(3, traceback.format_exc())
        # send_qq_private(541116212, "微信机器人报错了，快去看看吧")
        fangtang("微信机器人报错了，快去看看吧", "微信机器人报错了，快去看看吧")

@bot.register() #Friend
def auto_reply(msg):
    msg_type = msg.type
    text, sender = msg.text, msg.sender
    # puid = (msg.sender.puid,)
    beizhu = re.findall(':(.*?)>', str(msg.sender))[0].strip()
    beizhu = (beizhu,)
    if msg_type == 'Text':
        reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
        new_name = re.sub(reg, '', beizhu[0])
        write_log(1, '[{}]发送了微信消息[{}]'.format(new_name, text))

        if "vip_" in beizhu[0] and 'Friend' in str(sender):
            if beizhu[0] in eleme_sign_dict:
                state = reply(text, msg, beizhu, sender)
                if state == 0:
                    pass
                if state == 1:
                    pass
                if state == -1:
                    eleme_sign_base(eleme_sign_dict, beizhu, text, msg)
            elif beizhu[0] in card_dict:
                state = reply(text, msg, beizhu, sender)
                if state == 0:
                    pass
                if state == 1:
                    pass
                if state == -1:
                    daka_update_time(card_dict, beizhu, msg, text)
            else:
                reply(text, msg, beizhu, sender)
        else:
            reply(text, msg, beizhu, sender)


    if msg_type == 'Sharing':
        is_sharing(beizhu, sender, msg, text)

    if msg_type == 'Friends':
        # 判断好友请求中的验证文本
        # if '最趣分享' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        strs = 'Hi~ 你好啊，很高兴我们能成为朋友~'
        strs = strs.replace('|', '\n')
        # 向新的好友发送消息
        new_friend.send(strs)
        strs1 = SQL().select_var_info('WX_MENU')
        strs1 = strs1.replace('|', '\n')
        # 向新的好友发送消息
        new_friend.send(strs1)

bot.join()

