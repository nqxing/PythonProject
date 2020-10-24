from auto_reply.models import pubLOLWall
from auto_reply.package import *
from django.http import HttpResponse
from django.views import View

class UPLOLWall(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            if is_thread():
                return HttpResponse("后台有更新任务，请勿重复更新")
            else:
                run_main()
                write_log(1, '开始更新LOL壁纸')
                return HttpResponse("后台更新中")
        else:
            return HttpResponse(status=400)

def get_new_skin():
    new_bizhi = []
    try:
        r = requests.get('https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js')
        hero_dic = json.loads('{}'.format(r.text))
        hero_ids = hero_dic['hero']
        for i in hero_ids:
            pf_nums = get_skins(i['heroId'])
            if pf_nums:
                for p in pf_nums:
                    if i['title'] in p['name']:
                        pf_name = p['name']
                    else:
                        pf_name = p['name'] + ' {}'.format(i['title'])
                    if p['mainImg']:
                        values = pubLOLWall.objects.filter(skin_name=pf_name, hero_id=i['heroId'])
                        if values.exists():
                            pass
                        else:
                            pub = pubLOLWall()
                            pub.skin_name = pf_name
                            pub.skin_url = p['mainImg']
                            pub.hero_name = i['title']
                            pub.hero_id = int(i['heroId'])
                            short_link = short_url_new(p['mainImg'])
                            pub.skin_short_url = short_link
                            sk_size = get_size(p['mainImg'])
                            pub.skin_size = sk_size
                            new_bizhi.append(('{} {}'.format(pf_name, sk_size), short_link))
                            pub.save()
        return new_bizhi
    except:
        write_log(3, traceback.format_exc())
        return new_bizhi

def get_skins(hid):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    skins = []
    try:
        url = 'http://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(hid)
        r = requests.get(url, headers=headers)
        skins = json.loads('{}'.format(r.text))['skins']
        return skins
    except:
        write_log(3, traceback.format_exc())
        return skins

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-uplol-wall" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-uplol-wall')
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
        pub = pubVarList.objects.filter(var_name="LOL_NEW_WALL")
        pubs = pub[0]
        pubs.var_info = send_str
        pubs.save()
        # send_fwx_group(WX_LOL_GROUPS, send_str, True)
        # 英雄联盟暂无QQ群
        write_log(1, 'LOL壁纸更新成功，新增了{}张壁纸'.format(len(results)))

        # 20201016关闭壁纸下载
        # values = pubLOLWall.objects.all()
        # for v in values:
        #     down_wall(v.skin_name, v.skin_url, None, v.hero_name, 'yxlm', v.skin_size)
    else:
        write_log(1, '程序运行完毕，本次未新增英雄联盟壁纸'.format(len(results)))

