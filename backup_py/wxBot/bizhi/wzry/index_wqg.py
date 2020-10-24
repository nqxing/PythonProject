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
    url = 'https://smoba.ams.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=yxzj&iActivityId=253767&sServiceDepartment=group_g&sSDID=2e8cf6296c34d41d3b0192633c0c922b&sMiloTag=AMS-MILO-253767-603921-unknown-1570774943358-H77R8u&_=1570774943368'
    dict = {
    'iActivityId': 253767,
    'iFlowId': 603921,
    'g_tk': 1842395457,
    'e_code': 0,
    'g_code': 0,
    'eas_url': 'http%3A%2F%2Fpvp.qq.com%2Fcp%2Fa20190829skin%2Findex_wqg.html',
    'eas_refer': '',
    'sServiceDepartment': 'group_g',
    'sServiceType': 'yxzj'
    }
    r = requests.post(url, data=dict).json()
    sOutValue2 = r['modRet']['sOutValue2']
    sOutValue3 = r['modRet']['sOutValue3']
    sOutValue2S = sOutValue2.split('|')
    sOutValue3S = sOutValue3.split('|')
    tpOutValueS = []
    for i in range(len(sOutValue2S)):
        if sOutValue2S[i] == 'v_1':
            tpOutValueS.append('【{}】{}'.format('武陵仙君-诸葛亮', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_2':
            tpOutValueS.append('【{}】{}'.format('辉光之辰-后羿', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_3':
            tpOutValueS.append('【{}】{}'.format('蜜橘之夏-公孙离', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_4':
            tpOutValueS.append('【{}】{}'.format('魔法小厨娘-安琪拉', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_5':
            tpOutValueS.append('【{}】{}'.format('永曜之星-杨戬', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_6':
            tpOutValueS.append('【{}】{}'.format('游园惊梦-甄姬', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_7':
            tpOutValueS.append('【{}】{}'.format('遇见飞天-杨玉环', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_8':
            tpOutValueS.append('【{}】{}'.format('白虎志-百里玄策', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_9':
            tpOutValueS.append('【{}】{}'.format('冰霜恋舞曲-干将莫邪', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_10':
            tpOutValueS.append('【{}】{}'.format('大圣娶亲-孙悟空', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_11':
            tpOutValueS.append('【{}】{}'.format('奇迹圣诞-蔡文姬', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_12':
            tpOutValueS.append('【{}】{}'.format('瑞麟志-花木兰', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_13':
            tpOutValueS.append('【{}】{}'.format('青龙志-铠', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_14':
            tpOutValueS.append('【{}】{}'.format('玄武志-苏烈', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_15':
            tpOutValueS.append('【{}】{}'.format('一生所爱-露娜', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_16':
            tpOutValueS.append('【{}】{}'.format('朱雀志-百里守约', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_17':
            tpOutValueS.append('【{}】{}'.format('逐梦之光-东皇太一', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_18':
            tpOutValueS.append('【{}】{}'.format('逐梦之星-马可波罗', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_19':
            tpOutValueS.append('【{}】{}'.format('逐梦之翼-哪吒', sOutValue3S[i]))
        if sOutValue2S[i] == 'v_20':
            tpOutValueS.append('【{}】{}'.format('云端筑梦师-庄周', sOutValue3S[i]))
    tpOutValueS = strsort(tpOutValueS)
    result = ''
    for t in range(len(tpOutValueS)):
        result += '{}.{}\n'.format(t+1, tpOutValueS[-(t+1)])
    return result.strip()