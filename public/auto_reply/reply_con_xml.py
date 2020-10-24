from auto_reply.package.wz_wall_get import return_wzSkin
from auto_reply.package.wz_voice_get import return_wzYy
from auto_reply.package.lol_wall_get import return_lmSkin
from auto_reply.package.ele_sign_base import *
from auto_reply.reply.ele_sign import ele_sign_reply
from auto_reply.package.card_remind import card_set_time
from django.http import HttpResponse
from auto_reply.vd_comm import vd_comm
from auto_reply.package import *

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName(args[-1])
        thr.start()
    return wrapper

@asyncs
def del_action_dict(action_dict, eleme_sign_dict, eleme_sign_cap_dict, url_sc_dict, fromUser):
    write_log(1, '字典 action_dict 新增了 key：[{}] 动作为[{}] 当前共有{}个人在进行指令操作'.format(fromUser, action_dict[fromUser], len(action_dict)))
    time.sleep(300)
    value = action_dict.pop(fromUser)
    write_log(1, '字典 action_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value, len(action_dict)))
    if fromUser in eleme_sign_dict:
        value = eleme_sign_dict.pop(fromUser)
        write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value, len(action_dict)))
    if fromUser in eleme_sign_cap_dict:
        value = eleme_sign_cap_dict.pop(fromUser)
        write_log(1, '字典 eleme_sign_cap_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value, len(action_dict)))
    if fromUser in url_sc_dict:
        value = url_sc_dict.pop(fromUser)
        write_log(1, '字典 url_sc_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value, len(action_dict)))

def stop_thd(fromUser):
    # print('当前: ', threading.enumerate()) #返回一个包含正在运行的线程的list
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if fromUser in lists[i].name:
            _async_raise(lists[i].ident, SystemExit)
            write_log(1, '用户 [{}] 又发送另一指令提前终止了进程名 [{}]'.format(fromUser, fromUser))

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def reply_con_xml(action_dict, eleme_sign_dict, eleme_sign_cap_dict, url_sc_dict, content, fromUser, toUser, funName):
    rep_state = vd_comm(action_dict, eleme_sign_dict, url_sc_dict, fromUser, content, False)
    END_STR = pubVarList.objects.filter(var_name='END_STR')[0].var_info.replace('|', '\n')
    if rep_state['code'] == 0:
        stop_thd(fromUser)
        reply_content = rep_state['msg']
        del_action_dict(action_dict, eleme_sign_dict, eleme_sign_cap_dict, url_sc_dict, fromUser)
    elif rep_state['code'] == 1:
        reply_content = rep_state['msg']
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
        if funName == 'wzbz':
            reply_content = return_wzSkin(content)+END_STR
        elif funName == 'wzyy':
            reply_content = return_wzYy(content)+END_STR
        elif funName == 'urlSC':
            if content == '3':
                reply_content = "生成二维码，请在5分钟内回复你要生成的内容或网址链接（若是网址请一定记得加http://或https://哦）"+END_STR
                url_sc_dict[fromUser] = 'QrCode'
            elif content == '1':
                reply_content = '生成QQ短网址，请在5分钟内回复你要生成的网址链接（请一定记得以http://或https://开头哦）'+END_STR
                url_sc_dict[fromUser] = 'UrlCN'
            elif content == '2':
                reply_content = '生成新浪短网址，请在5分钟内回复你要生成的网址链接（请一定记得以http://或https://开头哦）'+END_STR
                url_sc_dict[fromUser] = 'tCN'
            else:
                if url_sc_dict[fromUser] == 'QrCode':
                    times = int(time.time())
                    value = qr_url(content, times)
                    if value:
                        HOST_URL = pubVarList.objects.filter(var_name='HOST_URL')[0].var_info
                        reply_content = '二维码生成成功！<a href="{}">点击此处保存</a>'.format(QR_IMG_URL.format(HOST_URL, times))+END_STR
                    else:
                        reply_content = '二维码生成失败，请稍后重试'+END_STR
                elif url_sc_dict[fromUser] == 'UrlCN':
                    value = short_url(content)
                    if value == -1:
                        reply_content = '生成失败，请稍后重试'+END_STR
                    else:
                        reply_content = "生成成功！{}".format(value)+END_STR
                elif url_sc_dict[fromUser] == 'tCN':
                    value = short_turl(content)
                    if value == -1:
                        reply_content = '生成失败，请稍后重试'
                    else:
                        reply_content = "生成成功！{}".format(value)+END_STR
                else:
                    reply_content = '请回复以上数字哦'+END_STR
        elif funName == 'elemeSign':
            if content == '1':
                reply_content = get_bind_name(fromUser, 2)
            elif content == '2':
                reply_content = eleme_sign_close(fromUser)+END_STR
            elif content == '3':
                reply_content = eleme_sign_del_close(fromUser)+END_STR
            else:
                reply_content = ele_sign_reply(eleme_sign_dict, eleme_sign_cap_dict, None, fromUser, content, END_STR, True)
        elif funName == 'removebgImg':
            reply_content = content+END_STR
        elif funName == 'removebgText':
            reply_content = '请回复你要生成的证件照图片或指令关键字哦~'+END_STR
        elif funName == 'videoShuiy':
            result = del_video_shuiy(content)
            if result['status'] == 0:
                value = short_url(result['message'])
                if value != -1:
                    url = value
                else:
                    url = result['message']
                reply_content = '水印去除成功，请复制以下链接在浏览器中打开查看或下载~\n\n{}'.format(url)+END_STR
            else:
                reply_content = result['message']+END_STR
        elif funName == 'garbageCx':
            result = get_garbage_name(content)
            reply_content = result['message']+END_STR
        elif funName == 'cardTx':
            result = card_set_time(content, fromUser)
            if "恭喜你" in result:
                reply_content = result
            else:
                reply_content = result + END_STR
        else:
            reply_content = return_lmSkin(content)+END_STR
    r = HttpResponse(XML_TEXT.format(fromUser, toUser, int(time.time()), reply_content))
    return r