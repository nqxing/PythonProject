from auto_reply.package import *
from auto_reply.package.wz_wall_get import return_wzSkin
from auto_reply.package.wz_voice_get import return_wzYy
from robot.models import *

def ruturn_tip(name):
    value = ''
    tips_list = list(TIPS.keys())
    for i in range(50):
        if name in TIPS:
            s = randint(0, len(tips_list)) - 1
            if name == tips_list[s]:
                pass
            else:
                value = TIPS[tips_list[s]]
                break
        else:
            break
    return value

def wz_reply(text):
    if text == 'all' or text == 'ALL' or text == 'All':
        t = ruturn_tip('bz')
        values = return_wzSkin('all')
        rep_str = '{}||{}'.format(values[1], t.format(values[0], values[0])).replace('|', '\n')
        return rep_str
    elif text == 'oth' or text == 'OTH' or text == 'Oth':
        t = ruturn_tip('yy')
        values = return_wzYy('oth')
        rep_str = '{}||{}'.format(values[1], t.format(values[0], values[0])).replace('|', '\n')
        return rep_str
    elif '壁纸' in text:
        text = text.replace('壁纸', '')
        if text:
            results = return_wzSkin(text)
            t = ruturn_tip('bz')
            rep_str = '{}||{}'.format(results[1], t.format(results[0], results[0])).replace('|', '\n')
            return rep_str
    elif '语音' in text:
        text = text.replace('语音', '')
        if text:
            results = return_wzYy(text)
            t = ruturn_tip('yy')
            rep_str = '{}||{}'.format(results[1], t.format(results[0], results[0])).replace('|', '\n')
            return rep_str
    elif '王者菜单' == text:
        values = pubVarList.objects.filter(var_name='WZ_PUB_MENU')
        if values:
            rep_str = values[0].var_info.replace('|', '\n')
            return rep_str
    elif '胜率' in text:
        values = pubWZwinRate.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('sl')
            wins = pubWZwinRate.objects.filter(cx_name="胜率排行榜")[0].cx_value
            rep_str = '{}{}||{}'.format(values[0].cx_value, wins, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '技能' in text:
        values = pubWZSkill.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('jn')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '出装' in text:
        values = pubWZEquip.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('cz')
            rep_str = '{}{}||{}'.format(values[0].cx_value, values[0].cx_value1, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '铭文' in text:
        values = pubWZRune.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('mw')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '克制' in text:
        values = pubWZKZ.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('kz')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '介绍' in text:
        values = pubWZIntroduce.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('js')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '组合' in text:
        values = pubWZZH.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('zh')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    elif '技巧' in text:
        values = pubWZSkills.objects.filter(cx_name=text)
        if values:
            t = ruturn_tip('jq')
            rep_str = '{}||{}'.format(values[0].cx_value, t.format(values[0].hero_name, values[0].hero_name)).replace('|', '\n')
            return rep_str
    else:
        pass
    return "没有找到({})有关的信息，请确认关键字输入正确哦~".format(text)

