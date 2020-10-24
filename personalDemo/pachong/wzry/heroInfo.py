import requests
import re
# headers = {
#     'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
# }
# url = 'https://image.ttwz.qq.com/h5/statichtml/hero-detail/167.html'
# text = None
# var_dict = {}
# r = requests.get(url, headers=headers)
# r.encoding = 'utf-8'
# values = re.findall('<script>(.*?)</script>', r.text, re.S)
#
# for v in values:
#     if 'window.__NUXT__=function' in v:
#         text = v
# if text!= None:
#     vars = re.findall('\((.*?)\)', text, re.S)
#     if len(vars) >= 2:
#         v1 = vars[0].split(',')
#         s1 = vars[-1]
#         value_js = re.findall('{(.*?)}', s1, re.S)
#         if value_js:
#             for v in value_js:
#                 s1 = s1.replace(v, 'json数据')
#             print(s1)
#         s1 = s1.split(',')
#         print(len(v1), v1)
#         print(len(s1), s1)
#         if len(v1) == len(s1):
#             for i in range(len(v1)):
#                 s = str(s1[i])
#                 s = s.replace('"', '')
#                 s = s.replace("'", '')
#                 var_dict[v1[i]] = s
#             print(var_dict)
import re

html = """ 
【英雄】花木兰(传说之刃)|【种族】人类|【身高】174cm|【阵营】长城守卫军|【身份】长城守卫军队长|【区域】河洛|【能量】武道|【英雄关系】兰陵王(对手) 铠(长城守卫军队友) 百里守约(长城守卫军队友) 百里玄策(长城守卫军队友) 苏烈(长城守卫军队友)|【人生箴言】谁说女子不如男。
不动如山，迅烈如火！|【人物小记】花木兰身为女性，却有着不输任何男性的热血豪情，她自愿请缨镇守长城，即便因歹人暗算而背负叛徒的污名，依旧徘徊在这片边疆为守护而战。她以超绝的领导力和毋庸置疑的实力召集各路强者，击退各路魔种和马贼。张扬跋扈的亮眼红发与轻重交替的高超剑术使她成为战场上一道靓丽的风景。|【英雄语音】|离家太远会忘记故乡，杀人太多会忘掉自己|逃避解决不了战争，只会解决你自己|谁说女子不如男|姐来展示下高端操作！|想活命吗？紧跟着我！|姐可是传说！
"""

if __name__ == '__main__':
    p = re.compile('<[^>]+>')
    print(p.sub("", html))




