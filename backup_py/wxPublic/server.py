# -*- coding: utf-8 -*-
from package import *
from package.wzry.get_wz_bizhi import return_wzSkin
from package.wzry.get_wz_yy import return_wzYy
from package.yxlm.get_lm_bizhi import return_lmSkin
from package.eleme.sign.sign_run import send_sign_index
from package.eleme.sign.sign_base import *
from package.eleme.sign.sign_login import captcha_yz,get_captcha
from package.removebk.remove_bg import remove_bg_index
from package.removebk.copy_img import copy_imgFile
from package.keywords.get_key_info import return_keyInfo
from flask_cors import *

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName(args[0])
        thr.start()
    return wrapper



action_dict = {}
eleme_sign_dict = {}
eleme_sign_cap_dict = {}

app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True)


@app.route('/autoReply/', methods=['GET', 'POST'])
# route() 装饰器用于把一个函数绑定到一个 URL
# 在微信公众号修改配置那里，如果你写的是“/wechat/”在括号里，就要在二级域名后面加上，不然就会出现token验证失败的一种情况！
def wxPublic():
    try:
        if request.method == 'GET':
            my_signature = request.args.get('signature', '')  # 获取携带 signature微信加密签名的参数
            my_timestamp = request.args.get('timestamp', '')  # 获取携带随机数timestamp的参
            my_nonce = request.args.get('nonce', '')  # 获取携带时间戳nonce的参数
            my_echostr = request.args.get('echostr', '')  # 获取携带随机字符串echostr的参数
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
                return make_response(my_echostr)
            else:
                return ''
        elif request.method == 'POST':
            # 下面这里是对请求解析，返回图灵机器人的回复
            xml = et.fromstring(request.data)
            # 获取用户发送的原始数据
            # fromstring()就是解析xml的函数，然后通过标签进行find()，即可得到标记内的内容。
            fromUser = xml.find('FromUserName').text
            toUser = xml.find('ToUserName').text
            msgType = xml.find("MsgType").text
            if msgType == 'text':
                if fromUser in action_dict:
                    content = xml.find('Content').text.strip()
                    # 获取向服务器发送的消息
                    # 返回数据包xml的文本回复格式
                    if action_dict[fromUser] == 'wzry_bz':
                        return reply_con_xml(content, fromUser, toUser, "wzbz")
                    if action_dict[fromUser] == 'wzry_yy':
                        return reply_con_xml(content, fromUser, toUser, "wzyy")
                    if action_dict[fromUser] == 'yxlm_bz':
                        return reply_con_xml(content, fromUser, toUser, "lmbz")
                    if action_dict[fromUser] == 'eleme_sign':
                        return reply_con_xml(content, fromUser, toUser, "elemeSign")
                    if action_dict[fromUser] == 'remove_bg':
                        return reply_con_xml(content, fromUser, toUser, "removebgText")
                    if action_dict[fromUser] == 'video_shuiy':
                        return reply_con_xml(content, fromUser, toUser, "videoShuiy")
                    if action_dict[fromUser] == 'garbage_cx':
                        return reply_con_xml(content, fromUser, toUser, "garbageCx")
                else:
                    content = xml.find('Content').text.strip()
                    rep_state = vd_comm(fromUser, content, True)
                    if rep_state['code'] == 0:
                        rep_content = rep_state['msg']
                        del_action_dict(fromUser)
                    elif rep_state['code'] == 2:
                        news_str = KEY_NEWS_BOT.format(fromUser, toUser, int(time.time()))
                        r = make_response(news_str)
                        r.content_type = 'application/xml'
                        return r
                    else:
                        rep_content = rep_state['msg']
                    r = make_response(XML_TEXT.format(fromUser, toUser, int(time.time()), rep_content))
                    r.content_type = 'application/xml'
                    return r
            elif msgType == 'image':
                if fromUser in action_dict:
                    if action_dict[fromUser] == 'remove_bg':
                        pic_url = xml.find('PicUrl').text.strip()
                        file_time = int(time.time())
                        file_names = ['{}_white.png'.format(file_time),'{}_blue.png'.format(file_time),'{}_red.png'.format(file_time)]
                        remove_bg_index(fromUser, pic_url, file_time, file_names)
                        if copy_imgFile(file_time, COPY_IMG_PATH.format("loading"), NEW_COPY_IMG_PATH):
                            content = '系统正在为您生成证件照...请稍等...\n\n白底：<a href="http://{}/wxPublic/image/{}">点击查看</a>\n\n' \
                                      '蓝底：<a href="http://{}/wxPublic/image/{}">点击查看</a>\n\n红底：<a href="http://{}/wxPublic/image/{}">点击查看</a>\n' \
                                      '----------\n注：图片状态实时更新，若点击图片还在生成中，请过会重新打开查看'.format(HOST_URL, file_names[0], HOST_URL, file_names[1], HOST_URL, file_names[2])
                            return reply_con_xml(content, fromUser, toUser, "removebgImg")
                        else:
                            content = '系统出错了，请稍后重试..'
                            send_fqq('生成证照动作复制初始图片出错了，快去看看吧')
                            return reply_con_xml(content, fromUser, toUser, "removebgImg")
                    else:
                        return ''
                else:
                    return ''
            elif msgType == 'event':
                event = xml.find('Event').text
                if event == 'subscribe':
                    rep_content = 'Hi~ 谢谢你的关注~\n\n希望我的存在能帮到你，需要什么可以回复告诉我哦，当然你也可以先发送下“菜单”让我介绍下自己哈！查看历史文章请点击右上角哦'
                    r = make_response(XML_TEXT.format(fromUser, toUser, int(time.time()), rep_content))                # 微信公众号做出响应，自动回复的格式如上
                    r.content_type = 'application/xml'
                    # 定义回复的类型为xml
                    return r
                else:
                    return ''
            else:
                return ''
        else:
            return ''
    except:
        write_log(3, '------- error -------\n{}---------------------'.format(traceback.format_exc()))
        send_fqq('微信公众号后台出错了，快去看看吧')

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

