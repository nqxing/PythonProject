from app_auto_reply.models import *
from pub_zqwz.config import *
from django.http import HttpResponse
from django.views import View
import random
from app_auto_reply.api.create_html import html

num = 0


def fnum():
    global num
    num = num + 1
    return num

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
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
    headers['User-Agent'] = random.choice(user_agent_list)

    url = 'https://camp.qq.com/h5/statichtml/hero-detail/{}.html'.format(hero_id)
    text = None
    r = requests.get(url, headers=headers, verify=False)
    if hero_id == '142':
        r = requests.get(url, headers=headers, verify=False)
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
        text_list = [] #正则匹配到初始js变量列表

        # 查询最新英雄接口
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

        # 查看所有英雄是否已经入库，若没有则添加到数据库
        for i in hero_ids:
            values = pubWZHeroName.objects.filter(hero_id=int(i))
            if values.exists():
                value = values[0]
                # 查看英雄别名常量HERO_BM_DICT是否有更新
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

        date = datetime.datetime.now().strftime('%Y%m%d')
        save_path = r'wz_info/{}'.format(date)
        folder = os.path.exists(save_path)
        if not folder:
            os.makedirs(save_path)

        # hero_dic = {'154': '花木兰', '123': '吕布'}
        hero_ids = list(hero_dic.keys())

        run_fun(save_path, hero_ids, date)
        files = os.listdir(save_path)  # 读入文件夹
        if len(hero_ids) != len(files):
            log(3, '没有获取到全部英雄数据，可能是请求异常了')
        else:
            log(1, '王者全部英雄数据获取完成，准备写入数据库')
            for file in files:
                f = open("{}/{}".format(save_path, file), "r", encoding='utf-8')
                lines = f.readlines()  # 读取全部内容
                if lines:
                    text_list.append(lines[0])
            sava_db(text_list, yx_tup, gx_tup)

    except:
        log(3, traceback.format_exc())

# 异常自动重试，tries重试次数 delay每次重试间隔多少秒
@retry(tries=10, delay=30)
def run_fun(save_path, hero_ids, date):
    files = os.listdir(save_path)   # 读入文件夹
    if len(hero_ids) != len(files):
        for i in hero_ids:
            file_name = "{}/{}-{}.txt".format(save_path, date, i)
            state = os.path.exists('{}'.format(file_name))
            if not state:
                value = get_hero_json(i)
                if value != None:
                    log(1, '{}，写入成功'.format(file_name))
                    with open("{}".format(file_name), "w", encoding='utf-8') as f:
                        f.write(value)
                else:
                    log(3, "{}, 没有获取到英雄id[{}]的信息".format(value, i))
            time.sleep(randint(7, 11))

