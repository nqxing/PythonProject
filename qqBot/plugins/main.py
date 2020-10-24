from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import on_notice, NoticeSession, on_request, RequestSession
from plugins.ele_sign.sign_base import *
from plugins.clock_in.clock_base import *
from plugins.pub_fun.fun_api import *



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

def reply(stripped_msg, qq):
    reply_dict = {'code': -1, 'msg': ''}
    if '$' in stripped_msg:
        bd_code = re.findall('\$(.*?)\$', stripped_msg)
        if bd_code:
            if len(bd_code[0]) == 8:
                bd_str = bind_wx(bd_code[0], qq)
                reply_dict['code'] = 1
                reply_dict['msg'] = bd_str

    if qq == ADMIN:
        if '字典' == stripped_msg:
            reply_str = '{}\n{}'.format(eleme_sign_dict, card_dict)
            reply_dict['code'] = 1
            reply_dict['msg'] = reply_str

    if stripped_msg == '修改手机号':
        values = SQL().select_sign_users(qq)
        if values and values[0][0] != None and values[0][1] != None:
            eleme_sign_dict[qq] = 'mobile'
            del_action_dict(1, qq)
            reply_dict['code'] = 0
            reply_dict['msg'] = '请在5分钟内回复你要修改的手机号'
        else:
            reply_dict['code'] = 1
            reply_dict['msg'] = '您未开启饿了么签到或未与公众号绑定，无法直接修改手机号\n请打开微信搜一搜，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU'

    if stripped_msg == '修改时间':
        values = SQL().select_clock(qq)
        if values and values[0][0] != None and values[0][1] != None:
            card_dict[qq] = 'up_time'
            del_action_dict(2, qq)
            reply_dict['code'] = 0
            reply_dict['msg'] = '请在5分钟内回复你要修改的时间'
        else:
            reply_dict['code'] = 1
            reply_dict['msg'] = '您未开启打卡提醒或未与公众号绑定，无法直接修改时间\n请打开微信搜一搜，关注公众号(最趣分享)后发送关键字“打卡提醒”进行开启或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU'

    if stripped_msg == '开启饿了么签到':
        reply_str = eleme_sign_open(qq)
        reply_dict['code'] = 1
        reply_dict['msg'] = reply_str
    if stripped_msg == '关闭饿了么签到':
        reply_str = eleme_sign_close(qq)
        reply_dict['code'] = 1
        reply_dict['msg'] = reply_str

    if stripped_msg == '开启打卡提醒':
        reply_str = daka_open(qq)
        reply_dict['code'] = 1
        reply_dict['msg'] = reply_str
    if stripped_msg == '关闭打卡提醒':
        reply_str = daka_close(qq)
        reply_dict['code'] = 1
        reply_dict['msg'] = reply_str

    return reply_dict