def stop_thd(fromUser):
    # print('当前: ', threading.enumerate()) #返回一个包含正在运行的线程的list
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if fromUser in lists[i].name:
            _async_raise(lists[i].ident, SystemExit)
            write_log(1, '用户 [{}] 又发送另一指令提前终止了进程名 [{}]'.format(fromUser, fromUser))

def reply_con_xml(content, fromUser, toUser, funName):
    rep_state = vd_comm(fromUser, content, False)
    if rep_state['code'] == 0:
        stop_thd(fromUser)
        reply_content = rep_state['msg']
        del_action_dict(fromUser)
    elif rep_state['code'] == 1:
        reply_content = rep_state['msg']
    elif rep_state['code'] == 2:
        news_str = KEY_NEWS_BOT.format(fromUser, toUser, int(time.time()))
        r = make_response(news_str)
        r.content_type = 'application/xml'
        return r
    else:
        if funName == 'wzbz':
            reply_content = return_wzSkin(WZ_PATH, content)
        elif funName == 'wzyy':
            reply_content = return_wzYy(WZ_PATH, content)
        elif funName == 'elemeSign':
            if content == '1':
                reply_content = eleme_sign_open(fromUser)
                eleme_sign_dict[fromUser] = 'mobile'
            elif content == '2':
                reply_content = '请在5分钟内回复您要重新绑定的手机号'
                eleme_sign_dict[fromUser] = 'mobile'
            elif content == '3':
                reply_content = eleme_sign_close(fromUser)
            elif content == '4':
                reply_content = '11'
            else:
                if eleme_sign_dict[fromUser] == 'mobile':
                    result = eleme_sign_verify_mobile(fromUser, content)
                    if result['status'] == 0:
                        reply_content = result['message']
                        eleme_sign_dict[fromUser] = 'codenum'
                    elif result['status'] == 1:
                        message = '账户存在风险，需要图形验证码，请点击下方链接查看验证码并回复：\n\n' \
                                  '<a href="http://{}/wxPublic/captcha/{}.jpg">点击查看验证码</a>'.format(HOST_URL, fromUser)
                        cap_list = [content, result['message']]
                        eleme_sign_cap_dict[fromUser] = cap_list
                        eleme_sign_dict[fromUser] = 'captcha'
                        reply_content = message
                    elif result['status'] == 3:
                        reply_content = result['message']
                        eleme_sign_dict[fromUser] = ''
                    else:
                        reply_content = result['message']
                elif eleme_sign_dict[fromUser] == 'captcha':
                    result = captcha_yz(eleme_sign_cap_dict[fromUser][0], eleme_sign_cap_dict[fromUser][1], content, fromUser)
                    if result['status'] == 0:
                        reply_content = result['message']
                        eleme_sign_dict[fromUser] = 'codenum'
                        value = eleme_sign_cap_dict.pop(fromUser)
                        write_log(1, '字典 eleme_sign_cap_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value,
                                                                                         len(eleme_sign_cap_dict)))
                    elif result['status'] == 1:
                        result1 = get_captcha(fromUser, eleme_sign_cap_dict[fromUser][0])
                        if result1['status'] == 0:
                            message = '{}，请重新点击下方链接查看验证码并回复：\n\n' \
                                      '<a href="http://{}/wxPublic/captcha/{}.jpg">点击查看验证码</a>'.format(result['message'], HOST_URL,
                                                                                                       fromUser)
                            cap_list = [eleme_sign_cap_dict[fromUser][0], result1['message']]
                            eleme_sign_cap_dict[fromUser] = cap_list
                            reply_content = message
                        else:
                            message = '{}：\n\n{}'.format(result['message'], result1['status'])
                            eleme_sign_dict[fromUser] = 'mobile'
                            reply_content = message
                    else:
                        eleme_sign_dict[fromUser] = 'mobile'
                        reply_content = result['message']
                elif eleme_sign_dict[fromUser] == 'codenum':
                    result = eleme_sign_verify_code(fromUser, content)
                    if result['status'] == 0:
                        # 异步执行签到 传False为查单人openId
                        send_sign_index(fromUser, False)
                        reply_content = '恭喜你，手机号绑定成功，饿了么自动签到设置成功，系统会在每天上午9-10点自动为你签到，点击下方链接查看今日签到结果' \
                                        '\n\n<a href="http://{}/wxPublic/sign/{}.txt">点击查看签到结果</a>\n------------\n注：每天的签到结果都会写入到上面的链接中，建议收藏该链接方便查看哦'
                        value = eleme_sign_dict.pop(fromUser)
                        write_log(1, '字典 eleme_sign_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value,
                                                                                         len(eleme_sign_dict)))
                        write_log(1, '{} 开启了饿了么自动签到并完成了手机号绑定'.format(fromUser))
                    elif result['status'] == 1:
                        reply_content = result['message']
                        eleme_sign_dict[fromUser] = 'mobile'
                    else:
                        reply_content = result['message']
                else:
                    reply_content = '请回复以上数字哦\n----------\n注：若要获取其他资源，请先发送“指令”切换哦'
        elif funName == 'removebgImg':
            reply_content = content
        elif funName == 'removebgText':
            reply_content = '请回复你要生成的证件照图片或指令关键字哦~'
        elif funName == 'videoShuiy':
            result = del_video_shuiy(content)
            if result['status'] == 0:
                value = short_url(result['message'])
                if value != -1:
                    url = value
                else:
                    url = result['message']
                reply_content = '水印去除成功，请复制以下链接在浏览器中打开查看或下载~\n\n{}'.format(url)
            else:
                reply_content = result['message']
        elif funName == 'garbageCx':
            result = get_garbage_name(content)
            reply_content = result['message']
        else:
            reply_content = return_lmSkin(LM_PATH, content)
    r = make_response(XML_TEXT.format(fromUser, toUser, int(time.time()), reply_content))
    # 微信公众号做出响应，自动回复的格式如上
    r.content_type = 'application/xml'
    # 定义回复的类型为xml
    return r

