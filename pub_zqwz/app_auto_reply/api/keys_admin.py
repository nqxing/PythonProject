from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from app_auto_reply.models import pubKeys, pubVarList
from django.contrib.auth import logout
from django.views import View

class KeyWZ(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            return render(request, 'key/wz.html')
        else:
            return render(request, 'key/index.html')

class VarList(View):
    def post(self, request, vars):
        value = request.session.get("msg", None)
        if value == "登录成功":
            var_info = request.POST.get("var_info").strip()
            var = pubVarList.objects.filter(var_name=vars)
            if var:
                var[0].var_info = var_info
                var[0].save()
                return HttpResponse('修改成功')
            else:
                HttpResponse("修改失败，未找到变量名")
        else:
            return HttpResponse('未登录')

class Key(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            key_values = pubKeys.objects.all()
            var_values = pubVarList.objects.all()
            return render(request, 'key/main.html', {"key_values": key_values, "var_values": var_values})
        else:
            return render(request, 'key/index.html')

    def post(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            key_text = request.POST.get("key_text")
            key_info = request.POST.get("key_info")
            if key_text != None or key_info != None:
                if len(key_text) == 0 or len(key_info) == 0:
                    return HttpResponse('输入项不能为空')
                else:
                    values = pubKeys.objects.filter(key=key_text)
                    if values.exists():
                        return HttpResponse('关键字已存在')
                    else:
                        key = pubKeys()
                        key.key = key_text
                        key.key_info = key_info
                        key.save()
                        return HttpResponse('新增成功')
            else:
                return HttpResponse('参数错误')
        else:
            return HttpResponse('未登录')

class UpKey(View):
    def post(self, request, kid):
        value = request.session.get("msg", None)
        if value == "登录成功":
            key_text = request.POST.get("key_text")
            key_info = request.POST.get("key_info")
            if key_text != None or key_info != None:
                key = pubKeys.objects.filter(pk=kid)
                if key:
                    key[0].key = key_text
                    key[0].key_info = key_info
                    key[0].save()
                    return HttpResponse('修改成功')
                else:
                    HttpResponse("未找到id")
            else:
                return HttpResponse('参数错误')
        else:
            return HttpResponse("未登录")

class Login(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            # return HttpResponse('')
            return redirect('/key')
        else:
            return render(request, 'key/index.html')

    def post(self, request):
        pwd = request.POST.get("pwd")
        if pwd != None:
            if pwd == '1996':
                request.session["msg"] = "登录成功"
                return HttpResponse(0)
                # return render(request, 'keywords/index.html', {"tips": "登录成功,正在跳转.."})
            else:
                return HttpResponse(1)
                # return render(request, 'keywords/index.html', {"tips": "密码错误,请重新输入"})
        else:
            return HttpResponse("参数错误")


def exit_login(request):
    if request.method == 'GET':
        value = request.session.get("msg", None)
        if value == "登录成功":
            logout(request)
            return redirect('/key')
        else:
            return HttpResponse('')
    else:
        return HttpResponse('')
