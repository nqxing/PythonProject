HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                  ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}

IS_DAILI = False  # 红包是否要加上代理访问
IS_HTTPS = True  # 是否关闭SSL证书验证 报443时打开此开关解决验证问题

# ELEME_DATA_PATH = r'config\wxbot.db'  # 账号数据库地址
# RILI_PATH = r'plugins\clock_in\rili\rili.db'

ELE_SIGN_MOBILE_HOST = 'http://localhost:90/ele_sign/?type=mobile&fromUser={}&content={}'
ELE_SIGN_CAPTCHA_HOST = 'http://localhost:90/ele_sign/?type=captcha&fromUser={}&content={}'
ELE_SIGN_CODENUM_HOST = 'http://localhost:90/ele_sign/?type=codenum&fromUser={}&content={}'
ELE_SIGN_CODENUM_HD_HOST = 'http://localhost:90/ele_sign/?type=codenum_hd&fromUser={}&content={}'

GET_WZ_WALL_HOST = 'http://localhost:90/wall/?type=wz&name={}'
GET_LOL_WALL_HOST = 'http://localhost:90/wall/?type=lol&name={}'
ELMME_SIGN_TXT = "C:/PythonProject/Django/public/static/wx_public/sign/{}"

PROXY = '59.44.247.194:9797'
PROXIES = {
    'http': 'http://' + PROXY,
    'https': 'https://' + PROXY
}

DEFAULT_HB_TIME = 7  # 红包每隔多少秒查询一次，若报操作太快了请增加秒数

HOST = '127.0.0.1'
# HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'
DB_NAME = 'public'

TIPS = {
    'bz': 'tips：发送“{}壁纸”可获取{}全皮肤壁纸哦，发送“菜单”可查看完整关键字列表',
    'jn': 'tips：发送“{}技能”可快速了解{}技能介绍哦，发送“菜单”可查看完整关键字列表',
    'sl': 'tips：发送“{}胜率”可查看{}最新胜率榜哦，发送“菜单”可查看完整关键字列表',
    'cz': 'tips：发送“{}出装”可查看{}出装推荐哦，发送“菜单”可查看完整关键字列表',
    'mw': 'tips：发送“{}铭文”可查看{}最新铭文搭配哦，发送“菜单”可查看完整关键字列表',
    'kz': 'tips：发送“{}克制”可查看{}英雄克制关系哦，发送“菜单”可查看完整关键字列表',
    'js': 'tips：发送“{}介绍”可查看{}的故事介绍哦，发送“菜单”可查看完整关键字列表',
    'zh': 'tips：发送“{}组合”可查看{}双/三排组合推荐哦，发送“菜单”可查看完整关键字列表',
    'jq': 'tips：发送“{}技巧”可查看{}使用技巧哦，发送“菜单”可查看完整关键字列表',
}