from auto_reply.package.ele_sign_base import *
from robot.models import pubEleSignCode
from auto_reply.package.ele_sign_login import captcha_yz, get_captcha

def ele_sign_reply(eleme_sign_dict, eleme_sign_cap_dict, eleme_sign_cap_dict_api, fromUser, content, END_STR, state):
    '''
    :param eleme_sign_dict:
    :param eleme_sign_cap_dict:
    :param eleme_sign_cap_dict_api:
    :param fromUser:
    :param content:
    :param END_STR:
    :param state: 为True是在公众号验证，否则是调用api验证的
    :return:
    '''
    HOST_URL = pubVarList.objects.filter(var_name='HOST_URL')[0].var_info
    if eleme_sign_dict[fromUser] == 'mobile':
        result = eleme_sign_verify_mobile(fromUser, content)
        if result['status'] == 0:
            reply_content = result['message'] + END_STR
            if state:
                eleme_sign_dict[fromUser] = 'codenum'
        elif result['status'] == 1:
            if state:
                message = '账户存在风险，需要图形验证码，请点击下方链接查看验证码并回复：\n\n' \
                          '<a href="{}">点击查看验证码</a>'.format(ELE_CAPTCHA_URL.format(HOST_URL, fromUser))
                eleme_sign_dict[fromUser] = 'captcha'
            else:
                url = short_url(ELE_CAPTCHA_URL.format(HOST_URL, fromUser))
                if url == -1:
                    url = ELE_CAPTCHA_URL.format(HOST_URL, fromUser)
                elif url == "生成短网址错误，确认网址正确":
                    url = ELE_CAPTCHA_URL.format(HOST_URL, fromUser)
                else:
                    url = url
                message = '账户存在风险，需要图形验证码，请点击下方链接查看验证码并回复：\n\n' \
                          '{}'.format(url)
            cap_list = [content, result['message']]
            if eleme_sign_cap_dict != None:
                eleme_sign_cap_dict[fromUser] = cap_list
            # 该变量使用于接口调用时读取数据
            if eleme_sign_cap_dict_api != None:
                eleme_sign_cap_dict_api[fromUser] = cap_list
            reply_content = message + END_STR
        elif result['status'] == 3:
            reply_content = result['message']
            if state:
                eleme_sign_dict[fromUser] = ''
        else:
            if '滑动验证码' in result['message']:
                # if get_chromes() > 5:
                #     reply_content = '账户存在风险，需要滑动验证码，因后台验证人数过多，请过会再发送手机号进行验证' + END_STR
                # else:
                if state:
                    reply_content = '账户存在风险，需要滑动验证码，系统正在后台为您验证，大概需要30秒，请在收到验证码后5分钟内进行回复，点击下方链接可实时查看验证结果' \
                                    '\n\n<a href="{}">点击查看验证结果</a>'.format(
                        ELE_SIGN_URL.format(HOST_URL, fromUser)) + END_STR
                    eleme_sign_verify_mobile_hd_index(eleme_sign_dict, fromUser, content, True)
                    eleme_sign_dict[fromUser] = 'codenum_hd'
                else:
                    url = short_url(ELE_SIGN_URL.format(HOST_URL, fromUser))
                    if url == -1:
                        url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                    elif url == "生成短网址错误，确认网址正确":
                        url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                    else:
                        url = url
                    reply_content = '账户存在风险，需要滑动验证码，系统正在后台为您验证，大概需要30秒，请在收到验证码后5分钟内进行回复，点击下方链接可实时查看验证结果' \
                                    '\n\n{}'.format(url) + END_STR
                    eleme_sign_verify_mobile_hd_index(eleme_sign_dict, fromUser, content, False)
            else:
                reply_content = result['message'] + END_STR
    elif eleme_sign_dict[fromUser] == 'captcha':
        if eleme_sign_cap_dict != None:
            result = captcha_yz(eleme_sign_cap_dict[fromUser][0], eleme_sign_cap_dict[fromUser][1], content, fromUser)
        else:
            result = captcha_yz(eleme_sign_cap_dict_api[fromUser][0], eleme_sign_cap_dict_api[fromUser][1], content, fromUser)
        if result['status'] == 0:
            reply_content = result['message'] + END_STR
            if state:
                eleme_sign_dict[fromUser] = 'codenum'
                value = eleme_sign_cap_dict.pop(fromUser)
                write_log(1, '字典 eleme_sign_cap_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value,
                                                                                              len(eleme_sign_cap_dict)))
        elif result['status'] == 1:
            if eleme_sign_cap_dict != None:
                result1 = get_captcha(fromUser, eleme_sign_cap_dict[fromUser][0])
            else:
                result1 = get_captcha(fromUser, eleme_sign_cap_dict_api[fromUser][0])
            if result1['status'] == 0:
                if state:
                    message = '{}，请重新点击下方链接查看验证码并回复：\n\n' \
                              '<a href="{}">点击查看验证码</a>'.format(result['message'],
                                                                    ELE_CAPTCHA_URL.format(HOST_URL, fromUser))
                else:
                    url = short_url(ELE_CAPTCHA_URL.format(HOST_URL, fromUser))
                    if url == -1:
                        url = ELE_CAPTCHA_URL.format(HOST_URL, fromUser)
                    elif url == "生成短网址错误，确认网址正确":
                        url = ELE_CAPTCHA_URL.format(HOST_URL, fromUser)
                    else:
                        url = url
                    message = '{}，请重新点击下方链接查看验证码并回复：\n\n' \
                              '{}'.format(result['message'], url)
                if eleme_sign_cap_dict != None:
                    cap_list = [eleme_sign_cap_dict[fromUser][0], result1['message']]
                    eleme_sign_cap_dict[fromUser] = cap_list
                # 该变量使用于接口调用时读取数据
                if eleme_sign_cap_dict_api != None:
                    cap_list = [eleme_sign_cap_dict_api[fromUser][0], result1['message']]
                    eleme_sign_cap_dict_api[fromUser] = cap_list
                reply_content = message + END_STR
            else:
                message = '{}：\n\n{}'.format(result['message'], result1['status'])
                if state:
                    eleme_sign_dict[fromUser] = 'mobile'
                reply_content = message + END_STR
        else:
            if state:
                eleme_sign_dict[fromUser] = 'mobile'
            reply_content = result['message'] + END_STR
    elif eleme_sign_dict[fromUser] == 'codenum':
        result = eleme_sign_verify_code(fromUser, content)
        if result['status'] == 0:
            # 异步执行签到 传False为查单人openId
            send_sign_index(fromUser, False)
            if state:
                reply_content = '恭喜你，手机号绑定成功，饿了么自动签到设置成功，系统会在每天上午9-10点自动为你签到，点击下方链接查看今日签到结果' \
                                '\n\n<a href="{}">点击查看签到结果</a>\n\n每天的签到结果都会写入到上面的链接中，建议收藏该链接方便查看哦，若您希望每天的签到结果通过微信/QQ发送给你，请回复数字“1”'.format(
                    ELE_SIGN_URL.format(HOST_URL, fromUser)) + END_STR
            else:
                url = short_url(ELE_SIGN_URL.format(HOST_URL, fromUser))
                if url == -1:
                    url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                elif url == "生成短网址错误，确认网址正确":
                    url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                else:
                    url = url
                reply_content = '恭喜你，手机号绑定成功，饿了么自动签到设置成功，系统会在每天上午9-10点自动为你签到，点击下方链接查看今日签到结果' \
                                '\n\n{}'.format(url) + END_STR
            value = eleme_sign_dict.pop(fromUser)
            write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value,
                                                                                          len(eleme_sign_dict)))
            write_log(1, '{} 开启了饿了么自动签到并完成了手机号绑定'.format(fromUser))
        elif result['status'] == 1:
            reply_content = result['message'] + END_STR
            if state:
                eleme_sign_dict[fromUser] = 'mobile'
        else:
            reply_content = result['message'] + END_STR
    elif eleme_sign_dict[fromUser] == 'codenum_hd':
        values = pubEleSignCode.objects.filter(wx_open_id=fromUser)
        value = values[0]
        if value.is_send:
            if len(content) == 6 and content.isdigit():
                value.sms_code = content
                value.save()
                if state:
                    reply_content = '恭喜你，验证码接收成功，系统正在后台为您验证，大概需要5秒，验证成功后系统会在每天上午9-10点自动为你签到，点击下方链接可实时查看验证和签到结果' \
                                    '\n\n<a href="{}">点击查看签到结果</a>\n\n每天的签到结果都会写入到上面的链接中，建议收藏该链接方便查看哦，若您希望每天的签到结果通过微信/QQ发送给你，请回复数字“1”'.format(
                        ELE_SIGN_URL.format(HOST_URL, fromUser)) + END_STR
                else:
                    url = short_url(ELE_SIGN_URL.format(HOST_URL, fromUser))
                    if url == -1:
                        url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                    elif url == "生成短网址错误，确认网址正确":
                        url = ELE_SIGN_URL.format(HOST_URL, fromUser)
                    else:
                        url = url
                    reply_content = '恭喜你，验证码接收成功，系统正在后台为您验证，大概需要5秒，验证成功后系统会在每天上午9-10点自动为你签到，点击下方链接可实时查看验证和签到结果' \
                                    '\n\n{}'.format(url) + END_STR
                value = eleme_sign_dict.pop(fromUser)
                write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value,
                                                                                              len(eleme_sign_dict)))
            else:
                reply_content = "输入错误，验证码为6位数字哦，请重新发送" + END_STR
        else:
            reply_content = "验证码还未发送，请稍等" + END_STR
    else:
        reply_content = '指令无效' + END_STR
    return reply_content