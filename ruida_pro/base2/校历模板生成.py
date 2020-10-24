import xlrd
from xlutils.copy import copy
from IQ.base2.wanNianLi import *
def MajorTemplate():
    xls = xlrd.open_workbook(r'基础模板\空\校历模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    year,monthList = get_data()
    print('{}年日历信息获取成功,正在写入模板~'.format(year))
    new_row = 1
    for num in range(len(monthList)):
        for i in range(len(monthList[num])):
            date = '{}/{}/{}'.format(year,num+1,i+1)
            sheet.write(new_row+i, 0, date)
            sheet.write(new_row+i, 1, monthList[num][str(i+1)])
        new_row+=len(monthList[num])
    xlsc.save('基础模板\\校历模板.xls')
    print('校历模板生成成功~~')
MajorTemplate()