# coding:utf-8
from app_auto_reply.models import pubWZItem
from pub_zqwz.config import *
# HTEXT -- 灰色字体
# MTEXT -- 默认字体
# PIC -- 图片
# MARK -- 段落标题
# RUNE  --  铭文图片显示list
# EQUIP --  出装图片显示list

MTEXT = '''<p style="white-space: normal;"><span style="font-size: 15px;">{}</span></p>'''
HTEXT = '''<p style="white-space: normal;"><span style="font-size: 15px;color: rgb(136, 136, 136);">{}</span></p>'''
PIC = '''<p style="white-space: normal;"><img data-ratio="0.47368421052631576"  data-w="2280" style="margin-bottom: 12px; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); border-width: 0px; border-style: initial; border-color: initial; user-select: none; border-radius: 0.13333rem; display: block; !important; height: auto !important; visibility: visible !important;" _width="591.031px" class="" src="{}" crossorigin="anonymous" alt="图片" data-fail="0"></p>'''
MARK = '''<br><p style="white-space: normal;"><span style="font-size: 15px;"><strong style="font-size: 20px;max-width: 100%;color: rgb(217, 33, 66);letter-spacing: 0.544px;background-color: rgb(255, 255, 255);box-sizing: border-box !important;overflow-wrap: break-word !important;">{}</strong></span></p>'''
EPIC = '''<img data-ratio="0.47368421052631576"  data-w="2280" style="margin-top: 12px; margin-left: 14px; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); border-width: 0px; border-style: initial; border-color: initial; user-select: none; border-radius: 6rem;  width: 40px !important; height: 40px !important; visibility: visible !important;" _width="591.031px" class="" src="{}" crossorigin="anonymous" alt="图片" data-fail="0">'''
RPIC = '''<img data-ratio="0.47368421052631576"  data-w="2280" style="margin-top: 12px; margin-left: 14px; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); border-width: 0px; border-style: initial; border-color: initial; user-select: none; width: 44px !important; height: 51px !important; visibility: visible !important;" _width="591.031px" class="" src="{}" crossorigin="anonymous" alt="图片" data-fail="0">'''
GSTEXT = '''<div style="white-space: normal; font-size: 15px; line-height: 1.8em;">{}</div>'''


def sc_content(html_dict):
    content = ''
    htmls = list(html_dict.keys())
    for h in htmls:
        if 'MTEXT' in h:
            content += MTEXT.format(html_dict[h])
        if 'HTEXT' in h:
            content += HTEXT.format(html_dict[h])
        if 'PIC' in h:
            content += PIC.format(html_dict[h])
        if 'MARK' in h:
            content += MARK.format(html_dict[h])
        if 'GSTEXT' in h:
            content += GSTEXT.format(html_dict[h])
        if 'EQUIP' in h:
            for i,k in enumerate(html_dict[h]):
                values = pubWZItem.objects.filter(cx_name=k)
                if values.exists():
                    url = values[0].cx_value
                    content += EPIC.format(url)
                if i == len(html_dict[h]) -1:
                    content += '<br>'
        if 'RUNE' in h:
            for i,k in enumerate(html_dict[h]):
                values = pubWZItem.objects.filter(cx_name=k)
                if values.exists():
                    url = values[0].cx_value
                    content += RPIC.format(url)
                if i == len(html_dict[h]) -1:
                    content += '<br>'
    return content

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setName('Thread-upwz-item')
        thr.start()
    return wrapper

@asyncs
def html(html_dict, hero_name, hero_id):
    try:
        log(1, '正在生成英雄[{}]html页面'.format(hero_name))
        content = sc_content(html_dict)
        f = open("app_auto_reply/api/mb.txt", "r", )  # 设置文件对象
        strs = f.read()  # 将txt文件的所有内容读入到字符串str中
        f.close()  # 将文件关闭
        new_html = strs.replace('{#title#}', hero_name)
        new_html = new_html.replace('{#media_title#}', "王者荣耀{}资料库｜出装打法及攻略大全".format(hero_name))
        new_html = new_html.replace('{#content#}', content)
        # data = {'title':'My Home Page','text':'html'}
        with open('/www/wwwroot/hero/hero{}.html'.format(hero_id), 'w', encoding='utf-8') as f:  # 设置文件对象
            f.write(new_html)
        log(1, '英雄[{}]html页面生成完毕'.format(hero_name))
    except:
        log(3, traceback.format_exc())