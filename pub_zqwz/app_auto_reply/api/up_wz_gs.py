from app_auto_reply.models import pubWZGS, pubWZHeroName
from pub_zqwz.config import *
from django.http import HttpResponse
from django.views import View

class UPWZgs(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            if is_thread():
                return HttpResponse("后台有更新任务，请勿重复更新")
            else:
                run_main()
                log(1, '开始更新王者故事')
                return HttpResponse("后台更新中")
        else:
            return HttpResponse(status=400)

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-upwz-gs" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-upwz-gs')
        thr.start()
    return wrapper

@asyncs
def run_main():
    try:
        heros = pubWZHeroName.objects.all()
        for h in heros:
            if h.hero_id != 155:
                url = 'https://pvp.qq.com/zlkdatasys/storyhero/story{}.json'.format(h.hero_id)
                r = requests.get(url).json()
                lj_e9 = r['lj_e9']
                r = requests.get(lj_e9)
                r.encoding = 'utf-8'
                strs = re.findall('"content":`(.*?)`}', r.text, re.S)
                if strs:
                    name = '{}故事'.format(h.hero_name)
                    values = pubWZGS.objects.filter(cx_name=name)
                    if values.exists():
                        zh_value = values[0]
                        if strs[0] != zh_value.cx_value:
                            zh_value.cx_value = strs[0]
                            zh_value.save()
                    else:
                        pub = pubWZGS()
                        pub.cx_name = name
                        pub.cx_value = strs[0]
                        pub.save()
    except:
        log(3, traceback.format_exc())
    log(1, '王者故事更新成功')


