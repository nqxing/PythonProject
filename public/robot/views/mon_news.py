from django.views import View
from robot.views.mon_wz_news import get_news_wzry
from robot.views.mon_lol_news import get_news_yxlm
from auto_reply.package import *
from django.http import HttpResponse

class MonNews(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            obj_type = request.GET.get("type")
            if obj_type == 'run':
                if is_thread():
                    return HttpResponse("新闻监控已开启，请勿重复开启")
                else:
                    run_main()
                    return HttpResponse("新闻监控开启成功")
            elif obj_type == 'stop':
                if is_thread():
                    stop_thd("Thread-mon-news")
                    return HttpResponse("新闻监控已关闭")
                else:
                    return HttpResponse("新闻监控未开启，无需关闭")
            else:
                return HttpResponse("指令类型不能为空")
        else:
            return HttpResponse(status=400)

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
            write_log(1, '终止了异步进程名 [{}]'.format(names))

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-mon-news" in lists[i].name:
            return True
    return False

def main():
    write_log(1, '正在获取最新文章')
    get_news_wzry()
    get_news_yxlm()


def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName("Thread-mon-news")
        thr.start()
    return wrapper

@asyncs
def run_main():
    main()
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(main, 'interval', minutes=30)
    write_log(1, '王者荣耀、英雄联盟新闻监控任务运行中，每隔30分钟执行一次')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        write_log(3, '定时任务出现异常')