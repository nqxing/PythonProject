from auto_reply.models import pubWZWall
from auto_reply.package import *

def return_wzSkin(name):
    end_str = '\n\n<a href="https://mp.weixin.qq.com/s/9WY90GBIk2HlmvJWSxScLA">点此加入王者壁纸开黑群了解更多游戏动态</a>'
    try:
        if name == 'all' or name == 'ALL' or name == 'All':
            return pubVarList.objects.filter(var_name='WZ_WALL_ALL')[0].var_info.replace('|', '\n')+end_str
        else:
            results = pubWZWall.objects.filter(hero_name_bm__contains=name)
            if len(results) != 0:
                result = '找到了{}张({})的壁纸:\n\n'.format(len(results), name)
                for res in results:
                    mob_skin = res.mob_skin_short_url
                    if mob_skin == None:
                        strs = '{}\n[电脑] {}\n\n'.format(res.skin_name, res.skin_short_url)
                    else:
                        strs = '{}\n[电脑] {}\n[手机] {}\n\n'.format(res.skin_name, res.skin_short_url,
                                                                 res.mob_skin_short_url)
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