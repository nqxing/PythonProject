from app_auto_reply.models import pubWZVoice
from pub_zqwz.config import *

def return_wzYy(name):
    end_str = ''
    # end_str = '\n\n<a href="https://mp.weixin.qq.com/s/9WY90GBIk2HlmvJWSxScLA">点此加入王者壁纸开黑群了解更多游戏动态</a>'
    values = []
    hero_name = '庄周'
    try:
        results = pubWZVoice.objects.filter(hero_name__contains=name)
        if len(results) != 0:
            result = '找到了({})的皮肤语音包合集，因英雄皮肤语音较多建议先保存至自己的网盘，再打开APP在线试听后选择下载哦~ 需要其它非英雄语音请回复“oth”||'.format(name)
            hero_name = results[0].hero_name
            values.append(hero_name)
            for res in results:
                strs = '{}：{}||'.format(res.hero_name, res.voice_url)
                result += strs
            values.append(result.strip()+end_str)
        else:
            values.append(hero_name)
            values.append("没有找到({})的皮肤语音包，请确认英雄名字输入正确哦~".format(name)+end_str)
        return values
    except:
        log(3, '{}'.format(traceback.format_exc()))
        values.append(hero_name)
        values.append("抱歉~ 查询出错了，请重试~"+end_str)
        return values