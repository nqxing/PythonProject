from robot.models import pubEleID, pubEleGroupSn
from auto_reply.package import *
from django.http import HttpResponse
from django.views import View

class AThongbao(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            obj_type = request.GET.get("type")
            if obj_type == 'run':
                if is_thread():
                    return HttpResponse("红包领取已开启，请勿重复开启")
                else:
                    run_main()
                    return HttpResponse("红包领取开启成功")
            elif obj_type == 'stop':
                if is_thread():
                    stop_thd("Thread-auto-hongbao")
                    return HttpResponse("红包领取已关闭")
                else:
                    return HttpResponse("红包领取未开启，无需关闭")
            else:
                return HttpResponse("指令类型不能为空")
        else:
            return HttpResponse(status=400)

# 红包监控 获取指定账号进行查询 出现最佳或最佳已被领取后退出程序
def update_hongbao(result, group_sn, hongbaoMax, phone):
    # 死循环查询，领到最佳，最佳已被领走或被服务器限制访问（此情况会重试5次）时退出循环
    if result['status'] == 0:
        if result['value']['promotion_records']:
            hongbao = len(result['value']['promotion_records'])
            if hongbao < hongbaoMax - 1:
                group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                if group_sn_values.exists():
                    for group_sn_value in group_sn_values:
                        group_sn_value.yet = hongbao
                        group_sn_value.up_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        group_sn_value.is_send = False
                        group_sn_value.save()
                mobile_values = pubEleID.objects.filter(mobile=phone)
                if mobile_values.exists():
                    for mobile in mobile_values:
                        mobile.id_info = '身份信息正常'
                        mobile.save()
                if hongbao == 0:
                    group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                    if group_sn_values.exists():
                        for group_sn_value in group_sn_values:
                            group_sn_value.delete()
                    result = {'status': 1, 'value': '[{}]-更新了该红包领取数并删除'.format(group_sn)}
                else:
                    result = {'status': 1, 'value': '[{}]-更新了该红包领取数'.format(group_sn)}
                return result
            elif hongbao == hongbaoMax - 1:
                group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                if group_sn_values.exists():
                    for group_sn_value in group_sn_values:
                        group_sn_value.yet = hongbao
                        group_sn_value.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        group_sn_value.save()
                lucky_result = lucky_hongbao(group_sn)
                if lucky_result['status'] == 0:
                    # print(lucky_result)
                    if type(lucky_result['value']['promotion_records']).__name__ == 'list':
                        if lucky_result['value']['promotion_records']:
                            for l in lucky_result['value']['promotion_records']:
                                if l['is_lucky']:
                                    lucky_name = l[
                                        'sns_username']
                                    lucky_amount = l['amount']
                                    group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                                    if group_sn_values.exists():
                                        for group_sn_value in group_sn_values:
                                            group_sn_value.delete()
                                    result = {'status': 0,
                                              'value': '[{}]-领取成功,最佳红包生成成功,领取人[{}],领取金额[{}]元'.format(group_sn,
                                                                                                     lucky_name,
                                                                                                     lucky_amount)}
                                    return result
                            result = {'status': 0, 'value': '[{}]-下个就是最大红包,但是内置账号未领取成功,可能是已达5次'.format(group_sn)}
                            return result
                        else:
                            result = {'status': 1, 'value': '领取为空,{}'.format(lucky_result)}
                            return result
                    else:
                        result = {'status': 1, 'value': '领取失败了,{}'.format(lucky_result)}
                        return result
                elif lucky_result['status'] == 1:
                    result = {'status': -1, 'value': '[{}]-领取失败,身份信息过期了'.format(group_sn)}
                    return result
                else:
                    result = {'status': 2, 'value': '[{}]-领取失败,{}'.format(group_sn, lucky_result['value'])}
                    return result
            elif hongbao == hongbaoMax:
                is_lucky = result['value']['promotion_records'][hongbaoMax - 1]['is_lucky']  # 减一是数组从0开始读
                if is_lucky:
                    group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                    if group_sn_values.exists():
                        for group_sn_value in group_sn_values:
                            group_sn_value.delete()
                result = {'status': 3, 'value': '[{}]-删除了该红包,红包最佳手气已出现'.format(group_sn)}
                return result
            elif hongbao > hongbaoMax:
                promotion_records = result['value']['promotion_records']
                for p in promotion_records:
                    is_lucky = p['is_lucky']  # 减一是数组从0开始读
                    if is_lucky:
                        group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
                        if group_sn_values.exists():
                            for group_sn_value in group_sn_values:
                                group_sn_value.delete()
                        break
                result = {'status': 4, 'value': '[{}]-删除了该红包,红包最佳手气已出现'.format(group_sn)}
                return result
        else:
            group_sn_values = pubEleGroupSn.objects.filter(group_sn=group_sn)
            if group_sn_values.exists():
                for group_sn_value in group_sn_values:
                    group_sn_value.delete()
            result = {'status': 1, 'value': '[{}]-查询失败并删除,{}'.format(group_sn, result)}
            return result
    elif result['status'] == 1:
        mobile_values = pubEleID.objects.filter(mobile=phone)
        if mobile_values.exists():
            for mobile in mobile_values:
                mobile.id_info = '未登录'
                mobile.save()
        result = {'status': -2, 'value': '[{}]-手机号[{}]身份信息过期了'.format(group_sn, phone)}
        return result
    elif result['status'] == 2 or result['status'] == -1:
        result = {'status': -3, 'value': '[{}]-{}'.format(group_sn, result['value'])}
        return result

def lucky_hongbao(group_sn):
    headers = {
        "Content-Type": "application/json",
        'X-Shard': 'loc=119.21212005615234,26.037235260009766',
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN",
        "Cookie": "SID=GKkZAu8u7DzrCdS0XbOsSpAupe098QZDchUQ"

    }
    url = 'https://mainsite-restapi.ele.me/marketing/v2/promotion/weixin/oQZUI0Wz2ndF9jFBI-sPPGr9DZFU'
    dict = {"group_sn":"{}".format(group_sn),"refer_user_id":"","weixin_uid":"","phone":"15160654911","user_id":169357636,"sns_type":6,"unionid":"o_PVDuEt0r2BVT2GDNGi1PXGj02A","platform":1,"latitude":26.037235260009766,"longitude":119.21212005615234,"weixin_username":"","weixin_avatar":""}
    try:
        r = requests.post(url, headers=headers, json=dict, verify=False)
        if r.status_code == 200 and 'promotion_records' in r.json():
            result = {'status': 0, 'value': r.json()}
            return result
        elif r.json()['message'] == '未登录':
            result = {'status': 1, 'value': r.json()}
            return result
        else:
            result = {'status': 2, 'value': r.json()}
            return result
    except:
        result = {'status': -1, 'value': 'Error :{}'.format(traceback.format_exc())}
        return result

def cx_hongbao(phone, link, sign, sid, group_sn):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN" ,
        'cookie': 'SID={}; '.format(sid)
    }
    url = 'https://h5.ele.me/restapi/marketing/v2/promotion/weixin/{}'.format(link)
    dict = {"method": "phone", "group_sn": "{}".format(group_sn), "sign": "{}".format(sign),
            "phone": "{}".format(phone), "device_id": "", "hardware_id": "", "platform": 0, "track_id": "undefined",
            "weixin_avatar": "", "weixin_username": "", "unionid": "fuck", "latitude": "", "longitude": ""}
    try:
        r = requests.post(url, headers=headers, data=dict, verify=False)
        if r.status_code == 200 and 'promotion_records' in r.json():
            result = {'status': 0, 'value': r.json()}
            return result
        elif r.json()['message'] == '未登录':
            result = {'status': 1, 'value': r.json()}
            return result
        else:
            result = {'status': 2, 'value': r.json()}
            return result
    except:
        result = {'status': -1, 'value': 'Error :{}'.format(traceback.format_exc())}
        return result

