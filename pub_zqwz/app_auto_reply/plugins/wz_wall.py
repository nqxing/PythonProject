from app_auto_reply.models import pubWZWall, pubVarList
from pub_zqwz.config import *

def return_wzSkin(name):
    end_str = ''
    # end_str = '\n\n<a href="https://mp.weixin.qq.com/s/9WY90GBIk2HlmvJWSxScLA">点此加入王者壁纸开黑群了解更多游戏动态</a>'
    values = []
    hero_name = '庄周'
    try:
        results = pubWZWall.objects.filter(hero_name_bm__contains=name)
        if len(results) != 0:
            result = '找到了{}张({})的壁纸，打开下方链接后长按图片即可保存壁纸哦，如需打包全英雄壁纸请回复“全英雄”||'.format(len(results), name)
            hero_name = results[0].hero_name
            values.append(hero_name)
            for res in results:
                mob_skin = res.mob_skin_short_url
                if mob_skin == None:
                    strs = '{}|[电脑] {}||'.format(res.skin_name, res.skin_short_url)
                else:
                    strs = '{}|[电脑] {}|[手机] {}||'.format(res.skin_name, res.skin_short_url,
                                                             res.mob_skin_short_url)
                result += strs
            result = result.strip()
            if len(result) > 1365:
                values.append(hero_name)
                values.append('该关键字信息量太大了，请换个详细点的关键字吧'+end_str)
                return values
            values.append(result+end_str)
        else:
            values.append(hero_name)
            values.append("没有找到({})的壁纸，请确认名字输入正确哦~".format(name)+end_str)
        return values

    except:
        log(3, '{}'.format(traceback.format_exc()))
        values.append(hero_name)
        values.append("抱歉~ 查询出错了，请重试~"+end_str)
        return values