import pdfkit
import time
from PersonalDemo.kuaiben.get_xiaoshuo import *
def sava_txt():
    h1 = '<h1>{}</h1><p>{}</p>'
    new_content = ''
    k = False
    chapters = get_zhangj('5b1739ab4e66e33f75dca017')
    f = open("qqgw_zj.txt", "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    for i in range(len(chapters)):
        title = chapters[i]['title']
        if k == False:
            print(title)
            if lines[0] == title:
                k = True
                print('找到了')
        else:
            print('开始写入-> {}'.format(title))
            body = get_content(chapters[i]['link'])
            body1 = body.replace('\n', '<br/>')
            content = h1.format(title, body1)
            # new_content += content
            with open('qqgw_zj.txt', 'w', encoding='utf-8') as file:
                file.write(chapters[i]['title'])
            with open('qqgw.txt', 'a', encoding='utf-8') as file:
                file.write(content)
            time.sleep(0.8)
def sava_pdf():
    print('正在转换成PDF..')
    f = open("qqgw.txt", "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    html = '<html><head><meta charset="UTF-8"><style>body{font-family:"微软雅黑";}p{font-size:18px;line-height:30px;}</style></head>%s</html>' % (lines[0])
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdfkit.from_string(html, '{}.pdf'.format('全球高武'), configuration=config)

# sava_txt()
sava_pdf()