def main():
    try:
        # lucky_num = 0
        i = 0
        values = pubEleID.objects.filter(id_info='身份信息正常')
        renws = pubEleGroupSn.objects.filter(state=True)
        sign_txt("hongbao_info", '{}-----本次共查询到{}个红包，可用账号数为{}个-----'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(renws), len(values)))
        for k, renw in enumerate(renws):
            group_sn, yet_max, add_time = renw.group_sn, renw.yet_max, renw.create_time
            phone, link, sign, sid, = values[i].mobile, values[i].open_id, values[i].sign, values[i].sid
            result = cx_hongbao(phone, link, sign, sid, group_sn)
            update_result = update_hongbao(result, group_sn, yet_max, phone)
            if update_result['status'] == 0:
                sign_txt("hongbao_info", '[{}]No.{}：[{}]{}'.format(phone, k + 1, add_time, update_result['value']))
                # lucky_num += 1
                # if lucky_num == 5:
                #     stop_thd("Thread-auto-hongbao")
                #     break
            elif update_result['status'] == 1:
                pass
            elif update_result['status'] == -1:
                sign_txt("hongbao_info", '[{}]No.{}：[{}]{}'.format(phone, k + 1, add_time, update_result['value']))
                break
            else:
                sign_txt("hongbao_info", '[{}]No.{}：[{}]{}'.format(phone, k + 1, add_time, update_result['value']))
            i += 1
            if i == len(values):
                i = 0
            time.sleep(1)
    except:
        sign_txt("hongbao_info", traceback.format_exc())


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thd(names):
    # print('当前: ', threading.enumerate()) #返回一个包含正在运行的线程的list
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if names in lists[i].name:
            _async_raise(lists[i].ident, SystemExit)
            sign_txt("hongbao_info", '终止了异步进程名 [{}]'.format(names))

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-auto-hongbao" in lists[i].name:
            return True
    return False



def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName("Thread-auto-hongbao")
        thr.start()
    return wrapper

@asyncs
def run_main():
    main()
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(main, 'interval', minutes=3)
    sign_txt("hongbao_info", '自动领红包任务执行完毕，每隔3分钟执行一次')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        sign_txt("hongbao_info", '定时任务出现异常')