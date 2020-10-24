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

# WXBOT_PATH = r"C:/PythonProject/Django/wxBot/wxpy.pkl"
WX_WZ_GROUPS = "王者荣耀壁纸群"
WX_LOL_GROUPS = "英雄联盟壁纸群"
QQ_WZ_GROUPS = 161758669
ERROR_QQ = 541116212

COPY_IMG_PATH = r'auto_reply/package/image/{}'
ELE_CAPTCHA_URL = r'http://{}/static/wx_public/captcha/{}.jpg'
ELE_SIGN_URL = r'http://{}/static/wx_public/sign/{}.txt'
IDENT_IMG_URL = r'http://{}/static/wx_public/image/{}'
QR_IMG_URL = r'http://{}/static/wx_public/qr/{}.png'

QR_IMG_PATH = r'static/wx_public/qr'
NEW_COPY_IMG_PATH = r'static/wx_public/image'
CAPTCHA_IMG_PATH = r'static/wx_public/captcha'
ELMME_SIGN_TXT = r'static/wx_public/sign'

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

eleme_sign_cap_dict_api = {}

KEY_NEWS_BOT = XML_NEWS.format("{}", "{}", "{}", "点击添加机器人微信", "查看详情", "https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt7Q5D7j9yibV3JseYyUXJtZ9icpaaTcEhF8Kj4LcUtv5IkKVw0PuKzP81Roic8icWffufGEynDbdYPLgQ/0?wx_fmt=png", "https://mp.weixin.qq.com/s/LuKaolxaNBZ9SLxcK18mTQ")

bm_dict = {
    "154": "木兰",
    "167": "猴子|猴哥",
    "168": "牛头|牛魔王",
    "130": "宫本",
    "116": "阿柯|阿珂",
    "113": "鱼",
    "126": "夏侯",
    "112": "鲁班|卤蛋",
    "132": "马可",
    "157": "火舞",
    "162": "娜可|露露",
    "163": "橘右君",
    "177": "狼狗",
    "184": "奶妈",
    "186": "太乙",
    "190": "诸葛",
    "111": "大小姐",
    "187": "东皇",
    "182": "干将",
    "193": "凯|恺",
    "196": "百里|守约",
    "195": "玄策",
    "502": "老虎",
    "513": "上官|婉儿",
    '511': '八戒',
    "312": "炸弹猫",
    '505': '谣|摇',
    '506': '走地鸡',
    '522': '耀|燿',
    '531': '静|境|竟',
    '527': '蒙括'
}