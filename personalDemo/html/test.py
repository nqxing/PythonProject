# # coding:utf-8
# TEXT = '''<p style="white-space: normal;"><span style="font-size: 14px;">{}</span></p>'''
#
#
#
# num = 0
# def fnum():
#     global num
#     num = num + 1
#     return num
#
# dict = {}
# template = '||【大神出装1】|追击刀锋 急速战靴 无尽战刃|碎星锤 影刃 名刀·司命|胜率63.85% 胜场数3240||【大神出装2】|贪婪之噬 急速战靴 无尽战刃|宗师之力 碎星锤 破军|胜率52.83% 胜场数2987||【大神出装3】|追击刀锋 急速战靴 无尽战刃|闪电匕首 碎星锤 贤者的庇护|胜率52.34% 胜场数3013'
# dslist = template.split('||')
# for ds in dslist:
#     if ds:
#         s = ds.split('|')
#         p = ''
#         ls = []
#         for k in s:
#             if '大神' in k:
#                 p += k
#             if ' ' in k:
#                 s = k.split(' ')
#                 if len(s) == 3:
#                     ls += s
#                 if len(s) == 2:
#                     u = '，'.join(s)
#                     p += u
#         dict['TEXT{}'.format(fnum())] = p
#         dict['EQUIP{}'.format(fnum())] = ls
#
# template = '【英雄】干将莫邪(法师/中路)||【技能升级】|二技能作为干将莫邪的主要输出技能，优先加点，1技能作为保命手段，可以副加，大招作为主要斩杀手段，几个关键的等级第一时间加点。||【铭文搭配】|干将莫邪定位是一个法师刺客，法术伤害及法术吸血是必须的，搭配装备，这样的铭文可以为对线阶段提供更高的续航能力！||【打法攻略】|干将莫邪没有位移技能，但是他可以通过自身的控制技能和召唤师技能来弥补这个缺陷，推荐召唤师技能闪现。前期对线阶段，可以利用2、3技能雌雄双剑来进行消耗，雌雄双剑的超远攻击距离以及弧形的弹道，会让敌方措不及防，搭配1技能击退效果带来的短暂控制，一旦拥有了大招，可以轻易的在线上单杀敌人！||【团战攻略】|团战中的干将莫邪，与单线的区别并不大，如果是主动开团，没有被突进的情况下，在团战的外围，不停的利用雌雄双剑搭配大招来进行消耗，大招命中后的冷却缩减效果，可以让干将莫邪可以在短时间内打出极高的伤害，被开团时，如果血量健康，那么可以利用自己的走位，尽量让自己的1技能能够同时命中多个敌人，给队友提供输出的空间，在血量已经低于安全范围后，迅速利用闪现远离团战中心，保证自己可以在一个安全的位置进行输出，帮助队友取得团战的胜利！'
# gllist = template.replace('||', '|').split('|')
# # print(gllist)
# gllist.pop(0)
# for gl in gllist:
#     if gl:
#         dict['TEXT{}'.format(fnum())] = gl
#
# print(dict)
#
# template = '【英雄】花木兰(战士/刺客/对抗路)|【热度排名】T2|【胜率】52.01%|【登场率】8.10%|【Ban率】0.12%|【数据更新】20201208'
# gllist = template.replace('||', '|').split('|')
# # print(gllist)
# gllist.pop(0)
# for gl in gllist:
#     if gl:
#         dict['TEXT{}'.format(fnum())] = gl
#
# print(dict)
#
#
#
# num = 0
# for i in range(5):
#     def fnum():
#         global num
#         num += 1
#         return num
#     print(fnum())
#     print(fnum())
#     print(fnum())
#     num = 0
import pymysql
mysql_conn = pymysql.connect(host="116.62.126.139", user="root", password="mm123456", port=3306, db='pub_zqwz')
# mysql_conn = pymysql.connect(host="localhost", user="root", password="123456", port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标
mysql_cursor.execute('''select * from pub_wz_item where cx_name like "%5级铭文%"''')
values = mysql_cursor.fetchall()
if values:
    for v in values:
        url = 'https://game.gtimg.cn/images/yxzj/img201606/mingwen/{}'.format(v[2].split('/')[-1])
        print(url)
        sql = '''UPDATE pub_wz_item SET cx_value = "{}" WHERE id = "{}" '''.format(url, v[0])
        mysql_cursor.execute(sql)
        mysql_conn.commit()