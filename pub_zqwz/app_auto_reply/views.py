from django.http import HttpResponse
from auto_reply.package.ele_sign_base import *
from auto_reply.package.ident_photo import remove_bg_index
from auto_reply.package.ident_photo_load import copy_imgFile
from auto_reply.vd_comm import vd_comm
from auto_reply.reply_con_xml import reply_con_xml, del_action_dict


def auto_reply(request):
    try:
        if request.method == 'GET':
            my_signature = request.GET.get('signature', '')  # 获取携带 signature微信加密签名的参数
            my_timestamp = request.GET.get('timestamp', '')  # 获取携带随机数timestamp的参
            my_nonce = request.GET.get('nonce', '')  # 获取携带时间戳nonce的参数
            my_echostr = request.GET.get('echostr', '')  # 获取携带随机字符串echostr的参数
            token = 'nqxing'
            # 这里输入你要在微信公众号里面填的token，保持一致
            data = [token, my_timestamp, my_nonce]
            data.sort()
            # 进行字典排序
            temp = ''.join(data)
            # 拼接成字符串
            mysignature = hashlib.sha1(temp.encode('utf-8')).hexdigest()
            # # 判断请求来源，将三个参数字符串拼接成一个字符串进行sha1加密,记得转换为utf-8格式
            if my_signature == mysignature:
                # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
                return HttpResponse(my_echostr)
            else:
                return HttpResponse('')
        elif request.method == 'POST':
            # 下面这里是对请求解析，返回图灵机器人的回复
            xml = et.fromstring(request.body)
            # 获取用户发送的原始数据
            # fromstring()就是解析xml的函数，然后通过标签进行find()，即可得到标记内的内容。
            fromUser = xml.find('FromUserName').text
            toUser = xml.find('ToUserName').text
            msgType = xml.find("MsgType").text
            if msgType == 'text':
                content = xml.find('Content').text.strip()
                rep_state = vd_comm(action_dict, eleme_sign_dict, url_sc_dict, fromUser, content, True)
                if rep_state['code'] == 0:
                    rep_content = rep_state['msg']
                    del_action_dict(action_dict, eleme_sign_dict, eleme_sign_cap_dict, url_sc_dict, fromUser)
                elif rep_state['code'] == 2:
                    news_str = KEY_NEWS_BOT.format(fromUser, toUser, int(time.time()))
                    r = HttpResponse(news_str)
                    return r
                elif rep_state['code'] == 3:
                    media_id = rep_state['msg']
                    news_str = XML_IMGAGE.format(fromUser, toUser, int(time.time()), media_id)
                    r = HttpResponse(news_str)
                    return r
                else:
                    rep_content = rep_state['msg']
                r = HttpResponse(XML_TEXT.format(fromUser, toUser, int(time.time()), rep_content))
                return r
            elif msgType == 'image':
                    return HttpResponse('')
            elif msgType == 'event':
                event = xml.find('Event').text
                if event == 'subscribe':
                    rep_content = pubVarList.objects.filter(var_name='FO_MSG')[0].var_info.replace('|', '\n')
                    r = HttpResponse(XML_TEXT.format(fromUser, toUser, int(time.time()), rep_content))                # 微信公众号做出响应，自动回复的格式如上
                    # 定义回复的类型为xml
                    return r
                else:
                    return HttpResponse('')
            else:
                return HttpResponse('')
        else:
            return HttpResponse('')
    except:
        write_log(3, format(traceback.format_exc()))
        # send_fqq('微信公众号后台出错了，快去看看吧')
        fangtang('微信公众号后台出错了，快去看看吧', '微信公众号后台出错了，快去看看吧')
        return HttpResponse('系统异常，请稍后再来看看吧')
