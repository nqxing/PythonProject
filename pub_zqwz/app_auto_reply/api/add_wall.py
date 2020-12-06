from app_auto_reply.models import pubWZWall, pubVarList
from django.http import HttpResponse
from django.views import View
from pub_zqwz.config import *
from app_auto_reply.api.public import short_url_new

class AddWall(View):
    def post(self, request):
        try:
            hero_id = request.POST.get("hero_id")
            skin_name = request.POST.get("skin_name")
            hero_name = request.POST.get("hero_name")
            skin_url = request.POST.get("skin_url")
            is_mob = request.POST.get("is_mob")
            p = pubWZWall()
            p.skin_name = skin_name
            p.skin_url = skin_url
            p.hero_name = hero_name
            p.hero_id = int(hero_id)
            short_link = short_url_new(skin_url)
            p.skin_short_url = short_link
            if is_mob != 'False':
                mob_short_link = short_url_new(is_mob)
                p.mob_skin_short_url = mob_short_link
                p.mob_skin_url = is_mob
                send_str = '【{}更新】新增了如下英雄壁纸：||{}|[电脑] {}|[手机] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), skin_name,
                                                            short_link, mob_short_link)
            else:
                send_str = '【{}更新】新增了如下英雄壁纸：||{}|[电脑] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), skin_name,
                                                            short_link)
            p.save()
            pubs = pubVarList.objects.filter(var_name="WZ_NEW_WALL")
            pub = pubs[0]
            pub.var_info = send_str
            pub.save()
            # send_fwx_group(WX_WZ_GROUPS, send_str, True)
            # send_fqq_group(send_str)
            return HttpResponse("新增成功")
        except:
            log(3, format(traceback.format_exc()))
            return HttpResponse("新增异常")