def vd_comm(fromUser, text, state):
    r = {'code': 0, 'msg': ''}
    end_str = '\n\n----------\n注：若要获取其他资源，请先发送“指令”切换哦'
    if text == '001':
        action_dict[fromUser] = 'wzry_bz'
        rs = '获取王者荣耀壁纸：\n\n请在5分钟内回复你要的英雄名字或皮肤关键字哦~ 需要全英雄请回复all'+end_str
        r['msg'] = rs
        return r
    elif text == '002':
        action_dict[fromUser] = 'wzry_yy'
        rs = '获取王者荣耀英雄皮肤语音包：\n\n请在5分钟内回复你要的英雄名字哦~ 需要其它非英雄语音请回复oth'+end_str
        r['msg'] = rs
        return r
    elif text == '003':
        action_dict[fromUser] = 'yxlm_bz'
        rs = '获取英雄联盟壁纸：\n\n请在5分钟内回复你要的英雄名字或皮肤关键字哦~ 需要全英雄请回复all'+end_str
        r['msg'] = rs
        return r
    elif text == '004':
        write_log(1, 'ceshi')
        action_dict[fromUser] = 'eleme_sign'
        eleme_sign_dict[fromUser] = ''
        rs = '饿了么自动签到：\n\n请在5分钟内回复以下数字进行操作\n回复1：开通饿了么签到\n回复2：修改你的签到手机号\n回复3：关闭饿了么自动签到\n回复4：删除并关闭饿了么签到'
        r['msg'] = rs
        return r
    elif text == '005':
        action_dict[fromUser] = 'video_shuiy'
        rs = '一键去除短视频水印：\n\n请在5分钟内回复你要去除水印的视频链接~ <a href="https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt6ds3uibdck4zsEwG8iaXmmIjRsic8NXR3icAOM5yib5TWb76qqlylfo3ekRTxxgF3mUhDicnOEQxTd1Siaw/0?wx_fmt=png">点击此处</a>' \
             '查看支持的视频网站'+end_str
        r['msg'] = rs
        return r
    elif text == '006':
        action_dict[fromUser] = 'remove_bg'
        rs = '一键生成红蓝白底证件照：\n\n请在5分钟内回复你要生成的照片哦~ <a href="https://mp.weixin.qq.com/s/6QBwt2IoFODi-sWA115eYA">点击此处</a>' \
             '查看生成示例'+end_str
        # r['code'] = 1
        r['msg'] = rs
        return r
    elif text == '007':
        action_dict[fromUser] = 'garbage_cx'
        rs = '垃圾分类查询：\n\n请在5分钟内回复你要查询的垃圾名字~ '+end_str
        r['msg'] = rs
        return r
    elif text == '008':
        rs = '<a href="https://mp.weixin.qq.com/s/RAWreKGC4fwkK5wsD_sWPg">上班忘记打卡？别担心，人工智能提醒你记得打卡</a>'
        r['code'] = 1
        r['msg'] = rs
        return r
    elif text == '009' or '饿了么' in text or '大包群' in text or '红包' in text:
        rs = '<a href="https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt4Tia88rrUWR5iaytNOn7ccG2wTbkEpd6yiczCYsolnZJgrwG8509eFQh3qorBibibm6Bh0qx1ZpLu3cfw/0?wx_fmt=png">点击加入饿了么美团红包互点群</a>\n\n<a href="https://mp.weixin.qq.com/s/sRoXiWti9yZtlEy2d9LOfQ">饿了么红包监控，下个最佳时自动通知你</a>'
        r['code'] = 1
        r['msg'] = rs
        return r
    elif text == '机器人':
        r['code'] = 2
        return r
    elif text == '指令' or text == '菜单' or text == '帮助':
        rs = 'Hi~ 下面是我目前支持的功能，需要什么就回复对应指令哈（如：001）\n\n'+ZHILING
        r['code'] = 1
        r['msg'] = rs
        return r
    elif '壁纸' in text or '王者' in text or '联盟' in text or 'lol' in text:
        rs = 'Hi~ 您是不是在找壁纸呢？需要哪个游戏的壁纸就回复哪个指令哈（如：001）\n\n'+ZHILING
        r['code'] = -1
        r['msg'] = rs
        return r
    else:
        if state:
            key_state = return_keyInfo(KEY_PATH, text)
            if key_state == 0:
                rs = '害~ 没找到你要的东西，请先发送指令我才知道你要什么哦\n\n发送“指令”可查看指令大全'
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

@asyncs
def del_action_dict(fromUser):
    write_log(1, '字典 action_dict 新增了 key：[{}] 动作为[{}] 当前共有{}个人在进行指令操作'.format(fromUser, action_dict[fromUser], len(action_dict)))
    time.sleep(300)
    value = action_dict.pop(fromUser)
    write_log(1, '字典 action_dict 移除了 key：[{}] 动作为[{}] 当前还剩{}个人在进行指令操作'.format(fromUser, value, len(action_dict)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # 加上host这段，就可以在浏览器访问你的网址, 新浪SAE需要指定5050端口