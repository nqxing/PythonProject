from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import re, datetime, time
from short_url import models
import hashlib

def changeMd5(url):
    m = hashlib.md5()
    m.update(url.encode("utf-8"))
    hexStr = m.hexdigest()
    return "{}{}{}{}{}".format(hexStr[0], hexStr[7], hexStr[14], hexStr[21], hexStr[31])

def rurl(request, url):
    if request.method=="GET":
        res = models.ShortUrl.objects.filter(short_url=url).first()
        if not res or not res.ori_url:
            return HttpResponse("没有此短网址")
        if time.time() - int(time.mktime(res.period.timetuple())) > 0:
            return HttpResponse("短网址已失效")
        return redirect(res.ori_url)

    if request.method=="POST":
        return HttpResponse("Request error")

def addShortUrl(request):
    if request.method == "POST":
        response = {"status": 100, "msg": None}
        long = request.POST.get('long')
        period = request.POST.get('period')
        res = re.search("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?"
                      "((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|"
                      "([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?"
                      "(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$", long)
        if not res:
            response["msg"] = "网址错误"
            response["status"] = 101
        elif period !="一年期" and period !="长期":
            response["msg"] = "有效期格式错误"
            response["status"] = 102
        else:
            date=datetime.datetime.now()
            if period=="一年期":
                date = datetime.datetime.now() + datetime.timedelta(days=365)
            if period=="长期":
                date = datetime.datetime.now() + datetime.timedelta(days=365 * 5)
            res = models.ShortUrl.objects.create(period=date)
            n = res.id
            short_url = changeMd5(long)
            if short_url == "addShortUrl" or short_url == "restoreUrl":
                response["msg"] = "请求再转换一次试试"
                response["status"] = 103
            else:
                models.ShortUrl.objects.filter(id=n).update(short_url=short_url, ori_url=long)
                response["msg"] = short_url

        return JsonResponse(response)
    if request.method == "GET":
        return HttpResponse("No get method")

def restoreUrl(request):
    if request.method == "POST":
        response = {"status": 100, "msg": None}
        short = request.POST.get('short')
        res = re.search("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?"
                        "((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\."
                        "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                        "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                        "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|"
                        "([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?"
                        "(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$", short)
        if not res or "/" not in short:
            response["msg"] = "网址错误"
            response["status"] = 101

        else:
            short_url=short.split("/")[-1]
            res=models.ShortUrl.objects.filter(short_url=short_url).first()
            if not res:
                response["msg"] = "没有该短网址"
                response["status"] = 102
            else:
                response["msg"] = res.ori_url

        return JsonResponse(response)
