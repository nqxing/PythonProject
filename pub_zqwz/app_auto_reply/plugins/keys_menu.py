from app_auto_reply.models import pubKeys, pubWZHeroName, pubWZWall
from pub_zqwz.config import *
from django.db.models import Q

def key_info(key_text):
    dict = {"code": 2, "msg": ""}
    try:
        results = pubWZHeroName.objects.filter(Q(hero_name__contains=key_text) | Q(hero_name_bm__contains=key_text))
        if results:
            hero_name = results[0].hero_name
            # sinfo = '嗨~ 你是不是想了解({})相关信息呢，但是我不知道你具体想知道哪方面哦，你可以回复以下我给你列的关键字哦||'.format(hero_name)
            # es = '壁纸：获取英雄全皮肤壁纸|出装：查看英雄出装推荐|铭文：查看英雄最新铭文搭配|攻略：查看英雄打法攻略|语音：获取英雄皮肤语音包|技能：快速了解英雄技能介绍|胜率：查看英雄最新胜率榜|克制：查看英雄克制关系|介绍：查看英雄人物背景介绍|组合：查看英雄双/三排组合推荐'
            # reps = es.split('|')
            # for re in reps:
            #     res = re.split('：')
            #     r = '---------------|回复“{}{}” --> {}|'.format(hero_name, res[0], res[1])
            #     sinfo += r
            article_title = "王者荣耀{}资料库｜出装打法及攻略大全".format(hero_name)
            article_desc = "点击查看详情"
            article_img = "https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt7Q5D7j9yibV3JseYyUXJtZ9icpaaTcEhF8Kj4LcUtv5IkKVw0PuKzP81Roic8icWffufGEynDbdYPLgQ/0?wx_fmt=png"
            skins = pubWZWall.objects.filter(hero_id=results[0].hero_id)
            if skins:
                article_img = skins[len(skins) - 1].skin_url
            article_url = "http://zuiqu.net/hero/hero{}.html".format(results[0].hero_id)
            rep_str = XML_NEWS.format("{}", "{}", "{}", article_title, article_desc, article_img, article_url)
            dict['code'] = 1
            dict['msg'] = rep_str
        else:
            if '王者' in key_text:
                key_text = '王者'
            results = pubKeys.objects.filter(key__contains=key_text)
            if results:
                result = '找到了{}个和({})有关的内容哦||'.format(len(results), key_text)
                for res in results:
                    strs = '{}||'.format(res.key_info)
                    result += strs
                dict['msg'] = result
            else:
                dict['code'] = 3
    except:
        log(3, '{}'.format(traceback.format_exc()))
        dict['code'] = -1
        dict['msg'] = "抱歉~ 查询出错了，请重试~"
    return dict
