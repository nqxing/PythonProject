import requests
import re

def sort_key(s):
    # 排序关键字匹配
    # 匹配数字序号
    if s:
        try:
            c = re.findall(r'(\d+)', s)[0]
        except:
            c = -1
        return int(c)
def strsort(alist):
    alist.sort(key=sort_key)
    return alist

def index_wqg():
    try:
        url = 'https://smoba.ams.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=txyxhdh&iActivityId=331333&sServiceDepartment=group_g&sSDID=a5e073b0157d9252f6d1ea705a7bce4e&sMiloTag=AMS-MILO-331333-704988-oQDeW0d1ggJZqrcdKtaHoHtC65l4-1602896594522-PJnc3X&_=1602896594524'
        # headers = {
        #     'Host': 'smoba.ams.game.qq.com',
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Origin': 'https://pvp.qq.com',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Cookie': 'IED_LOG_INFO2=openid%3DoQDeW0d1ggJZqrcdKtaHoHtC65l4%26loginType%3Dwx; pgv_info=ssid=2709843455; pgv_pvid=2709843455; tokenParams=%3Facctype%3Dwx%26appid%3Dwx1cd4fbe9335888fe%26code%3D071XL50w36N39V2rLR1w3tgVng1XL50d%26state%3DSTATE; access_token=38_WL0-DF72YiVZeaxFOQQo6oyy-ZTKeJodMXU0ZfRGtmd9RMStlGIhHLnOUz6BrPFi_b0VlSoMK8pE0RcxthnI--hDX19sFFogl9M5rerGLZY; acctype=wx; appid=wx1cd4fbe9335888fe; iegams_refresh_token=38_GfP4O91RUmoXFxT5dmHk0WdRJ5xB9xxA_4FTMDefSEVe35aod4GRCS_3PHKX1dmqvSWB2ZpF7D0mzNqzkvXSO2RdVyc_gCJLMvZWwcCR7z0; openid=oQDeW0d1ggJZqrcdKtaHoHtC65l4; wxcode=071XL50w36N39V2rLR1w3tgVng1XL50d; wxnickname=%u8352; pvpqqcomrouteLine=a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh; tvfe_boss_uuid=72d9195e2c4351b8; eas_sid=h1p6B0G0w9620038G0v7G1H2Q8',
        #     'Connection': 'keep-alive',
        #     'Accept': '*/*',
        #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.17(0x17001126) NetType/WIFI Language/zh_CN',
        #     'Referer':'https://pvp.qq.com/cp/a20200907backmh/index-v.html',
        #     'Content-Length': '362',
        #     'Accept-Language': 'zh-cn'
        #
        # }
        headers = {
            'Host': 'smoba.ams.game.qq.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://pvp.qq.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': 'skey=MaSD2pVoYr; uin=o0541116212; pgv_info=ssid=31055872; pgv_pvid=31055872; pvpqqcomrouteLine=a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh_a20200907backmh; qq_locale_id=2052; p_skey=90mmS2Sm0FxLpp2ljOvvbf7Xjp1WeYjZBKGnft-*FK0_; p_uin=o0541116212; IED_LOG_INFO2=userUin%3D541116212%26uin%3D541116212%26nickName%3D%2525E3%252580%252580%26nickname%3D%25E3%2580%2580%26userLoginTime%3D1602896305%26openid%3D%26logtype%3Dpt%26loginType%3Dpt; ams_qqopenid_1104466820=D890D4202FA630663270BFDAEC162020%7C541116212%7Cdf2915ac1f36a53a419c07d2db2f5276; eas_sid=B1b6g0T2K8l6l3K6j7f2f6b1O4; pvid=9452678066',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/18A393 QQ/8.4.9.604 V1_IPH_SQ_8.4.9_1_APP_A Pixel/1080 MiniAppEnable SimpleUISwitch/0 QQTheme/1000 Core/WKWebView Device/Apple(iPhone 8Plus) NetType/WIFI QBWebViewType/1 WKType/1',
            'Referer':'https://pvp.qq.com/cp/a20200907backmh/index-v.html',
            'Content-Length': '315',
            'Accept-Language': 'zh-cn'

        }
        # dict = {
        #     'appid': 'wx1cd4fbe9335888fe',
        #     'sPlatId': 0,
        #     'sArea': 4,
        #     'sServiceType': 'txyxhdh',
        #     'ams_targetappid': 'wx95a3a4d7c627e07d',
        #     'iActivityId': '331333',
        #     'iFlowId': '704988',
        #     'g_tk': '1842395457',
        #     'e_code': '0',
        #     'g_code': '0',
        #     'eas_url': 'http://pvp.qq.com/cp/a20200907backmh/index-v.html',
        #     'eas_refer': 'http://noreferrer/?reqid=681b23ce-45b8-4c8f-8df2-a1734d7cd049',
        #     'version': '23',
        #     'sServiceDepartment': 'group_g'
        # }
        dict = {
            'appid': '1104466820',
            'sPlatId': 0,
            'sArea': 4,
            'sServiceType': 'yxzj',
            'iActivityId': '331333',
            'iFlowId': '704988',
            'g_tk': '412103772',
            'e_code': '0',
            'g_code': '0',
            'eas_url': 'http://pvp.qq.com/cp/a20200907backmh/index-v.html',
            'eas_refer': 'http://noreferrer/?reqid=2af7ed7a-ff72-4536-8f8a-8796cfcce84f',
            'version': '23',
            'sServiceDepartment': 'group_g'
        }
        r = requests.post(url, headers=headers, data=dict).json()
        if r['ret'] == '0':
            vote = r['modRet']['jData']['vote']
            tpOutValueS = []
            if vote:
                slist = vote.keys()
                for s in slist:
                    if s == '1':
                        tpOutValueS.append('【{}】{}'.format('百里玄策-白虎志', vote[s]))
                    if s == '2':
                        tpOutValueS.append('【{}】{}'.format('干将莫邪-冰霜恋舞曲', vote[s]))
                    if s == '3':
                        tpOutValueS.append('【{}】{}'.format('孙悟空-大圣娶亲', vote[s]))
                    if s == '4':
                        tpOutValueS.append('【{}】{}'.format('上官婉儿-梁祝', vote[s]))
                    if s == '5':
                        tpOutValueS.append('【{}】{}'.format('公孙离-蜜橘之夏', vote[s]))
                    if s == '6':
                        tpOutValueS.append('【{}】{}'.format('蔡文姬-奇迹圣诞', vote[s]))
                    if s == '7':
                        tpOutValueS.append('【{}】{}'.format('铠-青龙志', vote[s]))
                    if s == '8':
                        tpOutValueS.append('【{}】{}'.format('花木兰-瑞麟志', vote[s]))
                    if s == '9':
                        tpOutValueS.append('【{}】{}'.format('裴擒虎-天狼狩猎者', vote[s]))
                    if s == '10':
                        tpOutValueS.append('【{}】{}'.format('曹操-天狼征服者', vote[s]))
                    if s == '11':
                        tpOutValueS.append('【{}】{}'.format('苏烈-玄武志', vote[s]))
                    if s == '12':
                        tpOutValueS.append('【{}】{}'.format('庄周-云端筑梦师', vote[s]))
                    if s == '13':
                        tpOutValueS.append('【{}】{}'.format('杨玉环-遇见飞天', vote[s]))
                    if s == '14':
                        tpOutValueS.append('【{}】{}'.format('露娜-一生所爱', vote[s]))
                    if s == '15':
                        tpOutValueS.append('【{}】{}'.format('甄姬-游园惊梦', vote[s]))
                    if s == '16':
                        tpOutValueS.append('【{}】{}'.format('东皇太一-逐梦之光', vote[s]))
                    if s == '17':
                        tpOutValueS.append('【{}】{}'.format('马可波罗-逐梦之星', vote[s]))
                    if s == '18':
                        tpOutValueS.append('【{}】{}'.format('哪吒-逐梦之翼', vote[s]))
                    if s == '19':
                        tpOutValueS.append('【{}】{}'.format('百里守约-朱雀志', vote[s]))
                tpOutValueS = strsort(tpOutValueS)
                result = ''
                for t in range(len(tpOutValueS)):
                    result += '{}.{}\n'.format(t+1, tpOutValueS[-(t+1)])
                return result.strip()
        else:
            return '投票查询失败!'
    except:
        return '投票查询失败!'
a = index_wqg()
print(a)