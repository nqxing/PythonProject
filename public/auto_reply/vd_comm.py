from auto_reply.package.key_info_get import return_keyInfo
from auto_reply.package.card_remind import card_open
from auto_reply.package.ele_sign_base import eleme_sign_open
from auto_reply.package import *

def vd_comm(action_dict, eleme_sign_dict, url_sc_dict, fromUser, text, state):
    END_STR = pubVarList.objects.filter(var_name='END_STR')[0].var_info.replace('|', '\n')
    r = {'code': 0, 'msg': ''}
    if text == '001' or text == '王者荣耀皮肤壁纸' or text == '王者荣耀壁纸' or text == '王者壁纸':
        action_dict[fromUser] = 'wzry_bz'
        rs = '获取王者荣耀壁纸：\n\n请在5分钟内回复你要的英雄名字或皮肤关键字哦~ 需要全英雄请回复all'+END_STR
        r['msg'] = rs
        return r
    elif text == '002'or text == '王者荣耀语音包' or text == '王者语音包':
        action_dict[fromUser] = 'wzry_yy'
        rs = '获取王者荣耀英雄皮肤语音包：\n\n请在5分钟内回复你要的英雄名字哦~ 需要其它非英雄语音请回复oth'+END_STR
        r['msg'] = rs
        return r
    elif text == '003' or text == '英雄联盟皮肤壁纸' or text == '英雄联盟壁纸' or text == '联盟壁纸' or text == 'LOL壁纸'or text == 'lol壁纸':
        action_dict[fromUser] = 'yxlm_bz'
        rs = '获取英雄联盟壁纸：\n\n请在5分钟内回复你要的英雄名字或皮肤关键字哦~ 需要全英雄请回复all'+END_STR
        r['msg'] = rs
        return r
    elif text == '004' or text == '饿了么红包':
        rs = pubVarList.objects.filter(var_name="ELE_AD")[0].var_info.replace('|', '\n')
        r['code'] = 1
        r['msg'] = rs
        return r

    # 20201016关闭该功能
    # elif text == '005' or text == '饿了么签到':
    #     action_dict[fromUser] = 'eleme_sign'
    #     vs = eleme_sign_open(fromUser)
    #     rs = '饿了么自动签到：\n\n'+vs+END_STR
    #     eleme_sign_dict[fromUser] = 'mobile'
    #     # rs = '饿了么自动签到：\n请在5分钟内回复以下数字进行操作\n\n回复1：开启饿了么自动签到\n回复2：添加(修改)签到手机号\n回复3：关闭饿了么自动签到\n回复4：删除并关闭饿了么签到\n回复5：绑定微信/QQ发送签到结果'+END_STR
    #     r['msg'] = rs
    #     return r
    # elif text == '006':
    #     rs = '<a href="https://mp.weixin.qq.com/s/sRoXiWti9yZtlEy2d9LOfQ">饿了么红包监控</a>'
    #     r['code'] = 1
    #     r['msg'] = rs
    #     return r

    # 20201016关闭该功能
    # elif text == '007' or text == '打卡提醒':
    #     action_dict[fromUser] = 'card_tx'
    #     vs = card_open(fromUser)
    #     rs = '上下班打卡提醒：\n\n'+vs+END_STR
    #     # rs = '<a href="https://mp.weixin.qq.com/s/RAWreKGC4fwkK5wsD_sWPg">上班忘记打卡？别担心，人工智能提醒你记得打卡</a>'
    #     # r['code'] = 1
    #     r['msg'] = rs
    #     return r

    # 20201016关闭该功能
    # elif text == '008' or text == '短网址':
    #     action_dict[fromUser] = 'url_sc'
    #     url_sc_dict[fromUser] = ''
    #     rs = '生成短网址或二维码：\n请在5分钟内回复以下数字进行操作\n\n回复1：永久url.cn短网址生成\n回复2：永久t.cn短网址生成\n回复3：链接或内容转二维码'+END_STR
    #     r['msg'] = rs
    #     return r
    elif text == '009' or text == '去水印':
        action_dict[fromUser] = 'video_shuiy'
        rs = '一键去除短视频水印：\n\n请在5分钟内回复你要去除水印的视频链接~\n<a href="https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt6ds3uibdck4zsEwG8iaXmmIjRsic8NXR3icAOM5yib5TWb76qqlylfo3ekRTxxgF3mUhDicnOEQxTd1Siaw/0?wx_fmt=png">点击此处</a>' \
             '查看支持的视频网站'+END_STR
        r['msg'] = rs
        return r
    elif text == '010' or text == '证件照':
        action_dict[fromUser] = 'remove_bg'
        rs = '一键生成红蓝白底证件照：\n\n请在5分钟内回复你要生成的照片哦~\n<a href="https://mp.weixin.qq.com/s/6QBwt2IoFODi-sWA115eYA">点击此处</a>' \
             '查看生成示例'+END_STR
        r['msg'] = rs
        return r
    elif text == '011' or text == '垃圾分类':
        action_dict[fromUser] = 'garbage_cx'
        rs = '垃圾分类查询：\n\n请在5分钟内回复你要查询的垃圾名字'+END_STR
        r['msg'] = rs
        return r
    elif text == '012'  or '红包群' in text:
        r['code'] = 3
        r['msg'] = "njHpjMQsdYbNZkFSToEkBhnAGIxO9HuVkZI--1ytaHY"
        return r
    elif text == '013' or text == '小编微信':
        rs = '<a href="https://mp.weixin.qq.com/s/drufLcC-t9sGl7WNA_-0LA">我的微信</a>'
        r['code'] = 1
        r['msg'] = rs
        return r
    elif text == '机器人':
        # code = 2 为回复图文信息
        # code = 3 为回复图片，msg为media_id
        r['code'] = 3
        r['msg'] = "njHpjMQsdYbNZkFSToEkBvCzrCV1XfCAVn5MNMeByR4"
        return r
    elif text == '指令' or text == '菜单' or text == '帮助':
        rs = 'Hi~ 下面是我目前支持的功能，需要什么就回复对应指令哈！如：001\n\n'+pubVarList.objects.filter(var_name='ZHILING')[0].var_info.replace('|', '\n')
        r['code'] = 1
        r['msg'] = rs
        return r
    elif '壁纸' in text or '王者' in text or '联盟' in text or 'lol' in text:
        rs = 'Hi~ 您是不是在找壁纸呢？需要哪个游戏的壁纸就回复哪个指令哈！如：001\n\n'+pubVarList.objects.filter(var_name='ZHILING')[0].var_info.replace('|', '\n')
        r['code'] = -1
        r['msg'] = rs
        return r
    else:
        if state:
            key_state = return_keyInfo(text)
            if key_state == 0:
                rs = pubVarList.objects.filter(var_name="NO_STR")[0].var_info.replace('|', '\n')
                r['code'] = -1
                r['msg'] = rs
                return r
            else:
                key_state = key_state.replace('|', '\n')
                r['code'] = -1
                r['msg'] = key_state
                return r
        else:
            r['code'] = -2
            return r