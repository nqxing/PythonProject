import requests
import re
import json
from selenium import webdriver

headers = {
    'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
}
hero_id = 142
url = 'https://image.ttwz.qq.com/h5/statichtml/hero-detail/{}.html'.format(hero_id)
text = None
# var_dict = {}

datas = requests.get('https://game.gtimg.cn/images/yxzj/act/a20160510story/relavance/data.js').text
datas = re.sub('\s', '', datas)
tups = re.findall('\((.*?)\)', datas, re.S)
yx_tup = eval('({})'.format(tups[1]))
gx_tup = eval('({})'.format(tups[2]))

r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
values = re.findall('<script>(.*?)</script>', r.text, re.S)

for v in values:
    if 'window.__NUXT__=function' in v:
        text = v
if text!= None:
    print(text)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    js = """
    var res = JSON.stringify(%s)
    return res;
    """ % text
    result = driver.execute_script(js)
    driver.close()
    res_dict = json.loads(result)
    heroName = res_dict['state']['heroDetail']['heroInfo']['szTitle']
    heroId = res_dict['state']['heroDetail']['heroId']
    print('【英雄】{}({}/{})'.format(heroName, res_dict['state']['heroDetail']['heroInfo']['szHeroType'], res_dict['state']['heroDetail']['heroInfo']['szBranchRoad']))
    gameInfo = res_dict['state']['heroDetail']['gameInfo']['list']
    updateTime = res_dict['state']['heroDetail']['gameInfo']['updateTime']
    for g in gameInfo:
        print('【{}】{}'.format(g['name'], g['value']))
    print('【数据更新】' + updateTime)
    skillInfo = res_dict['state']['heroDetail']['skillInfo'][0]
    for i,s in enumerate(skillInfo):
        if i == 0:
            jn = '被动'
        else:
            jn = '{}技能'.format(i)
        p = re.compile('<[^>]+>')
        szDesc = p.sub("", s['szDesc'])
        print('【{}({})】初始{}CD{}秒，消耗{}|{}'.format(s['szTitle'], jn, s['szType'], s['iCoolDown'], s['iLoss'], szDesc.strip()))
    equipInfo = res_dict['state']['heroDetail']['equipInfo']
    for i,e in enumerate(equipInfo):
        showRate = float(e['showRate'])*100
        winRate = float(e['winRate'])*100
        print('【核心装备{}】{}[{}]（登场率{}%，胜率{}%）'.format(i+1, e['szTitle'], e['szCate'], '%.2f' % showRate, '%.2f' % winRate))
    runeRank = res_dict['state']['heroDetail']['runeInfo']['runeRank']
    for i,r in enumerate(runeRank):
        showRate = float(r['showRate'])*100
        winRate = float(r['winRate'])*100
        rs = '【铭文搭配{}】'.format(i+1)
        ws = '（登场率{}%，胜率{}%）'.format('%.2f' % showRate, '%.2f' % winRate)
        for l in r['list']:
            rs += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
        print(rs.strip()+ws)
    kzInfo = res_dict['state']['heroDetail']['kzInfo']['list']
    for i,k in enumerate(kzInfo):
        kzParam = float(k['kzParam'])*100
        print('【克制英雄{}】{}（克制指数{}）'.format(i+1, k['szTitle'], '%.2f' % kzParam))
    bkzInfo = res_dict['state']['heroDetail']['bkzInfo']['list']
    for i,k in enumerate(bkzInfo):
        bkzParam = float(k['bkzParam'])*100
        print('【被克制英雄{}】{}（克制指数{}）'.format(i+1, k['szTitle'], '%.2f' % bkzParam))
    res_json = requests.get('https://pvp.qq.com/zlkdatasys/storyhero/index{}.json'.format(hero_id)).json()
    da_ac = res_json['da_ac'][0]
    hero_info = '【英雄】{}({})'.format(da_ac['YXMC_8f'], da_ac['yxbm_72'])
    if da_ac['yxzz_b8']:
        hero_info += '|【种族】{}'.format(da_ac['yxzz_b8'])
    if da_ac['sg_30']:
        hero_info += '|【身高】{}'.format(da_ac['sg_30'])
    if da_ac['yxsl_54']:
        hero_info += '|【阵营】{}'.format(da_ac['yxsl_54'])
    if da_ac['yxsf_48']:
        hero_info += '|【身份】{}'.format(da_ac['yxsf_48'])
    if da_ac['qym_e7']:
        hero_info += '|【区域】{}'.format(da_ac['qym_e7'])
    if da_ac['nl_96']:
        hero_info += '|【能量】{}'.format(da_ac['nl_96'])
    gx_str = '|【英雄关系】'
    for g in gx_tup:
        if str(hero_id) == g[0]:
            hero_name = ''
            hero_gx = g[2]
            for y in yx_tup:
                if g[1] == y[0]:
                    hero_name = y[1]
            if hero_name:
                gx_str += '{}({}) '.format(hero_name, hero_gx)
    if gx_str != '|【英雄关系】':
        hero_info += gx_str.strip()
    if da_ac['rsy_49']:
        hero_info += '|【人生箴言】{}'.format(da_ac['rsy_49'])
    if res_json['cjjj_6c']:
        hero_info += '|【人物小记】{}'.format(res_json['cjjj_6c'])
    if 'yy_4e' in res_json:
        hero_info += '|【英雄语音】'
        yy_4e = res_json['yy_4e']
        for y in yy_4e:
            hero_info += '|{}'.format(y['yywa1_f2'])
    print()
    print(hero_info.replace('|', '\n'))