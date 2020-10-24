# APPID = 'wx783e5537bd7ee69b'
# APPSECRET = '67c6b5ba477796e0a06945c71109e4ce'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}
# HEADERS = {
#     'User-Agent': 'Rajax/1 16th/meizu_16th_CN Android/8.1.0 Display/Flyme_8.0.0.0A Eleme/8.30.1 Channel/meizu ID/db0f7c28-eb3d-3548-97c0-196205639927; KERNEL_VERSION:4.9.65-perf+ API_Level:27 Hardware:6c8be58e32dfebacddf1a397548ad297',
#     'x-ttid': 'meizu@eleme_android_8.30.1',
#     'X-Shard': 'loc=119.21251974999905,26.037580892443657',
#     'X-Eleme-RequestID': 'B7F79F16B66248A2BB3652DEACC47936|1584426543206',
#     'X-Sopush-Appkey': '24895413',
#     'X-Sopush-Appversion': '8.30.1',
#     'x-bx-version': '6.4.1',
#     'x-devid': 'XQtDE+3LuTIDABb9EaEOhLDZ',
#     'Content-Type': 'application/json; charset=UTF-8',
#     'Host': 'restapi.ele.me'
# }

WZ_PATH = r'C:\PythonProject\wxBot\bizhi\wzry\wzry.db'
LM_PATH = r'C:\PythonProject\wxBot\bizhi\yxlm\yxlm.db'

KEY_PATH = r'package\keywords\keyword.db'
ELEME_DATA_PATH = r'package\eleme\eleme.db'  # 账号数据库地址
COPY_IMG_PATH = r'package\removebk\image\{}'
BG_ID_PATH = r'package\removebk\{}'

NEW_COPY_IMG_PATH = r'C:\inetpub\wwwroot\wxPublic\image'
CAPTCHA_IMG_PATH = r'C:\inetpub\wwwroot\wxPublic\captcha'
ELMME_SIGN_TXT = r'C:\inetpub\wwwroot\wxPublic\sign'

HOST_URL = 'zqfx.52qdg.com:81'
# HOST_URL = '122.51.67.37:81'

XML_TEXT = '<xml>' \
           '<ToUserName><![CDATA[{}]]></ToUserName>' \
           '<FromUserName><![CDATA[{}]]></FromUserName>' \
           '<CreateTime>{}</CreateTime>' \
           '<MsgType><![CDATA[text]]></MsgType>' \
           '<Content><![CDATA[{}]]></Content>' \
           '</xml>'

XML_IMGAGE = '<xml>' \
           '<ToUserName><![CDATA[{}]]></ToUserName>' \
           '<FromUserName><![CDATA[{}]]></FromUserName>' \
           '<CreateTime>{}</CreateTime>' \
           '<MsgType><![CDATA[image]]></MsgType>' \
           '<Image><MediaId><![CDATA[{}]]></MediaId></Image>' \
           '</xml>'

XML_NEWS = '''
          <xml>
          <ToUserName><![CDATA[{}]]></ToUserName>
          <FromUserName><![CDATA[{}]]></FromUserName>
          <CreateTime>{}</CreateTime>
          <MsgType><![CDATA[news]]></MsgType>
          <ArticleCount>1</ArticleCount>
          <Articles>
            <item>
              <Title><![CDATA[{}]]></Title>
              <Description><![CDATA[{}]]></Description>
              <PicUrl><![CDATA[{}]]></PicUrl>
              <Url><![CDATA[{}]]></Url>
            </item>
          </Articles>
        </xml>
        '''
KEY_NEWS_BOT = XML_NEWS.format("{}", "{}", "{}", "点击添加机器人微信", "查看详情", "https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt7Q5D7j9yibV3JseYyUXJtZ9icpaaTcEhF8Kj4LcUtv5IkKVw0PuKzP81Roic8icWffufGEynDbdYPLgQ/0?wx_fmt=png", "https://mp.weixin.qq.com/s/LuKaolxaNBZ9SLxcK18mTQ")

ZHILING = '''001  -->  王者荣耀最新全英雄皮肤壁纸
002  -->  王者荣耀全皮肤台词语音包
003  -->  英雄联盟最新全英雄皮肤壁纸
004  -->  饿了么APP每日自动签到
005  -->  一键去除抖音快手等短视频水印
006  -->  简单一步生成红蓝白底证件照
007  -->  垃圾分类查询
008  -->  上下班打卡微信提醒
009  -->  加入饿了么美团红包互点群\n
更多功能增加中...
'''
