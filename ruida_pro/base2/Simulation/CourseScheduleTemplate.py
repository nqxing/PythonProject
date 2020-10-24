from random import randint  # 随机函数
import xlrd
from xlutils.copy import copy
import requests
# 导入外部课表模板模拟生成


courses = ['语文', '数学', '化学', '英语', '物理', '政治', '体育与技术', '计算机信息', '地理', ]
classs = ['1班', '2班', '3班', '4班', '5班', '6班', '7班', '8班', '9班', '10班', ]
class_type = '行政班'
room_list = ['101', '201', '301', '102', '操场', '音乐教室', '', '']

def Template():
    tea_list = get_teaName()
    x = 3
    y = 5
    xls = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\课表模板\模板.xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    for i in range(len(classs)):
        # sheet.write(x, 0, classs[i])
        # sheet.write(x, 1, class_type)
        for r in range(2, 42):
            sheet.write(y, r, courses[randint(0, len(courses) - 1)])
            sheet.write(y + 1, r, tea_list[randint(0, len(tea_list) - 1)]['name'])
            sheet.write(y + 2, r, room_list[randint(0, len(room_list) - 1)])
        x += 1
        y += 3
    # sheet.write_merge(x, x + 2, 0, 0, '测试')
    # sheet.write_merge(x+3, x+3 + 2, 0, 0, '测试')
    # sheet.write_merge(x, x + 2, 0, 0, '测试')
    xlsc.save(r'C:\Users\Administrator\Desktop\课表模板\锐达模板.xls')

def get_teaName():
    url = 'http://gateway2-test.591iq.com.cn/apps/base/school/teacher/list'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
        'AccessToken': 'BD9D773800BDA08872E0E4590A79FCE4'
    }
    dict = {
        'rows': 100,
        'page': 1,
        'wordNumber': '',
        'schoolId': 1
    }
    r = requests.post(url, headers = headers, data=dict)
    return r.json()['data']['rows']

Template()