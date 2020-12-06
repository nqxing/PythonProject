from pub_zqwz.config import *
from app_auto_reply.plugins.wz_wall import return_wzSkin
from app_auto_reply.plugins.wz_voice import return_wzYy
from app_auto_reply.plugins.keys_menu import key_info
from app_auto_reply.models import *

def ruturn_tip(name):
    value = ''
    tips_list = list(TIP_DICT.keys())
    for i in range(50):
        if name in TIP_DICT:
            s = randint(0, len(tips_list)) - 1
            if name == tips_list[s]:
                pass
            else:
                value = TIP_DICT[tips_list[s]]
                break
        else:
            break
    return value

def reply(text):
    res = {'code': 1, 'msg': ''}
    if '壁纸' in text:
        text = text.replace('壁纸', '')
        if text:
            results = return_wzSkin(text)
            t = ruturn_tip('bz')
            rep_str = '{}||{}'.format(results[1], t.format(results[0], results[0]))
            res['msg'] = rep_str
    elif '语音' in text:
        text = text.replace('语音', '')
        if text:
            results = return_wzYy(text)
            t = ruturn_tip('yy')
            rep_str = '{}||{}'.format(results[1], t.format(results[0], results[0]))
            res['msg'] = rep_str
    elif '王者菜单' == text:
        values = pubVarList.objects.filter(var_name='WZ_PUB_MENU')
        if values:
            rep_str = values[0].var_info
            res['msg'] = rep_str
    elif '胜率' in text:
        values = pubWZwinRate.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('sl')
            wins = pubWZwinRate.objects.filter(cx_name="胜率排行榜")[0].cx_value
            rep_str = '{}{}||{}'.format(values[0].cx_value, wins, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '技能' in text:
        values = pubWZSkill.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('jn')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '出装' in text:
        values = pubWZEquip.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('cz')
            rep_str = '{}{}||{}'.format(values[0].cx_value, values[0].cx_value1, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '铭文' in text:
        values = pubWZRune.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('mw')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '克制' in text:
        values = pubWZKZ.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('kz')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '介绍' in text:
        values = pubWZIntroduce.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('js')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '组合' in text:
        values = pubWZZH.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('zh')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif '攻略' in text:
        values = pubWZSkills.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('jq')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name))
            res['msg'] = rep_str
    elif text == '小编微信':
        # rep_str = '<a href="https://mp.weixin.qq.com/s/drufLcC-t9sGl7WNA_-0LA">我的微信</a>'
        article_title = "点击添加小编微信"
        article_desc = "查看详情"
        article_img = "https://mmbiz.qpic.cn/mmbiz_png/CFpeqnV0qt7Q5D7j9yibV3JseYyUXJtZ9icpaaTcEhF8Kj4LcUtv5IkKVw0PuKzP81Roic8icWffufGEynDbdYPLgQ/0?wx_fmt=png"
        article_url = "https://mp.weixin.qq.com/s/drufLcC-t9sGl7WNA_-0LA"
        rep_str = XML_NEWS.format("{}", "{}", "{}", article_title, article_desc, article_img, article_url)
        res['code'] = 2
        res['msg'] = rep_str
    elif text == '机器人':
        # code = 1  为回复文本
        # code = 2 为回复图文信息
        # code = 3 为回复图片，msg为media_id
        res['code'] = 3
        res['msg'] = "njHpjMQsdYbNZkFSToEkBvCzrCV1XfCAVn5MNMeByR4"
    elif text == '指令' or text == '菜单' or text == '帮助':
        rep_str = pubVarList.objects.filter(var_name='ZHILING')[0].var_info
        res['msg'] = rep_str
    else:
        key_state = key_info(text)
        if key_state != -1:
            res['msg'] = key_state
        else:
            res['msg'] = pubVarList.objects.filter(var_name="NO_STR")[0].var_info
    end_str = pubVarList.objects.filter(var_name='END_STR')[0].var_info
    if end_str != 'None':
        res['msg'] += end_str
    if not res['msg']:
        res['msg'] = pubVarList.objects.filter(var_name="NO_STR")[0].var_info
    return res

