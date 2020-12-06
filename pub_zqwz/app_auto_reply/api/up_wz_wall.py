from app_auto_reply.models import pubWZWall, pubVarList
from pub_zqwz.config import *
from app_auto_reply.api.public import short_url_new
from django.http import HttpResponse
from django.views import View

class UPWZWall(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            if is_thread():
                return HttpResponse("后台有更新任务，请勿重复更新")
            else:
                run_main()
                log(1, '开始更新王者壁纸')
                return HttpResponse("后台更新中")
        else:
            return HttpResponse(status=400)

def get_new_skin():
    skin_names = {}
    new_bizhi = []
    pf_link = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
    mob_pf_link = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-mobileskin-{}.jpg'
    try:
        r = requests.get('http://game.gtimg.cn/images/yxzj/web201706/js/heroid.js')
        r.encoding = 'gbk'
        heros = re.findall('module_exports = {(.*?)};', r.text, re.S)
        hero = '{%s}' % heros[0].replace("'", '"')
        hero_dic = json.loads('{}'.format(hero))
        # hero_dic = {'154': '花木兰', '141': '貂蝉',}
        hero_ids = list(hero_dic.keys())
        for i in hero_ids:
            if i != '155':
                pf_nums = get_skins(i)
                if pf_nums:
                    skin_names[i] = pf_nums
            # print(i)
            time.sleep(1)
        skins = list(skin_names.keys())
        for s in skins:
            for k, p in enumerate(skin_names[s]):
                pf_name = '{} {}'.format(hero_dic[s], p)
                pf_url = pf_link.format(s, s, k + 1)
                mob_pf_url = mob_pf_link.format(s, s, k + 1)
                values = pubWZWall.objects.filter(skin_name=pf_name, hero_id=s)
                if values.exists():
                    pass
                else:
                    pub = pubWZWall()
                    pub.skin_name = pf_name
                    pub.skin_url = pf_url
                    pub.hero_name = hero_dic[s]
                    pub.hero_id = int(s)
                    pub.mob_skin_url = mob_pf_url
                    short_link = short_url_new(pf_url)
                    mob_short_link = short_url_new(mob_pf_url)
                    pub.skin_short_url = short_link
                    new_bizhi.append((pf_name, '[电脑] '+ short_link))
                    pub.mob_skin_short_url = mob_short_link
                    new_bizhi.append((pf_name, '[手机] '+ mob_short_link))
                    if s in HERO_BM_DICT:
                        if '|' in HERO_BM_DICT[s]:
                            bm = ' '.join(HERO_BM_DICT[s].split('|')) + ' {}'.format(pf_name)
                        else:
                            bm = HERO_BM_DICT[s] + ' {}'.format(pf_name)
                    else:
                        bm = pf_name
                    pub.hero_name_bm = bm
                    pub.save()

        return new_bizhi
    except:
        log(3, traceback.format_exc())
        return new_bizhi

def get_skins(hid):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    skin_names = []
    try:
        url = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'.format(hid)
        r = requests.get(url, headers=headers)
        r.encoding = 'gbk'
        skins = pq(r.text)('.pic-pf-list').attr('data-imgname')
        skins = skins.split('|')
        for s in skins:
            if '&' in s:
                skin_names.append(s.split('&')[0])
            else:
                skin_names.append(s)
        return skin_names
    except:
        log(3, traceback.format_exc())
        return skin_names

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-upwz-wall" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-upwz-wall')
        thr.start()
    return wrapper

@asyncs
def run_main():
    results = get_new_skin()
    if results:
        result = ''
        for i in results:
            strs = '{}|{}||'.format(i[0], i[1])
            result += strs
        send_str = '【{}更新】新增了如下英雄壁纸：||{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), result.strip())
        pub = pubVarList.objects.filter(var_name="WZ_NEW_WALL")
        pubs = pub[0]
        pubs.var_info = send_str
        pubs.save()
        # send_fwx_group(WX_WZ_GROUPS, send_str, True)

        # 20201016因酷Q关闭服务，关闭QQ发送通道
        # send_fqq_group(send_str)
        log(1, '王者壁纸更新成功，新增了{}张壁纸'.format(len(results)))

        # 20201016关闭壁纸下载
        # values = pubWZWall.objects.all()
        # for v in values:
        #     down_wall(v.skin_name, v.skin_url, v.mob_skin_url, v.hero_name, 'wzry', None)
    else:
        log(1, '程序运行完毕，本次未新增王者荣耀壁纸'.format(len(results)))

