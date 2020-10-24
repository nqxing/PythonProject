from plugins.pub_fun.fun_api import *
from config import TIPS

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

def group_reply(stripped_msg):
    if '壁纸' in stripped_msg:
        stripped_msg = stripped_msg.replace('壁纸', '')
        if stripped_msg:
            results = SQL().select_wz_wall(stripped_msg)
            if len(results) != 0:
                result = '找到了{}张({})的壁纸:\n\n'.format(len(results), stripped_msg)
                for res in results:
                    mob_skin = res[6]
                    if mob_skin == None:
                        strs = '{}\n[电脑] {}\n\n'.format(res[1], res[5])
                    else:
                        strs = '{}\n[电脑] {}\n[手机] {}\n\n'.format(res[1], res[5],
                                                                 res[6])
                    result += strs
                result = result.strip()
                if len(result) > 1365:
                    return '该关键字信息量太大了，请换个详细点的关键字吧'
                else:
                    t = ruturn_tip('bz')
                    rep_str = '{}||{}'.format(result, t.format(results[0][3], results[0][3])).replace('|', '\n')
                    return rep_str.strip()
            # else:
            #     # return "没有找到({})的壁纸，请确认名字输入正确哦~".format(name) + end_str
            #     pass
    elif '菜单' == stripped_msg:
        strs1 = SQL().select_var_info('WZ_GROUP_MENU')
        strs1 = strs1.replace('|', '\n')
        return strs1.strip()
    elif '胜率' in stripped_msg:
        results = SQL().select_wz_win_rate(stripped_msg)
        if results:
            t = ruturn_tip('sl')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '技能' in stripped_msg:
        results = SQL().select_wz_skill(stripped_msg)
        if results:
            t = ruturn_tip('jn')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '出装' in stripped_msg:
        results = SQL().select_wz_equip(stripped_msg)
        if results:
            t = ruturn_tip('cz')
            rep_str = '{}{}||{}'.format(results[0][0], results[0][1], t.format(results[0][2], results[0][2])).replace(
                '|', '\n')
            return rep_str.strip()
    elif '铭文' in stripped_msg:
        results = SQL().select_wz_rune(stripped_msg)
        if results:
            t = ruturn_tip('mw')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '克制' in stripped_msg:
        results = SQL().select_wz_kz(stripped_msg)
        if results:
            t = ruturn_tip('kz')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '介绍' in stripped_msg:
        results = SQL().select_wz_introduce(stripped_msg)
        if results:
            t = ruturn_tip('js')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '组合' in stripped_msg:
        results = SQL().select_wz_zh(stripped_msg)
        if results:
            t = ruturn_tip('zh')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    elif '技巧' in stripped_msg:
        results = SQL().select_wz_jq(stripped_msg)
        if results:
            t = ruturn_tip('jq')
            rep_str = '{}||{}'.format(results[0][0], t.format(results[0][1], results[0][1])).replace('|', '\n')
            return rep_str.strip()
    else:
        return ''