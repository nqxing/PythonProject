from config.fun_api import *

def eleme_sign_base(eleme_sign_dict, beizhu, text, msg):
    if eleme_sign_dict[beizhu[0]] == 'mobile':
        try:
            fromUser = SQL().select_bind_is_users(beizhu[0])[0][0]
            result = requests.get(ELE_SIGN_MOBILE_HOST.format(fromUser, text)).text
            if "账户存在风险，需要图形验证码" in result:
                eleme_sign_dict[beizhu[0]] = 'captcha'
            if "账户存在风险，需要滑动验证码" in result:
                eleme_sign_dict[beizhu[0]] = 'codenum_hd'
            if "验证码发送成功" in result:
                eleme_sign_dict[beizhu[0]] = 'codenum'
            msg.reply(result)
        except:
            eleme_sign_dict[beizhu[0]] = 'mobile'
            write_log(3, traceback.format_exc())
            msg.reply("系统异常，请发送手机号重试")
    elif eleme_sign_dict[beizhu[0]] == 'captcha':
        try:
            fromUser = SQL().select_bind_is_users(beizhu[0])[0][0]
            result = requests.get(ELE_SIGN_CAPTCHA_HOST.format(fromUser, text)).text
            if "验证码验证失败，请重新发送手机号绑定" in result:
                eleme_sign_dict[beizhu[0]] = 'mobile'
            if "验证码发送成功" in result:
                eleme_sign_dict[beizhu[0]] = 'codenum'
            msg.reply(result)
        except:
            eleme_sign_dict[beizhu[0]] = 'mobile'
            write_log(3, traceback.format_exc())
            msg.reply("系统异常，请发送手机号重试")
    elif eleme_sign_dict[beizhu[0]] == 'codenum':
        try:
            fromUser = SQL().select_bind_is_users(beizhu[0])[0][0]
            result = requests.get(ELE_SIGN_CODENUM_HOST.format(fromUser, text)).text
            if "验证失效了，请重新发送手机号" in result:
                eleme_sign_dict[beizhu[0]] = 'mobile'
            if "恭喜你，手机号绑定成功" in result:
                value = eleme_sign_dict.pop(beizhu[0])
            msg.reply(result)
        except:
            eleme_sign_dict[beizhu[0]] = 'mobile'
            write_log(3, traceback.format_exc())
            msg.reply("系统异常，请发送手机号重试")
    elif eleme_sign_dict[beizhu[0]] == 'codenum_hd':
        try:
            fromUser = SQL().select_bind_is_users(beizhu[0])[0][0]
            result = requests.get(ELE_SIGN_CODENUM_HD_HOST.format(fromUser, text)).text
            msg.reply(result)
        except:
            eleme_sign_dict[beizhu[0]] = 'mobile'
            write_log(3, traceback.format_exc())
            msg.reply("系统异常，请发送手机号重试")

def eleme_sign_open(eleme_sign_dict, beizhu, msg):
    if "vip_" in beizhu[0]:
        values = SQL().select_sign_users(beizhu[0])
        if values and values[0][0] != None and values[0][1] != None:
            values = SQL().select_sign_open1(beizhu[0])
            mobile_str = values[0][1]
            state_str = values[0][0]
            if state_str == True and mobile_str == None:
                eleme_sign_dict[beizhu[0]] = 'mobile'
                msg.reply('您已开启饿了么自动签到，但还未绑定手机号，现在回复手机号绑定吧')
            elif state_str == False and mobile_str == None:
                SQL().up_sign_open1(beizhu[0])
                eleme_sign_dict[beizhu[0]] = 'mobile'
                msg.reply('您的饿了么自动签到开启成功，但还未绑定手机号，现在回复手机号绑定吧')
            elif state_str == False and mobile_str != None:
                SQL().up_sign_open1(beizhu[0])
                msg.reply('您的饿了么自动签到开启成功，当前绑定的手机号为（{}），如需更改请发送关键字“修改手机号”哦'.format(mobile_str))
            else:
                msg.reply('您已开启饿了么自动签到，无需再次开启，若您要关闭饿了么自动签到请发送“关闭饿了么签到”')
        else:
            msg.sender.send_image('public.jpg')
            msg.reply(
                '您未开启饿了么签到或未与公众号绑定，无法直接开启\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
    else:
        msg.sender.send_image('public.jpg')
        msg.reply('您未开启饿了么签到或未与公众号绑定，无法直接开启\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')

def eleme_sign_close(beizhu, msg):
    if "vip_" in beizhu[0]:
        values = SQL().select_sign_users(beizhu[0])
        if values and values[0][0] != None and values[0][1] != None:
            state_str = SQL().select_sign_open1(beizhu[0])[0][0]
            if state_str == True:
                SQL().up_sign_open2(beizhu[0])
                msg.reply('您的饿了么自动签到已关闭，发送“开启饿了么签到”可再次开启哦')
            elif state_str == False:
                msg.reply('您的饿了么自动签到已是关闭状态，无需重复关闭')
        else:
            msg.sender.send_image('public.jpg')
            msg.reply('您未开启饿了么签到或未与公众号绑定，无法直接关闭\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
    else:
        msg.sender.send_image('public.jpg')
        msg.reply('您未开启饿了么签到或未与公众号绑定，无法直接关闭\n请长按识别图中二维码，关注公众号(最趣分享)后发送关键字“饿了么签到”进行开通或绑定\n\n点击查看绑定教程：https://url.cn/5VXTApU')
