from app_auto_reply.models import *
from pub_zqwz.config import *
from django.http import HttpResponse
from django.views import View
import random

class UPWZHeroInfo(View):
    def get(self, request):
        # value = request.session.get("msg", None)
        # if value == "登录成功":
        if is_thread():
            return HttpResponse("后台有更新任务，请勿重复更新")
        else:
            run_main()
            log(1, '开始更新王者信息')
            return HttpResponse("后台更新中")
        # else:
        #     return HttpResponse(status=400)

def sort_key(s):
    # 排序关键字匹配
    # 匹配数字序号
    if s:
        try:
            c = re.findall(r'\d+\.\d+', s)[0]
        except:
            c = -1
        return float(c)
def strsort(alist):
    alist.sort(key=sort_key)
    return alist

def get_hero_json(hero_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
    headers['User-Agent'] = random.choice(user_agent_list)

    url = 'https://camp.qq.com/h5/statichtml/hero-detail/{}.html'.format(hero_id)
    text = None
    r = requests.get(url, headers=headers)
    if text == None:
        r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    values = re.findall('<script>(.*?)</script>', r.text, re.S)
    for v in values:
        if 'window.__NUXT__=function' in v:
            text = v
    return text
def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-upwz-hero-info" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-upwz-hero-info')
        thr.start()
    return wrapper

@asyncs
def run_main():
    try:
        text_list = [] #正则匹配到初始js变量
        res_dict_list = [] #英雄信息转化成json后的列表集合
        r = requests.get('http://game.gtimg.cn/images/yxzj/web201706/js/heroid.js')
        r.encoding = 'gbk'
        heros = re.findall('module_exports = {(.*?)};', r.text, re.S)
        hero = '{%s}' % heros[0].replace("'", '"')
        hero_dic = json.loads('{}'.format(hero))
        hero_ids = list(hero_dic.keys())

        # 英雄关系数据接口
        datas = requests.get('https://game.gtimg.cn/images/yxzj/act/a20160510story/relavance/data.js').text
        datas = re.sub('\s', '', datas)
        tups = re.findall('\((.*?)\)', datas, re.S)
        yx_tup = eval('({})'.format(tups[1]))
        gx_tup = eval('({})'.format(tups[2]))

        for i in hero_ids:
            values = pubWZHeroName.objects.filter(hero_id=int(i))
            if values.exists():
                value = values[0]
                if i in HERO_BM_DICT:
                    if HERO_BM_DICT[i] != value.hero_name_bm:
                        value.hero_name_bm = HERO_BM_DICT[i]
                        value.save()
            else:
                pub = pubWZHeroName()
                pub.hero_id = int(i)
                pub.hero_name = hero_dic[i]
                if i in HERO_BM_DICT:
                    pub.hero_name_bm = HERO_BM_DICT[i]
                pub.save()
        # hero_dic = {'142': '安琪拉',}
        # hero_ids = list(hero_dic.keys())
        for i in hero_ids:
            text = get_hero_json(i)
            if text != None:
                text_list.append(text)
            else:
                log(3, "{}".format(text))
                log(3, "获取英雄id[{},{}]信息出错".format(i, hero_dic[i]))
        # windows环境
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)

        # linux环境
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        for t in text_list:
            js = """
            var res = JSON.stringify(%s)
            return res;
            """ % t
            result = driver.execute_script(js)
            res_dict = json.loads(result)
            res_dict_list.append(res_dict)
        driver.close()
        for res_dict in res_dict_list:
            heroName = res_dict['state']['heroDetail']['heroInfo']['szTitle']
            heroId = res_dict['state']['heroDetail']['heroId']
            heroName_values = pubWZHeroName.objects.filter(hero_id=int(heroId))
            hero_cxNames = [heroName]
            if heroName_values.exists():
                hero_name_bm = heroName_values[0].hero_name_bm
                if hero_name_bm != None:
                    if '|' in hero_name_bm:
                        hero_cxNames += hero_name_bm.split('|')
                    else:
                        hero_cxNames.append(hero_name_bm)
            dwInfo = '{}/{}'.format(res_dict['state']['heroDetail']['heroInfo']['szHeroType'], res_dict['state']['heroDetail']['heroInfo']['szBranchRoad'])
            csHeroInfo = '【英雄】{}({})'.format(heroName, dwInfo)
            # 英雄胜率部分信息
            winRateInfo = csHeroInfo
            gameInfo = res_dict['state']['heroDetail']['gameInfo']['list']
            updateTime = res_dict['state']['heroDetail']['gameInfo']['updateTime']
            for g in gameInfo:
                if g['value']:
                    v = g['value']
                else:
                    v = '暂未更新'
                winRateInfo += '|【{}】{}'.format(g['name'], v)
            winRateInfo += '|【数据更新】{}'.format(updateTime)

            # 英雄技能部分信息
            skillInfo = csHeroInfo
            skillInfos = res_dict['state']['heroDetail']['skillInfo'][0]
            for i, s in enumerate(skillInfos):
                if i == 0:
                    jn = '被动'
                else:
                    jn = '{}技能'.format(i)
                p = re.compile('<[^>]+>')
                szDesc = p.sub("", s['szDesc'])
                skillInfo += '|【{}({})】初始{}CD{}秒/消耗{}|{}'.format(s['szTitle'], jn, s['szType'], s['iCoolDown'], s['iLoss'],
                                                         szDesc.strip())
            # 英雄核心装备部分信息
            equipInfo = csHeroInfo
            equipInfos = res_dict['state']['heroDetail']['equipInfo']
            if equipInfos:
                for i, e in enumerate(equipInfos):
                    showRate = float(e['showRate']) * 100
                    winRate = float(e['winRate']) * 100
                    equipInfo += '||【核心装备{}】{}[{}]|登场率{}% 胜率{}%'.format(i + 1, e['szTitle'], e['szCate'], '%.2f' % showRate,
                                                                '%.2f' % winRate)
            else:
                equipInfo += '||数据暂未更新'

            # 英雄铭文部分信息
            runeRankInfo = csHeroInfo
            runeRank = res_dict['state']['heroDetail']['runeInfo']['runeRank']
            if runeRank:
                for i, r in enumerate(runeRank):
                    showRate = float(r['showRate']) * 100
                    winRate = float(r['winRate']) * 100
                    rs = '||【铭文搭配{}】'.format(i+1)
                    wins = '|登场率{}% 胜率{}%'.format('%.2f' % showRate, '%.2f' % winRate)
                    hongs = '|红色铭文：'
                    lans = '|蓝色铭文：'
                    lvs = '|绿色铭文：'
                    for l in r['list']:
                        if l['szColor'] in hongs:
                            hongs += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
                        if l['szColor'] in lans:
                            lans += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
                        if l['szColor'] in lvs:
                            lvs += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))

                    runeRankInfo += '{}{}{}{}{}'.format(rs, hongs.strip(), lans.strip(), lvs.strip(), wins)
            else:
                runeRankInfo += '||数据暂未更新'

            # 英雄克制关系部分信息
            kzInfo = '|'
            kzInfos = res_dict['state']['heroDetail']['kzInfo']['list']
            bkzInfos = res_dict['state']['heroDetail']['bkzInfo']['list']
            if kzInfos and bkzInfos:
                for i, k in enumerate(kzInfos):
                    kzParam = float(k['kzParam']) * 100
                    kzInfo += '|【克制英雄{}】|{}（克制指数{}）'.format(i + 1, k['szTitle'], '%.2f' % kzParam)
                bkzInfo = '|'
                for i, k in enumerate(bkzInfos):
                    bkzParam = float(k['bkzParam']) * 100
                    bkzInfo += '|【被克制英雄{}】|{}（克制指数{}）'.format(i + 1, k['szTitle'], '%.2f' % bkzParam)
                heroKzInfo = '{}{}{}'.format(csHeroInfo, kzInfo, bkzInfo)
            else:
                heroKzInfo = '{}||数据暂未更新'.format(csHeroInfo)

            # 英雄组合关系部分信息
            dfInfo = ''
            if res_dict['state']['heroDetail']['dfInfo']:
                dfInfos = res_dict['state']['heroDetail']['dfInfo']['list']
                for i, d in enumerate(dfInfos):
                    showRate = d['showRate']
                    winRate = d['winRate']
                    wins = '|登场率{} 胜率{}'.format(showRate, winRate)
                    heros = '|'
                    hero_ids = list(d['heroList'].keys())
                    for h in hero_ids:
                        heros += '{} '.format(d['heroList'][h]['szTitle'])
                    dfInfo += '|【双排组合{}】{}{}'.format(i + 1, heros.strip(), wins)
            tfInfo = ''
            if res_dict['state']['heroDetail']['tfInfo']:
                tfInfos = res_dict['state']['heroDetail']['tfInfo']['list']
                for i, t in enumerate(tfInfos):
                    showRate = t['showRate']
                    winRate = t['winRate']
                    wins = '|登场率{} 胜率{}'.format(showRate, winRate)
                    heros = '|'
                    hero_ids = list(t['heroList'].keys())
                    for h in hero_ids:
                        heros += '{} '.format(t['heroList'][h]['szTitle'])
                    tfInfo += '|【三排组合{}】{}{}'.format(i + 1, heros.strip(), wins)
            if dfInfo and tfInfo:
                zhInfo = '{}|{}|{}'.format(csHeroInfo, dfInfo, tfInfo)
            else:
                zhInfo = '{}||数据暂未更新'.format(csHeroInfo)

            # 艾琳没有故事信息
            if heroId != '155':
                # 英雄简介部分信息
                res_json = requests.get('https://pvp.qq.com/zlkdatasys/storyhero/index{}.json'.format(heroId)).json()
                da_ac = res_json['da_ac'][0]
                hero_info = '【英雄】{}({})|【定位】{}'.format(da_ac['YXMC_8f'], da_ac['yxbm_72'], dwInfo)
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
                    if heroId == g[0]:
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
            else:
                hero_info = ''

            for cxName in hero_cxNames:
                win_cxName = '{}胜率'.format(cxName)
                winRate_values = pubWZwinRate.objects.filter(cx_name=win_cxName)
                if winRate_values.exists():
                    winRate_value = winRate_values[0]
                    if winRateInfo != winRate_value.cx_value:
                        winRate_value.cx_value = winRateInfo
                        winRate_value.update_time_str = updateTime
                        winRate_value.save()
                else:
                    pub = pubWZwinRate()
                    pub.cx_name = win_cxName
                    pub.cx_value = winRateInfo
                    pub.hero_name = heroName
                    pub.hero_id = int(heroId)
                    pub.update_time_str = updateTime
                    pub.save()
                skill_cxName = '{}技能'.format(cxName)
                skill_values = pubWZSkill.objects.filter(cx_name=skill_cxName)
                if skill_values.exists():
                    skill_value = skill_values[0]
                    if skillInfo != skill_value.cx_value:
                        skill_value.cx_value = skillInfo
                        skill_value.save()
                else:
                    pub = pubWZSkill()
                    pub.cx_name = skill_cxName
                    pub.cx_value = skillInfo
                    pub.hero_name = heroName
                    pub.hero_id = int(heroId)
                    pub.save()
                equip_cxName = '{}出装'.format(cxName)
                equip_values = pubWZEquip.objects.filter(cx_name=equip_cxName)
                if equip_values.exists():
                    equip_value = equip_values[0]
                    if equipInfo != equip_value.cx_value:
                        equip_value.cx_value = equipInfo
                        equip_value.save()
                else:
                    pub = pubWZEquip()
                    pub.cx_name = equip_cxName
                    pub.cx_value = equipInfo
                    pub.hero_name = heroName
                    pub.hero_id = int(heroId)
                    pub.save()
                rune_cxName = '{}铭文'.format(cxName)
                rune_values = pubWZRune.objects.filter(cx_name=rune_cxName)
                if rune_values.exists():
                    rune_value = rune_values[0]
                    if runeRankInfo != rune_value.cx_value:
                        rune_value.cx_value = runeRankInfo
                        rune_value.save()
                else:
                    pub = pubWZRune()
                    pub.cx_name = rune_cxName
                    pub.cx_value = runeRankInfo
                    pub.hero_name = heroName
                    pub.hero_id = int(heroId)
                    pub.save()
                kz_cxName = '{}克制'.format(cxName)
                kz_values = pubWZKZ.objects.filter(cx_name=kz_cxName)
                if kz_values.exists():
                    kz_value = kz_values[0]
                    if heroKzInfo != kz_value.cx_value:
                        kz_value.cx_value = heroKzInfo
                        kz_value.save()
                else:
                    pub = pubWZKZ()
                    pub.cx_name = kz_cxName
                    pub.cx_value = heroKzInfo
                    pub.hero_name = heroName
                    pub.hero_id = int(heroId)
                    pub.save()

                if heroId != '155':
                    intr_cxName = '{}介绍'.format(cxName)
                    intr_values = pubWZIntroduce.objects.filter(cx_name=intr_cxName)
                    if intr_values.exists():
                        intr_value = intr_values[0]
                        if hero_info != intr_value.cx_value:
                            intr_value.cx_value = hero_info
                            intr_value.save()
                    else:
                        pub = pubWZIntroduce()
                        pub.cx_name = intr_cxName
                        pub.cx_value = hero_info
                        pub.hero_name = heroName
                        pub.hero_id = int(heroId)
                        pub.save()

                if '组合' in zhInfo:
                    zh_cxName = '{}组合'.format(cxName)
                    zh_values = pubWZZH.objects.filter(cx_name=zh_cxName)
                    if zh_values.exists():
                        zh_value = zh_values[0]
                        if zhInfo != zh_value.cx_value:
                            zh_value.cx_value = zhInfo
                            zh_value.save()
                    else:
                        pub = pubWZZH()
                        pub.cx_name = zh_cxName
                        pub.cx_value = zhInfo
                        pub.hero_name = heroName
                        pub.hero_id = int(heroId)
                        pub.save()

            # 英雄壁纸部分信息
            if len(hero_cxNames) == 1:
                hero_name_bm = ''
            else:
                del(hero_cxNames[0])
                hero_name_bm = ' '.join(hero_cxNames)
            skin_infos = pubWZWall.objects.filter(hero_id=int(heroId))
            if skin_infos.exists():
                for skin in skin_infos:
                    hero_name_bms = '{} {}'.format(hero_name_bm, skin.skin_name)
                    if skin.hero_name_bm != None:
                        if skin.hero_name_bm != hero_name_bms:
                            skin.hero_name_bm = hero_name_bms
                            skin.save()
                    else:
                        skin.hero_name_bm = hero_name_bms
                        skin.save()

        #  20201030新增英雄胜率前十排行榜
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        }
        url = 'https://camp.qq.com/h5/statichtml/hero-rank.html'
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        rows = pq(r.text)('.table-grid_body .table-grid_body-row').items()
        times = pq(r.text)('.time').text()
        wins = []
        for row in rows:
            cells = row('.table-grid_body-cell').items()
            hero_name, win = None, None
            for i, cell in enumerate(cells):
                if i == 0:
                    hero_name = cell('.hero-single .hero-info .hero-name').text()
                if i == 2:
                    win = cell.text()
            if hero_name != None and win != None:
                wins.append('|【{}】{}'.format(hero_name, win))
        wins = strsort(wins)
        win_str = '||---全服前十胜率排行榜---'
        for i, win in enumerate(reversed(wins)):
            win_str += win
            if i == 9:
                break
        winRate_values = pubWZwinRate.objects.filter(cx_name="胜率排行榜")
        if winRate_values.exists():
            winRate_value = winRate_values[0]
            if win_str != winRate_value.cx_value:
                winRate_value.cx_value = win_str
                winRate_value.update_time_str = times
                winRate_value.save()
        else:
            pub = pubWZwinRate()
            pub.cx_name = "胜率排行榜"
            pub.cx_value = win_str
            pub.hero_name = "全英雄"
            pub.hero_id = 1000
            pub.update_time_str = times
            pub.save()
    except:
        log(3, traceback.format_exc())