from app_auto_reply.models import pubWZItem
from pub_zqwz.config import *
from django.http import HttpResponse
from django.views import View

class UPWZItem(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            if is_thread():
                return HttpResponse("后台有更新任务，请勿重复更新")
            else:
                run_main()
                log(1, '开始更新王者装备、铭文图标')
                return HttpResponse("后台更新中")
        else:
            return HttpResponse(status=400)

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-upwz-item" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-upwz-item')
        thr.start()
    return wrapper

@asyncs
def run_main():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        # 铭文图标
        url = 'https://h5.kohsocialapp.qq.com//app/yxzj/rune_moni/main?isOpenBattleAssist=0&serverName=%E5%BE%AE%E4%BF%A125%E5%8C%BA&areaName=%E8%8B%B9%E6%9E%9C&roleName=%E6%94%B6%E8%97%8F%E4%BA%BA%E9%97%B4%E6%AC%A2%E4%B9%90&nickname=%E9%81%8E%E5%AE%A2&isMainRole=1&appOpenid=oFhrws4pz-F5V6uY9hWSLNt576m8&areaId=4&roleId=2146322985&gameId=20001&roleJob=%E6%9C%80%E5%BC%BA%E7%8E%8B%E8%80%85&serverId=4035&accessToken=40_Mf2m3rL3DH6Zeprm6EhcXk0j62bcZwwvYnUcNvR8vrfy-_TPjI59Og5sH9JJ0m4-aAxiU3Lptey7_7SgNQyJdQxt8JPKG6JXaRi-S6guZtE&isOpenBattlePro=0&gameOpenid=owanlsqLAnE0N5cRDCf7haGOTeHE&uniqueRoleId=849648551&toOpenid=owanlsqLAnE0N5cRDCf7haGOTeHE&filterType=0&roleLevel=30&userId=493132974&appVersion=46140220120301&appVersionName=4.61.402&qi=1&wi=1&z=4035&zn=%E8%8B%B9%E6%9E%9C%E5%BE%AE%E4%BF%A125%E5%8C%BA&role=%E6%94%B6%E8%97%8F%E4%BA%BA%E9%97%B4%E6%AC%A2%E4%B9%90&platid=0&source=smoba_zhushou&algorithm=v2&version=3.1.96i&timestamp=1607581109155&appid=wxf4b1e8a3e9aaf978&openid=oFhrws4pz-F5V6uY9hWSLNt576m8&sig=fab1f115d7c922ac91e2150bb8e22ca2&encode=2&msdkEncodeParam=0532D971C6027F14215F00AFDAC8F1DD1811412561CC7BD6F8B7B392AE1DD5D98A4D54A8F10DCA47C8A4AD17BCDEC0AAD584C63018CF427AC050452BEF1BF8907D6E8C66AA2E5620F019A2A2671FECFE933E3A4C19C02E564213DC1097DB783A2FC916C78536924506F45707DC683FC36938A3776AE83DE5FFABC0D2EE63A3742A67A86F66F3103FBA84DDEE243582BAFCD344B5FA0966C05F09DBA802C6EE88B60750FEEDB31CD4F23716995C3E70ADA530975F7990CFDF34E2B6F03BEB2BB7A58A3EDC02E0BF84147C9D1BB1B298358107B874A6301160F574993247C2EE26349C9CA0DC6722C37F02955A3012E2DBE3440C37C62255807061A251AD93E864DAE8846D4C093D883EDE15EEFA7887B88DD4C629D46EA381760E6CFAE59420D8393957AF15265370F2285E021D6D727F5E6C966B4582788084E19A465393A74EEBE4F08B9CAC27117C77C263C227C0814D9644551BC81D1C'
        r = requests.get(url)
        r.encoding = 'utf-8'
        hds = pq(r.text)('.mtui-cell-mingwen').items()
        for h in hds:
            url = "https:{}".format(h('.mtui-cell__hd img').attr('data-lazysrc'))
            name = h('.mtui-cell__bd .mtui-cell_title').text()
            # print(name, url)
            values = pubWZItem.objects.filter(cx_name=name)
            if values.exists():
                zh_value = values[0]
                if url != zh_value.cx_value:
                    zh_value.cx_value = url
                    zh_value.save()
            else:
                pub = pubWZItem()
                pub.cx_name = name
                pub.cx_value = url
                pub.save()

        # 装备图标
        url = 'https://pvp.qq.com/web201605/item.shtml'
        r = requests.get(url, headers=headers)
        r.encoding = 'gbk'
        lis = pq(r.text)('#Jlist-details li').items()
        for l in lis:
            name = l('a img').attr('alt')
            url = "https:{}".format(l('a img').attr('src'))
            # print(name, url)
            values = pubWZItem.objects.filter(cx_name=name)
            if values.exists():
                zh_value = values[0]
                if url != zh_value.cx_value:
                    zh_value.cx_value = url
                    zh_value.save()
            else:
                pub = pubWZItem()
                pub.cx_name = name
                pub.cx_value = url
                pub.save()


    except:
        log(3, traceback.format_exc())
    log(1, '王者装备、铭文图标更新成功')