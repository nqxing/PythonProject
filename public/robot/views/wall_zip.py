from auto_reply.package import *
from django.http import HttpResponse
from django.views import View
from bypy import ByPy

class ZIPWall(View):
    def get(self, request):
        value = request.session.get("msg", None)
        if value == "登录成功":
            obj_type = request.GET.get("type")
            if obj_type == 'wz':
                if is_thread():
                    return HttpResponse("后台有打包任务，请勿重复打包")
                else:
                    run_main("wz")
                    write_log(1, '开始打包最新王者荣耀壁纸')
                    return HttpResponse("后台打包中")
            elif obj_type == 'lol':
                if is_thread():
                    return HttpResponse("后台有打包任务，请勿重复打包")
                else:
                    run_main("lol")
                    write_log(1, '开始打包最新英雄联盟壁纸')
                    return HttpResponse("后台打包中")
            else:
                return HttpResponse("类型不能为空")
        else:
            return HttpResponse(status=400)

def is_thread():
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if "Thread-zip-wall" in lists[i].name:
            return True
    return False

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-zip-wall')
        thr.start()
    return wrapper

@asyncs
def run_main(gname):
    try:
        if gname == 'wz':
            # 生成压缩包
            stime = datetime.datetime.now().strftime('%Y_%m_%d')
            filename = '王者荣耀壁纸_{}.zip'.format(stime)
            zip_path = r'static/wall/{}'.format(filename)
            zipDir(r'static/wall/wzry', zip_path)
            bp = ByPy()
            bp.upload(localpath="{}".format(zip_path), remotepath='wzry', ondup='overwrite')
            # os.system('bypy upload {} /wzry'.format(zip_path))
            if (os.path.exists(zip_path)):
                os.remove(zip_path)
            var = pubVarList.objects.filter(var_name="WZ_WALL_ALL")
            if var:
                var[0].var_info = '王者荣耀全英雄皮肤壁纸打包合集（{}更新）||百度网盘：<a href="https://pan.baidu.com/s/16dvLafTPL0Ncac77GjDEgg">点我下载</a> 【提取码：hsyv】'.format(stime)
                var[0].save()
                write_log(1, '链接名称更新成功')
            else:
                write_log(3, '未找到变量名')
            write_log(1, '最新王者荣耀壁纸打包完成')
        if gname == 'lol':
            # 生成压缩包
            stime = datetime.datetime.now().strftime('%Y_%m_%d')
            filename = '英雄联盟壁纸_{}.zip'.format(stime)
            zip_path = r'static/wall/{}'.format(filename)
            zipDir(r'static/wall/yxlm', zip_path)
            bp = ByPy()
            bp.upload(localpath="{}".format(zip_path), remotepath='yxlm', ondup='overwrite')
            # os.system('bypy upload {} /yxlm'.format(zip_path))
            if (os.path.exists(zip_path)):
                os.remove(zip_path)
            var = pubVarList.objects.filter(var_name="LOL_WALL_ALL")
            if var:
                var[0].var_info = '英雄联盟全英雄皮肤壁纸打包合集（{}更新）||百度网盘：<a href="https://pan.baidu.com/s/1VvJZwtNLVMk71SluJwpeWA">点我下载</a> 【提取码：nmtp】'.format(stime)
                var[0].save()
                write_log(1, '链接名称更新成功')
            else:
                write_log(3, '未找到变量名')
            write_log(1, '最新英雄联盟壁纸打包完成')
    except:
        write_log(3, traceback.format_exc())

def zipDir(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w",zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()
