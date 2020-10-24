from nonebot.default_config import *

SUPERUSERS = {541116212}
ADMIN = '541116212'
COMMAND_START = {'', '/', '!', '／', '！'}

HOST = '127.0.0.1'
PORT = 8080

# WZ_GROUP_ID = 175272593
WZ_GROUP_ID = 161758669
# BOT_QQ = 184417622
BOT_QQ = 173391006

GET_WZ_WALL_HOST = 'http://localhost:90/wall/?type=wz&name={}'

ELE_SIGN_MOBILE_HOST = 'http://localhost:90/ele_sign/?type=mobile&fromUser={}&content={}'
ELE_SIGN_CAPTCHA_HOST = 'http://localhost:90/ele_sign/?type=captcha&fromUser={}&content={}'
ELE_SIGN_CODENUM_HOST = 'http://localhost:90/ele_sign/?type=codenum&fromUser={}&content={}'
ELE_SIGN_CODENUM_HD_HOST = 'http://localhost:90/ele_sign/?type=codenum_hd&fromUser={}&content={}'

# HOST = 'localhost'
# HOST = '122.51.67.37'
USER = 'root'
PWD = 'MUGVHmugvtwja116ye38b1jhb'
# PWD = '123456'
# PWD = 'mm123456'
DB_NAME = 'public'

eleme_sign_dict = {}
card_dict = {}



# 王者菜单提示

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