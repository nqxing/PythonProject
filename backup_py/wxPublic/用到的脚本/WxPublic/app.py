# -*- coding: utf-8 -*-
from flask import request
from flask import Flask, make_response
import hashlib
import time
import xml.etree.ElementTree as et
from tenx_ai import tenx_ai

app = Flask(__name__)
app.debug = True


@app.route('/wx/', methods=['GET','POST'])
# route() 装饰器用于把一个函数绑定到一个 URL
# 在微信公众号修改配置那里，如果你写的是“/wechat/”在括号里，就要在二级域名后面加上，不然就会出现token验证失败的一种情况！
def wechat():
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
        # 获取向服务器发送的消息
        # createTime = xml.find("CreateTime")
        xml_sta = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>'
        # 返回数据包xml的文本回复格式
        if msgType == 'text':
            content = xml.find('Content').text
            # 判断消息类型, 如果返回的字段是text，则是文字
            reply_content = tenx_ai(content)
            r = make_response(xml_sta % (fromUser, toUser, str(int(time.time())), reply_content))
            # 微信公众号做出响应，自动回复的格式如上
            r.content_type = 'application/xml'
            # 定义回复的类型为xml
            return r
            # 输出自动回复
        elif msgType == 'event':
            event = xml.find('Event').text
            if event == 'subscribe':
                xml_re = '''
                                    <xml>
                      <ToUserName><![CDATA[%s]]></ToUserName>
                      <FromUserName><![CDATA[%s]]></FromUserName>
                      <CreateTime>%s</CreateTime>
                      <MsgType><![CDATA[news]]></MsgType>
                      <ArticleCount>2</ArticleCount>
                      <Articles>
                        <item>
                          <Title><![CDATA[%s]]></Title>
                          <Description><![CDATA[%s]]></Description>
                          <PicUrl><![CDATA[%s]]></PicUrl>
                          <Url><![CDATA[%s]]></Url>
                        </item>
                        <item>
                          <Title><![CDATA[%s]]></Title>
                          <Description><![CDATA[%s]]></Description>
                          <PicUrl><![CDATA[%s]]></PicUrl>
                          <Url><![CDATA[%s]]></Url>
                        </item>
                      </Articles>
                    </xml>
                '''
                title = '关注必看，不看后悔'
                description = '你要是不看我，你会失去众多实用功能'
                picUrl = 'https://mmbiz.qlogo.cn/mmbiz_jpg/CFpeqnV0qt6uQDWlvUheuLXkxpOKIYCPuicfbKWsgCTOaFibicVdFJqNOWYzSEbP9RMJ6aEy09S3KEKib2lyzCvkXQ/0?wx_fmt=jpeg'
                url = 'https://mp.weixin.qq.com/s/CMBFO-qqXNrTCzpE4C3RAQ'
                title1 = '我不仅仅是个公众号，我还能聊天哦'
                description1 = '我不仅仅是个公众号，我还能聊天哦'
                picUrl1 = 'http://pic1.cxtuku.com/00/06/78/b9800d9002bd.jpg'
                r = make_response(xml_re % (fromUser, toUser, str(int(time.time())), title, description, picUrl, url, title1, description1, picUrl1, url))
                # 微信公众号做出响应，自动回复的格式如上
                r.content_type = 'application/xml'
                # 定义回复的类型为xml
                return r
            else:
                return ''
        elif msgType == 'link':
            title = xml.find('Title').text
            url = xml.find('Url').text
            description = xml.find('Description').text
            reply_content = '您分享的不是饿了么红包哦'
            r = make_response(xml_sta % (fromUser, toUser, str(int(time.time())), reply_content))
            # 微信公众号做出响应，自动回复的格式如上
            r.content_type = 'application/xml'
            # 定义回复的类型为xml
            return r
        else:
            reply_content = '人家只认识文字和饿了么红包啦(˘•ω•˘)'
            r = make_response(xml_sta % (fromUser, toUser, str(int(time.time())), reply_content))
            # 微信公众号做出响应，自动回复的格式如上
            r.content_type = 'application/xml'
            # 定义回复的类型为xml
            return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # 加上host这段，就可以在浏览器访问你的网址, 新浪SAE需要指定5050端口