HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}


WX_WZ_GROUPS = "王者荣耀壁纸群"
WX_LOL_GROUPS = "英雄联盟壁纸群"
QQ_WZ_GROUPS = 161758669
ERROR_QQ = 541116212

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

HERO_BM_DICT = {
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

TIP_DICT = {
    'bz': 'tips：发送“{}壁纸”可获取{}全皮肤壁纸哦，发送“王者菜单”可查看完整关键字列表',
    'jn': 'tips：发送“{}技能”可快速了解{}技能介绍哦，发送“王者菜单”可查看完整关键字列表',
    'sl': 'tips：发送“{}胜率”可查看{}最新胜率榜哦，发送“王者菜单”可查看完整关键字列表',
    'cz': 'tips：发送“{}出装”可查看{}出装推荐哦，发送“王者菜单”可查看完整关键字列表',
    'mw': 'tips：发送“{}铭文”可查看{}最新铭文搭配哦，发送“王者菜单”可查看完整关键字列表',
    'kz': 'tips：发送“{}克制”可查看{}英雄克制关系哦，发送“王者菜单”可查看完整关键字列表',
    'js': 'tips：发送“{}介绍”可查看{}的故事介绍哦，发送“王者菜单”可查看完整关键字列表',
    'zh': 'tips：发送“{}组合”可查看{}双/三排组合推荐哦，发送“王者菜单”可查看完整关键字列表',
    'jq': 'tips：发送“{}技巧”可查看{}使用技巧哦，发送“王者菜单”可查看完整关键字列表',
    'yy': 'tips：发送“{}语音”可获取{}皮肤语音包哦，发送“王者菜单”可查看完整关键字列表',
}