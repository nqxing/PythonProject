from auto_reply.models import pubWZWall, pubLOLWall
from django.http import HttpResponse
from django.views import View
from auto_reply.package import *

class Wall(View):
    def get(self, request):
        try:
            gname = request.GET.get("type")
            if gname == 'wz':
                name = request.GET.get("name")
                if name != None and len(name) != 0:
                    results = pubWZWall.objects.filter(skin_name__contains=name)
                    if len(results) != 0:
                        result = '找到了{}张({})的壁纸：\n\n'.format(len(results), name)
                        for res in results:
                            mob_skin = res.mob_skin_short_url
                            if mob_skin == None:
                                strs = '{}\n[电脑] {}\n\n'.format(res.skin_name, res.skin_short_url)
                            else:
                                strs = '{}\n[电脑] {}\n[手机] {}\n\n'.format(res.skin_name, res.skin_short_url, res.mob_skin_short_url)
                            result += strs
                        result = result.strip()
                        return HttpResponse(result)
                    else:
                        return HttpResponse("没有找到({})的壁纸，请确认名字输入正确哦".format(name))
                else:
                    return HttpResponse("英雄名字不能为空")
            elif gname == 'lol':
                name = request.GET.get("name")
                if name != None and len(name) != 0:
                    results = pubLOLWall.objects.filter(skin_name__contains=name)
                    if len(results) != 0:
                        result = '找到了{}张({})的壁纸：\n\n'.format(len(results), name)
                        for res in results:
                            strs = '{} {}\n{}\n\n'.format(res.skin_name, res.skin_size, res.skin_short_url)
                            result += strs
                        result = result.strip()
                        return HttpResponse(result)
                    else:
                        return HttpResponse("没有找到({})的壁纸，请确认名字输入正确哦".format(name))
                else:
                    return HttpResponse("英雄名字不能为空")
            else:
                return HttpResponse("游戏类型不能为空")
        except:
            write_log(3, format(traceback.format_exc()))
            return HttpResponse("查询出错了，请稍后再试")

    def post(self, request):
        try:
            gname = request.POST.get("type")
            if gname == 'wz':
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
            elif gname == 'lol':
                hero_id = request.POST.get("hero_id")
                skin_name = request.POST.get("skin_name")
                hero_name = request.POST.get("hero_name")
                skin_url = request.POST.get("skin_url")
                p = pubLOLWall()
                p.skin_name = skin_name
                p.skin_url = skin_url
                p.hero_name = hero_name
                p.hero_id = int(hero_id)
                short_link = short_url_new(skin_url)
                p.skin_short_url = short_link
                sk_size = get_size(skin_url)
                p.skin_size = sk_size
                p.save()
                send_str = '【{}更新】新增了如下英雄壁纸：||{} {}|{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'), skin_name, sk_size,
                                                               short_link)
                # send_fwx_group(WX_LOL_GROUPS, send_str, True)
                pubs = pubVarList.objects.filter(var_name="LOL_NEW_WALL")
                pub = pubs[0]
                pub.var_info = send_str
                pub.save()
                return HttpResponse("新增成功")
            else:
                return HttpResponse("游戏类型不能为空")
        except:
            write_log(3, format(traceback.format_exc()))
            return HttpResponse("新增异常")