def sava_db(text_list, yx_tup, gx_tup):
    res_dict_list = []  # 英雄信息转化成json后的列表集合
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
        html_dict = {}
        yxmc, yxdw, yxzz, yxsg, yxzy, yxsf, yxqy, yxnl, yxgx, yxxj = None, None, None, None, None, None, None, None, None, None
        yxyy = []
        def wgs(hero_name):
            values = pubWZGS.objects.filter(cx_name='{}故事'.format(hero_name))
            if values.exists():
                estr = values[0].cx_value
                html_dict['GSTEXT{}'.format(fnum())] = estr
            else:
                html_dict['GSTEXT{}'.format(fnum())] = '数据暂未更新'
        def wmtext(text):
            gllist = text.replace('||', '|').split('|')
            gllist.pop(0)
            for gl in gllist:
                if gl:
                    html_dict['MTEXT{}'.format(fnum())] = gl
        def wequip(heroId):
            values = pubWZEquip.objects.filter(hero_id=int(heroId))
            if values.exists():
                estr = values[0].cx_value1
                template = estr
                dslist = template.split('||')
                for ds in dslist:
                    if ds:
                        s = ds.split('|')
                        p = ''
                        ls = []
                        for k in s:
                            if '大神' in k:
                                p += k
                            if ' ' in k:
                                s = k.split(' ')
                                if len(s) == 3:
                                    ls += s
                                if len(s) == 2:
                                    u = '｜'.join(s)
                                    p += u
                        html_dict['MTEXT{}'.format(fnum())] = p
                        html_dict['EQUIP{}'.format(fnum())] = ls

        heroName = res_dict['state']['heroDetail']['heroInfo']['szTitle']
        heroId = res_dict['state']['heroDetail']['heroId']
        hpic_values = pubWZWall.objects.filter(hero_id=int(heroId))
        if hpic_values.exists():
            hpic = hpic_values[0].skin_url
            html_dict['PIC{}'.format(fnum())] = hpic
        heroName_values = pubWZHeroName.objects.filter(hero_id=int(heroId))
        hero_cxNames = [heroName]
        if heroName_values.exists():
            hero_name_bm = heroName_values[0].hero_name_bm
            if hero_name_bm != None:
                if '|' in hero_name_bm:
                    hero_cxNames += hero_name_bm.split('|')
                else:
                    hero_cxNames.append(hero_name_bm)
        dwInfo = '{}/{}'.format(res_dict['state']['heroDetail']['heroInfo']['szHeroType'],
                                res_dict['state']['heroDetail']['heroInfo']['szBranchRoad'])
        csHeroInfo = '【英雄】{}({})'.format(heroName, dwInfo)
        # 艾琳没有故事信息
        if heroId != '155':
            # 英雄简介部分信息
            res_json = requests.get('https://pvp.qq.com/zlkdatasys/storyhero/index{}.json'.format(heroId)).json()
            da_ac = res_json['da_ac'][0]
            hero_info = '【英雄】{}({})|【定位】{}'.format(da_ac['YXMC_8f'], da_ac['yxbm_72'], dwInfo)
            yxmc = '【英雄】{}({})'.format(da_ac['YXMC_8f'], da_ac['yxbm_72'])
            yxdw = '【定位】{}'.format(dwInfo)
            if da_ac['yxzz_b8']:
                hero_info += '|【种族】{}'.format(da_ac['yxzz_b8'])
                yxzz = '【种族】{}'.format(da_ac['yxzz_b8'])
            if da_ac['sg_30']:
                hero_info += '|【身高】{}'.format(da_ac['sg_30'])
                yxsg = '【身高】{}'.format(da_ac['sg_30'])
            if da_ac['yxsl_54']:
                hero_info += '|【阵营】{}'.format(da_ac['yxsl_54'])
                yxzy = '【阵营】{}'.format(da_ac['yxsl_54'])
            if da_ac['yxsf_48']:
                hero_info += '|【身份】{}'.format(da_ac['yxsf_48'])
                yxsf = '【身份】{}'.format(da_ac['yxsf_48'])
            if da_ac['qym_e7']:
                hero_info += '|【区域】{}'.format(da_ac['qym_e7'])
                yxqy = '【区域】{}'.format(da_ac['qym_e7'])
            if da_ac['nl_96']:
                hero_info += '|【能量】{}'.format(da_ac['nl_96'])
                yxnl = '【能量】{}'.format(da_ac['nl_96'])
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
                yxgx = gx_str.strip().replace('|', '')
            if da_ac['rsy_49']:
                hero_info += '|【人生箴言】{}'.format(da_ac['rsy_49'])
            if res_json['cjjj_6c']:
                hero_info += '|【人物小记】{}'.format(res_json['cjjj_6c'])
                yxxj = '{}'.format(res_json['cjjj_6c'])
            if 'yy_4e' in res_json:
                hero_info += '|【英雄语音】'
                yxyy.append('【英雄语音】')
                yy_4e = res_json['yy_4e']
                for y in yy_4e:
                    hero_info += '|{}'.format(y['yywa1_f2'])
                    yxyy.append(y['yywa1_f2'])

            html_dict['HTEXT{}'.format(fnum())] = yxxj
        else:
            hero_info = ''


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
        html_dict['MARK{}'.format(fnum())] = '英雄热度：'
        wmtext(winRateInfo)
        html_dict['MARK{}'.format(fnum())] = '英雄信息：'
        html_dict['MTEXT{}'.format(fnum())] = yxmc
        html_dict['MTEXT{}'.format(fnum())] = yxdw
        html_dict['MTEXT{}'.format(fnum())] = yxzz
        html_dict['MTEXT{}'.format(fnum())] = yxsg
        html_dict['MTEXT{}'.format(fnum())] = yxzy
        html_dict['MTEXT{}'.format(fnum())] = yxsf
        html_dict['MTEXT{}'.format(fnum())] = yxqy
        html_dict['MTEXT{}'.format(fnum())] = yxnl
        html_dict['MTEXT{}'.format(fnum())] = yxgx
        for y in yxyy:
            html_dict['MTEXT{}'.format(fnum())] = y

        # 英雄核心装备部分信息
        equipInfo = csHeroInfo
        equipInfos = res_dict['state']['heroDetail']['equipInfo']

        html_dict['MARK{}'.format(fnum())] = '出装铭文：'
        szTitle = '数据暂未更新'
        if equipInfos:
            if len(equipInfos) == 3:
                szTitle = '核心装备：{} {} {}'.format(equipInfos[0]['szTitle'], equipInfos[1]['szTitle'], equipInfos[2]['szTitle'])
            for i, e in enumerate(equipInfos):
                showRate = float(e['showRate']) * 100
                winRate = float(e['winRate']) * 100
                equipInfo += '||【核心装备{}】{}[{}]|登场率{}% 胜率{}%'.format(i + 1, e['szTitle'], e['szCate'], '%.2f' % showRate,
                                                                    '%.2f' % winRate)
        else:
            equipInfo += '||数据暂未更新'
        html_dict['MTEXT{}'.format(fnum())] = szTitle
        html_dict['MTEXT{}'.format(fnum())] = ""

        wequip(heroId)

        html_dict['MTEXT{}'.format(fnum())] = ""
        # 英雄铭文部分信息
        runeRankInfo = csHeroInfo
        runeRank = res_dict['state']['heroDetail']['runeInfo']['runeRank']
        if runeRank:
            for i, r in enumerate(runeRank):
                showRate = float(r['showRate']) * 100
                winRate = float(r['winRate']) * 100
                rs = '||【铭文搭配{}】'.format(i + 1)
                wins = '|登场率{}% 胜率{}%'.format('%.2f' % showRate, '%.2f' % winRate)
                rstr = '【铭文搭配{}】登场率{}%｜胜率{}%'.format(i + 1, '%.2f' % showRate, '%.2f' % winRate)
                html_dict['MTEXT{}'.format(fnum())] = rstr
                rlist = []
                hongs = '|红色铭文：'
                lans = '|蓝色铭文：'
                lvs = '|绿色铭文：'
                for l in r['list']:
                    if l['szColor'] in hongs:
                        hongs += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
                        rlist.append('5级铭文:{}'.format(l['szTitle'].split(':')[-1]))
                    if l['szColor'] in lans:
                        lans += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
                        rlist.append('5级铭文:{}'.format(l['szTitle'].split(':')[-1]))
                    if l['szColor'] in lvs:
                        lvs += '{}x{} '.format(l['szTitle'].split(':')[-1], str(l['num']))
                        rlist.append('5级铭文:{}'.format(l['szTitle'].split(':')[-1]))
                html_dict['RUNE{}'.format(fnum())] = rlist
                html_dict['MTEXT{}'.format(fnum())] = hongs.replace('|', '')
                html_dict['MTEXT{}'.format(fnum())] = lans.replace('|', '')
                html_dict['MTEXT{}'.format(fnum())] = lvs.replace('|', '')

                runeRankInfo += '{}{}{}{}{}'.format(rs, hongs.strip(), lans.strip(), lvs.strip(), wins)
        else:
            runeRankInfo += '||数据暂未更新'

        # 写英雄攻略部分
        html_dict['MARK{}'.format(fnum())] = '打法攻略：'
        values = pubWZSkills.objects.filter(cx_name='{}攻略'.format(heroName))
        if values.exists():
            estr = values[0].cx_value
            wmtext(estr)

        # 英雄克制关系部分信息
        kzInfo = '|'
        html_dict['MARK{}'.format(fnum())] = '克制关系：'
        kzInfos = res_dict['state']['heroDetail']['kzInfo']['list']
        bkzInfos = res_dict['state']['heroDetail']['bkzInfo']['list']
        skz = '数据暂未更新'
        sbkz = '数据暂未更新'
        if kzInfos and bkzInfos:
            if len(kzInfos) == 3 and len(bkzInfos) == 3:
                skz = '克制英雄：{} {} {}'.format(kzInfos[0]['szTitle'], kzInfos[1]['szTitle'], kzInfos[2]['szTitle'])
                sbkz = '被克制英雄：{} {} {}'.format(bkzInfos[0]['szTitle'], bkzInfos[1]['szTitle'], bkzInfos[2]['szTitle'])
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

        html_dict['MTEXT{}'.format(fnum())] = skz
        html_dict['MTEXT{}'.format(fnum())] = sbkz

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

        # 英雄技能部分信息
        html_dict['MARK{}'.format(fnum())] = '技能介绍：'
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
            html_dict['MTEXT{}'.format(fnum())] = '【{}({})】初始{}CD{}秒/消耗{}'.format(s['szTitle'], jn, s['szType'], s['iCoolDown'], s['iLoss'])
            html_dict['MTEXT{}'.format(fnum())] = '{}'.format(szDesc.strip())

        html_dict['MARK{}'.format(fnum())] = '英雄故事：'
        wgs(heroName)
        global num
        num = 0
        # log(1, html_dict)
        html(html_dict, heroName, heroId)

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

        # 将别名更新到英雄壁纸库
        if len(hero_cxNames) == 1:
            hero_name_bm = ''
        else:
            del (hero_cxNames[0])
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
    win_str = '||---全服前20胜率排行榜---'
    for i, win in enumerate(reversed(wins)):
        win_str += win
        if i == 19:
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