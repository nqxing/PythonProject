from auto_reply.package import *
from auto_reply.package.wz_wall_get import return_wzSkin
from auto_reply.package.wz_voice_get import return_wzYy
from robot.models import *

TIPS = {
    'bz': 'tips：发送“{}壁纸”可获取{}全皮肤壁纸哦，发送“王者菜单”可查看完整关键字列表',
    'jn': 'tips：发送“{}技能”可快速了解{}技能介绍哦，发送“王者菜单”可查看完整关键字列表',
    'sl': 'tips：发送“{}胜率”可查看{}最新胜率榜哦，发送“王者菜单”可查看完整关键字列表',
    'cz': 'tips：发送“{}出装”可查看{}出装推荐哦，发送“王者菜单”可查看完整关键字列表',
    'mw': 'tips：发送“{}铭文”可查看{}最新铭文搭配哦，发送“王者菜单”可查看完整关键字列表',
    'kz': 'tips：发送“{}克制”可查看{}英雄克制关系哦，发送“王者菜单”可查看完整关键字列表',
    'js': 'tips：发送“{}介绍”可查看{}的故事介绍哦，发送“王者菜单”可查看完整关键字列表',
    'zh': 'tips：发送“{}组合”可查看{}双/三排组合推荐哦，发送“王者菜单”可查看完整关键字列表',
    'jq': 'tips：发送“{}技巧”可查看{}使用技巧哦，发送“王者菜单”可查看完整关键字列表',
    'yy': 'tips：发送“{}语音”可获取{}皮肤语音包哦，发送“王者菜单”可查看完整关键字列表',
}

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

