from auto_reply.models import pubLOLWall
from auto_reply.package import *

def return_lmSkin(name):
    end_str = '\n\n<a href="https://mp.weixin.qq.com/s/5bnPmyEsWYZqfPH1AqICCw">点此加入联盟壁纸开黑群了解更多游戏动态</a>'
    try:
        if name == 'all' or name == 'ALL' or name == 'All':
            return pubVarList.objects.filter(var_name='LOL_WALL_ALL')[0].var_info.replace('|', '\n')+end_str
        else:
            results = pubLOLWall.objects.filter(skin_name__contains=name)
            if len(results) != 0:
                result = '找到了{}张({})的壁纸:\n\n'.format(len(results), name)
                for res in results:
                    strs = '{} {}\n{}\n\n'.format(res.skin_name, res.skin_size, res.skin_short_url)
                    result += strs
                result = result.strip()
                if len(result) > 1365:
                    return '该关键字信息量太大了，请换个详细点的关键字吧'+end_str
                return result+end_str
            else:
                return "没有找到({})的壁纸，请确认名字输入正确哦~".format(name)+end_str
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        return "抱歉~ 查询出错了，请重试~"+end_str