# only_short_message=False 处理长消息
@on_natural_language(keywords=None, only_to_me=False, only_short_message=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    if session.ctx['message_type'] == 'private':
        qq = '{}'.format(session.ctx['user_id'])
        if qq in eleme_sign_dict:
            reply_dict = reply(stripped_msg, qq)
            state = reply_dict['code']
            if state == 0:
                await session.send(reply_dict['msg'])
            if state == 1:
                await session.send(reply_dict['msg'])
            if state == -1:
                reply_str = eleme_sign_base(qq, stripped_msg)
                await session.send(reply_str)
        elif qq in card_dict:
            reply_dict = reply(stripped_msg, qq)
            state = reply_dict['code']
            if state == 0:
                await session.send(reply_dict['msg'])
            if state == 1:
                await session.send(reply_dict['msg'])
            if state == -1:
                reply_str = daka_update_time(qq, stripped_msg)
                await session.send(reply_str)
        else:
            # state = IntentCommand(90.0, 'reply', args={'msg': stripped_msg, 'qq': qq})
            reply_dict = reply(stripped_msg, qq)
            if reply_dict['code'] != -1:
                await session.send(reply_dict['msg'])

    if session.ctx['message_type'] == 'group':
        if session.ctx['to_me'] == True:
            stripped_msg = stripped_msg
            # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
            # return IntentCommand(90.0, 'wz_bizhi', args={'hero_name': stripped_msg})

        # if '壁纸' in stripped_msg:
        #     user_id = session.ctx['user_id']
        #     reply_str = "[CQ:at,qq={}] Hi~ 如果你要壁纸请长按我头像@我英雄名字或皮肤的某个关键字哦~".format(user_id)
        #     await session.send(reply_str)

        if '壁纸' in stripped_msg:
            stripped_msg = stripped_msg.replace('壁纸', '')
            if stripped_msg:
                results = SQL().select_wz_wall(stripped_msg)
                if len(results) != 0:
                    result = '找到了{}张({})的壁纸:\n\n'.format(len(results), stripped_msg)
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
                        await session.send('该关键字信息量太大了，请换个详细点的关键字吧')
                    else:
                        t = ruturn_tip('bz')
                        rep_str = '{}||{}'.format(result, t.format(results[0][3], results[0][3])).replace('|', '\n')
                        await session.send(rep_str.strip())
                # else:
                #     # return "没有找到({})的壁纸，请确认名字输入正确哦~".format(name) + end_str
                #     pass
        elif '菜单' in stripped_msg:
            strs1 = SQL().select_var_info('WZ_GROUP_MENU')
            strs1 = strs1.replace('|', '\n')
            await session.send(strs1.strip())
        elif '胜率' in stripped_msg:
            results = SQL().select_wz_win_rate(stripped_msg)
            if results:
                t = ruturn_tip('sl')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '技能' in stripped_msg:
            results = SQL().select_wz_skill(stripped_msg)
            if results:
                t = ruturn_tip('jn')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '出装' in stripped_msg:
            results = SQL().select_wz_equip(stripped_msg)
            if results:
                t = ruturn_tip('cz')
                rep_str = '{}{}||{}'.format(results[0][0], results[0][1], t.format(results[0][2], results[0][2])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '铭文' in stripped_msg:
            results = SQL().select_wz_rune(stripped_msg)
            if results:
                t = ruturn_tip('mw')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '克制' in stripped_msg:
            results = SQL().select_wz_kz(stripped_msg)
            if results:
                t = ruturn_tip('kz')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '介绍' in stripped_msg:
            results = SQL().select_wz_introduce(stripped_msg)
            if results:
                t = ruturn_tip('js')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '组合' in stripped_msg:
            results = SQL().select_wz_zh(stripped_msg)
            if results:
                t = ruturn_tip('zh')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        elif '技巧' in stripped_msg:
            results = SQL().select_wz_jq(stripped_msg)
            if results:
                t = ruturn_tip('jq')
                rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
                await session.send(rep_str.strip())
        else:
            pass


        # if '音乐' in stripped_msg:
        #     # user_id = session.ctx['user_id']
        #     reply_str = "[CQ:music,type=qq,id=4758512]"
        #     # 向用户发送天气预报
        #     await session.send(reply_str)


        # if '演示' == stripped_msg:
        #     reply_str = "[CQ:at,qq={}] 李信".format(session.bot.config.BOT_QQ)
        #     # 向用户发送天气预报
        #     await session.send(reply_str)
        #     time.sleep(0.3)
        #     return IntentCommand(90.0, 'wz_bizhi', args={'hero_name': '李信'})

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.ctx['group_id'] == session.bot.config.WZ_GROUP_ID:
        user_id = session.ctx['user_id']
        # reply_str = r"[CQ:at,qq={}] 欢迎新朋友~|群里有全英雄高清无水印壁纸，需要请长按我头像@我英雄名字或皮肤的某个关键字获取哦~|发送“演示”可查看获取教程".format(user_id)
        reply_str = r"[CQ:at,qq={}] 欢迎新朋友~||需要壁纸请直接发送“英雄名+壁纸”获取哦（如：赵云壁纸）||若还需要查询某英雄胜率、出装、铭文、组合、介绍、克制、技能等功能，可以发送“英雄名字+关键字”查看哦（如：李白铭文、李白出装）".format(user_id)
        reply_str = reply_str.replace('|', '\n')
        # 发送欢迎消息
        await session.send(reply_str)

# 将函数注册为好友请求处理器
@on_request('friend')
async def _(session: RequestSession):
    # 自动同意
    await session.approve()
#
# @on_notice('friend_add')
# async def _(session: NoticeSession):
#     user_id = session.ctx['user_id']
#     print(user_id)
#     # 发送消息
#     await session.send('你好啊1~')